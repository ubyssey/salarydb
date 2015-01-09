var rated = false;

$('.star').mouseenter(function(){
    if (!rated){
        $(this).parent().addClass('rated');
        $('.star').removeClass('fa-star').removeClass('fa-star-half-o').addClass('fa-star-o');
        $(this).prevAll().addClass('fa-star').removeClass('fa-star-o').removeClass('fa-star-half-o');
        $(this).addClass('fa-star').removeClass('fa-star-o').removeClass('fa-star-half-o');
        $(this).nextAll().addClass('fa-star-o').removeClass('fa-star').removeClass('fa-star-half-o');
    }
});

$('.stars').mouseleave(function(){
    if (!rated){
        $(this).removeClass('rated');
        $('.star').removeClass('fa-star').removeClass('fa-star-o').removeClass('rated');
        $('.star.full').addClass('fa-star');
        $('.star.half').addClass('fa-star-half-o');
        $('.star.empty').addClass('fa-star-o');
    }
});

$('.star').click(function(){
    if (!rated){
        var rating = $(this).data("rating");
        rated = true;
        $.getJSON(BASE_URL+'/api/vote/'+ID+'/', { rating: rating }, function(data){
            if(data.success){
                $('.rating .message').text("Thanks for voting");
            } else {
                $('.rating .message').text("You've already voted!");
                rated = false;
            }
        });
    }
})

var margin = {top: 0, right: 60, bottom: 30, left: 30},
    width = 560 - margin.left - margin.right,
    height = 340 - margin.top - margin.bottom;

var bisectLeft = d3.bisector(function(d) { return d.x; }).left;

var x = d3.scale.linear()
    .range([0, width + 10]);

var y = d3.scale.linear()
    .range([height - 10, 0]);

var xAxis = d3.svg.axis()
    .ticks(5)
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var area = d3.svg.area()
    .interpolate('basis')
    .x(function(d) { return x(d.x); })
    .y0(height)
    .y1(function(d) { return y(d.y); });

var line = d3.svg.line()
    .x(function(d) { return x(d.x); })
    .y(function(d) { return y(d.y); })
    .interpolate('basis');

var svg = d3.select('.chart').append("svg")
    .attr("id", "chart-overall")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("viewBox", "0 0 " + (width + margin.left + margin.right) + " " + (height + margin.top + margin.bottom))
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// HELPER FUNCTIONS

var getOrdinal = function(n) {
   var s=["th","st","nd","rd"],
       v=n%100;
   return n+(s[(v-20)%10]||s[v]||s[0]);
}

var calcPercentile = function(data, value){
    if(data.indexOf(value) == -1)
        return false;
    var dec = data.indexOf(value)/data.length;
    return getOrdinal(Math.floor(dec*100));
}

var getY = function(x0) {
    var i = bisectLeft(data, x0, 1),
        d0 = data[i - 1],
        d1 = data[i],
        d = x0 - d0.x > d1.x - x0 ? d1 : d0;
    return d;
}

var drawGraph = function(url, svg) {
    d3.json(url, function(error, json) {
        if (error) return console.warn(error);
        data = json.points;
        salaries = json.salaries;

        x.domain(d3.extent(data, function(d) { return d.x; }));
        y.domain(d3.extent(data, function(d) { return d.y; }));

        svg.append("path")
            .datum(data)
            .attr("class", "area")
            .attr("clip-path", "url(#clip)")
            .attr("d", area);

        svg.append("path")
            .datum(data)
            .attr("class", "line")
            .attr("d", line);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end");

        cPos = getY(EMPLOYEE);

        var eLine = svg.append("line")
            .style("stroke", "red")
            .attr("x1", x(EMPLOYEE))
            .attr("x2", x(EMPLOYEE))
            .attr("y0", 0)
            .attr("y1", height);

        var percentile = calcPercentile(salaries, EMPLOYEE);

        var perBox = svg.append("g");

        perBox.append("rect")
            .attr("x", (x(EMPLOYEE) - 50))
            .attr("y", ((height/2) - 19))
            .style("fill", "white")
            .style("stroke", "grey")
            .attr("rx", 2)
            .attr("ry", 2)
            .attr("width", 100)
            .attr("height", 30);

        perBox.append("text")
            .text(percentile + " percentile")
            .style("text-anchor", "middle")
            .style("font-size", "12px")
            .attr("x", (x(EMPLOYEE)))
            .attr("y", height/2);

        $('.charts').tabs();
        $('.chart-tabs').show();

    });
}

drawGraph(BASE_URL+"/static/data/salaries.json", svg);

if(FACULTY){
    var faculty = d3.select('.chart').append("svg")
        .attr("id", "chart-faculty")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("viewBox", "0 0 " + (width + margin.left + margin.right) + " " + (height + margin.top + margin.bottom))
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    drawGraph(BASE_URL+"/api/faculty/"+FACULTY, faculty);
}



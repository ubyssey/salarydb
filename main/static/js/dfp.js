$(document).ready(function(){
	var dfpslots=$("body").find(".adslot").filter(":visible"),
	i=0,
	slot= new Array();

	if (dfpslots.length) {
		googletag.cmd.push(function() {
			$(dfpslots).each(function(){
				slot[i] = googletag.defineSlot('/61222807/'+$(this).attr('data-dfp'), [$(this).width(), $(this).height()], 	$(this).attr('id')).addService(googletag.pubads());
				i++
			});

			googletag.enableServices();

			$(dfpslots).each(function(){
				googletag.display($(this).attr('id'));
			});
		});
	}
});

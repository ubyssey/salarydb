select
  f.id,
	count(*) as emp_count,
    avg(e.remuneration) as avg_salary,
    f.short_name
from
	salarydb.main_employee as e
join salarydb.main_faculty f on (e.faculty_id = f.id)
group by
	f.id
order by
    avg_salary desc
select
	count(*) as emp_count,
    avg(e.remuneration) as avg_salary,
    d.name as dept_name
from
	salarydb.main_employee as e
join salarydb.main_department d on (e.department_id = d.id)
group by
	d.id
order by
    avg_salary desc
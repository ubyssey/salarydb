select
	count(*) as emp_count,
    avg(e.remuneration) as avg_salary,
    d.name as dept_name
from
	salarydb.salarydb_employee as e
join salarydb.salarydb_department d on (e.department_id = d.id)
group by
	d.id
order by
    avg_salary desc

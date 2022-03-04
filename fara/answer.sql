select state, count(*) from registrants r
group by state
order by count desc
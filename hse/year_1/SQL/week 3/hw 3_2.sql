/*кому бы это не попалось на проверку, простите...*/

select distinct 'GLE' as "Indicator", 
(select lifeexpectancy 
	from country 
	where governmentform = 'Federal Republic'
	and lifeexpectancy is not null
	order by lifeexpectancy desc limit 1) 
as "Federal Republic", 
(select lifeexpectancy 
	from country 
	where governmentform = 'Republic'
	and lifeexpectancy is not null
	order by lifeexpectancy desc limit 1) 
as "Republic",
(select lifeexpectancy 
	from country 
	where governmentform not in ('Republic', 'Federal Republic')
	and lifeexpectancy is not null
	order by lifeexpectancy desc limit 1)
as "Other"
from country
union
select distinct 'LLE' as "Indicator", 
(select lifeexpectancy 
	from country 
	where governmentform = 'Federal Republic'
	and lifeexpectancy is not null
	order by lifeexpectancy limit 1), 
(select lifeexpectancy 
	from country 
	where governmentform = 'Republic'
	and lifeexpectancy is not null
	order by lifeexpectancy limit 1),
(select lifeexpectancy
	from country 
	where governmentform not in ('Republic', 'Federal Republic')
	and lifeexpectancy is not null
	order by lifeexpectancy limit 1)
from country

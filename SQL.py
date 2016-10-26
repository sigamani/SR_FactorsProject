
stringCoverage = """

set statement_timeout to 1200000;

select
p.year, 
p.num as count_market,
a.num as count_dpr, 
b.num as count_ebit, 
c.num as count_ev,
d.num as count_ndpy,
e.num as count_tat,
f.num as count_gpm,
g.num as count_gi,
h.num as count_opm,
i.num as count_roa,
j.num as count_roic,
k.num as count_ae

from (
select year, count(data) as num
from wsfactorsubset
where fieldid = 5055
and timeseriesfrequency = 'A'
group by year
) p

left join (
select w2.fieldid, w2.year, count(w2.data) as num
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 09504 --  Dividend payout ratio
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) a on a.year=p.year

left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 18191 -- EBIT
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) b on b.year=p.year

left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 18100 -- EV
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) c on c.year=p.year


left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 03255 -- Net Debt Paydown Yield
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) d on d.year=p.year


left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08401 -- Total Asset Turnover
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) e on e.year=p.year


left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08306 -- Gross Profit Margin
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) f on f.year=p.year


left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 01100 -- Gross Income
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) g on g.year=p.year


left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08316 -- Operating Profit Margin
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) h on h.year=p.year


left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08326 -- Return on Assets
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) i on i.year=p.year


left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08376 -- Return on Invested Capital
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) j on j.year=p.year


left join (
select w2.fieldid, w2.year, count(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 02999 --  Assets/Equity
and w2.timeseriesfrequency = 'A'
and w1.timeseriesfrequency = 'A'
group by w2.year, w2.fieldid
) k on k.year=p.year


order by p.year asc;

"""

stringCoverageWeighted = """

set statement_timeout to 1200000;

select 
 f.fieldid,
 wsfields.description,
 f.year,
 f.FactorCount AS FactorCount,
 MCap.FactorCount as MCapCount,
 case when MCap.FactorCount<>0 then cast(f.FactorCount as real)/cast(MCap.FactorCount as real) else 0 end as EqualWgtCoverage,
 f.MCapSum as MCapSumValidFactor,
 MCap.MCapSum AS MCapSum,
 case when MCap.MCapSum<>0 then f.MCapSum/MCap.MCapSum else 0 end as MCapWgtCoverage
from 
(
	select
		f.year,
		f.fieldID,
		count(f.data) as FactorCount,
		sum(MCap.data) as MCapSum
	from wsfactorsubset Price
	inner join wscountry c on c.wscode = Price.wscode
	inner join wsfactorsubset f
	on f.wscode = Price.wscode
	and f.timeseriesfrequency = Price.timeseriesfrequency
	and f.year = Price.year
	and f.fieldid in(09504,18191,08401,08306,01100,08326,08376,02999,03501,01001,05201,7210)
	left join wsfactorsubset MCap
	on MCap.wscode = Price.wscode
	and MCap.timeseriesfrequency = Price.timeseriesfrequency
	and MCap.year = Price.year
	and MCap.fieldid =7210
	where price.fieldid = 5055--7210
	and price.timeseriesfrequency = 'A'
	group by f.fieldid, f.year--, c.country
) f
full outer join
(
	select
		price.year,
		price.fieldID,
		count(price.data) as FactorCount,
		sum(MCap.data) as MCapSum
	from wsfactorsubset Price
	inner join wscountry c on c.wscode = Price.wscode
	left join wsfactorsubset MCap
	on MCap.wscode = Price.wscode
	and MCap.timeseriesfrequency = Price.timeseriesfrequency
	and MCap.year = Price.year
	and MCap.fieldid =7210
	where price.fieldid = 5055--7210
	and price.timeseriesfrequency = 'A'
	group by price.fieldid, price.year
) MCap on MCap.year = f.year
join wsfields on wsfields.fieldid = f.fieldID
order by f.fieldID, f.year
"""

stringCountryCoverage = """
set statement_timeout to 1200000;

select
f.year,f.PriceCount as count_market,g.FactorCount as count_gi,f.country
from (
	select  
		n1.year,
		c.country,
		count(n1.*) as PriceCount
	from wsfactorsubset n1
	join wscountry c on c.wscode = n1.wscode
	where n1.fieldid = 5055
	and n1.timeseriesfrequency = 'A'
	--and n1.year = 2005
	group by n1.year, c.country
) f
join (
	select  
		n1.year,
		c.country,
		count(n1.*) as FactorCount
	from wsfactorsubset n1
	join wsfactorsubset n2 on n1.wscode=n2.wscode 
	join wscountry c on c.wscode = n1.wscode
	and n1.year=n2.year 
	and n1.timeseriesfrequency=n2.timeseriesfrequency 
	and n2.fieldid=5055
	where n1.fieldid = 09504 --divpayratio
	and n1.timeseriesfrequency = 'A'
	--and n1.year = 2005
	group by n1.year, c.country
) g on g.year = f.year and g.country =f.country
order by f.year asc;
"""

stringCountryCoverage2 = """
set statement_timeout to 1200000;

select
f.year,f.PriceCount as count_market,g.FactorCount as count_gi,f.nationcode
from (
	select  
		n1.year,
		c.nationcode,
		count(n1.*) as PriceCount
	from wsfactorsubset n1
	join wscountry c on c.wscode = n1.wscode
	where n1.fieldid = 5055
	and n1.timeseriesfrequency = 'A'
	--and n1.year = 2005
	group by n1.year, c.nationcode
) f
join (
	select  
		n1.year,
		c.nationcode,
		count(n1.*) as FactorCount
	from wsfactorsubset n1
	join wsfactorsubset n2 on n1.wscode=n2.wscode 
	join wscountry c on c.wscode = n1.wscode
	and n1.year=n2.year 
	and n1.timeseriesfrequency=n2.timeseriesfrequency 
	and n2.fieldid=5055
	where n1.fieldid = 1100
	and n1.timeseriesfrequency = 'A'
	--and n1.year = 2005
	group by n1.year, c.nationcode
) g on g.year = f.year and g.nationcode =f.nationcode
order by f.year asc;
"""


stringMean = """
set statement_timeout to 1200000;

select
p.year, 
round(a.num,1) as avg_dpr, 
round(b.num,1) as avg_ebit, 
round(c.num,1) as avg_ev,
round(d.num,1) as avg_ndpy,
round(e.num,1) as avg_tat,
round(f.num,1) as avg_gpm,
round(g.num,1) as avg_gi,
round(h.num,1) as avg_opm,
round(i.num,1) as avg_roa,
round(j.num,1) as avg_roic,
round(k.num,1) as avg_ae

from (
select year, count(data) as num
from wsfactorsubset
where fieldid = 5055
group by year
) p

left join (
select w2.fieldid, w2.year, avg(w2.data) as num
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 09504 --  Dividend payout ratio
group by w2.year, w2.fieldid
) a on a.year=p.year

left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 18191 -- EBIT
group by w2.year, w2.fieldid
) b on b.year=p.year

left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 18100 -- EV
group by w2.year, w2.fieldid
) c on c.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 03255 -- Net Debt Paydown Yield
group by w2.year, w2.fieldid
) d on d.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08401 -- Total Asset Turnover
group by w2.year, w2.fieldid
) e on e.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08306 -- Gross Profit Margin
group by w2.year, w2.fieldid
) f on f.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 01100 -- Gross Income
group by w2.year, w2.fieldid
) g on g.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08316 -- Operating Profit Margin
group by w2.year, w2.fieldid
) h on h.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08326 -- Return on Assets
group by w2.year, w2.fieldid
) i on i.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08376 -- Return on Invested Capital
group by w2.year, w2.fieldid
) j on j.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 02999 --  Assets/Equity
group by w2.year, w2.fieldid
) k on k.year=p.year


order by p.year asc;

"""

stringMedian = """

set statement_timeout to 1200000;

select
p.year, 
a.num as avg_dpr, 
b.num as avg_ebit, 
c.num as avg_ev,
d.num as avg_ndpy,
e.num as avg_tat,
f.num as avg_gpm,
g.num as avg_gi,
h.num as avg_opm,
i.num as avg_roa,
j.num as avg_roic,
k.num as avg_ae

from (
select year, count(data) as num
from wsfactorsubset
where fieldid = 5055
group by year
) p


left join (
select distinct w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 9504 --  Dividend payout ratio
group by w2.year, w2.fieldid, w2.data
) a on a.year=p.year

left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 18191 -- EBIT
group by w2.year, w2.fieldid, w2.data
) b on b.year=p.year

left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 18100 -- EV
group by w2.year, w2.fieldid, w2.data
) c on c.year=p.year


left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 03255 -- Net Debt Paydown Yield
group by w2.year, w2.fieldid, w2.data
) d on d.year=p.year


left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08401 -- Total Asset Turnover
group by w2.year, w2.fieldid, w2.data
) e on e.year=p.year


left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08306 -- Gross Profit Margin
group by w2.year, w2.fieldid, w2.data
) f on f.year=p.year


left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 01100 -- Gross Income
group by w2.year, w2.fieldid, w2.data
) g on g.year=p.year


left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08316 -- Operating Profit Margin
group by w2.year, w2.fieldid, w2.data
) h on h.year=p.year


left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08326 -- Return on Assets
group by w2.year, w2.fieldid, w2.data
) i on i.year=p.year


left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 08376 -- Return on Invested Capital
group by w2.year, w2.fieldid, w2.data
) j on j.year=p.year


left join (
select w2.fieldid, w2.year, median(w2.data) 
over(partition by w2.year) as num

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
where w2.fieldid = 02999 --  Assets/Equity
group by w2.year, w2.fieldid, w2.data
) k on k.year=p.year


order by p.year asc;

"""

stringMeanWeighted = """

set statement_timeout to 1200000;

select
p.year,
round(p.factor_val,1) as avg_dpr,
round(p.weighted_factor_val,1) as mcapweightedavg_dpr,
round(b.factor_val,1) as avg_ebit,
round(b.weighted_factor_val,1) as mcapweightedavg_ebit,
round(c.factor_val,1) as avg_ev,
round(c.weighted_factor_val,1) as mcapweightedavg_ev,
round(d.factor_val,1) as avg_ndpy,
round(d.weighted_factor_val,1) as mcapweightedavg_ndpy,
round(e.factor_val,1) as avg_tat,
round(e.weighted_factor_val,1) as mcapweightedavg_tat,
round(f.factor_val,1) as avg_gpm,
round(f.weighted_factor_val,1) as mcapweightedavg_gpm,
round(g.factor_val,1) as avg_gi,
round(g.weighted_factor_val,1) as mcapweightedavg_gi,
round(h.factor_val,1) as avg_opm,
round(h.weighted_factor_val,1) as mcapweightedavg_opm,
round(i.factor_val,1) as avg_roa,
round(i.weighted_factor_val,1) as mcapweightedavg_roa,
round(j.factor_val,1) as avg_roic,
round(j.weighted_factor_val,1) as mcapweightedavg_roic,
round(k.factor_val,1) as avg_a,
round(k.weighted_factor_val,1) as mcapweightedavg_a,
round(l.factor_val,1) as avg_e,
round(l.weighted_factor_val,1) as mcapweightedavg_e

from (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 09504
group by w2.fieldid, w2.year) p


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 18191
group by w2.fieldid, w2.year
) b on b.year=p.year

left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 18100 -- EV
group by w2.fieldid, w2.year
) c on c.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 03255 -- Net Debt Paydown Yield
group by w2.fieldid, w2.year
) d on d.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08401 -- Total Asset Turnover
group by w2.fieldid, w2.year
) e on e.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08306 -- Gross Profit Margin
group by w2.fieldid, w2.year
) f on f.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 01100 -- Gross Income
group by w2.fieldid, w2.year
) g on g.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08316 -- Operating Profit Margin
group by w2.fieldid, w2.year
) h on h.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08326 -- Return on Assets
group by w2.fieldid, w2.year
) i on i.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08376 -- Return on Invested Capital
group by w2.fieldid, w2.year
) j on j.year=p.year


left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 02999 --  Assets
group by w2.fieldid, w2.year
) k on k.year=p.year

left join (
select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 3501 -- Equities
group by w2.fieldid, w2.year
) l on l.year=p.year

order by year asc 

"""

stringMeanWeightedTruncated = """

select 
table1.year, 
f_roundsf(table1.truncated_mean_a,2) as t_avg_dpr, f_roundsf(table1.truncated_weighted_mean_a,2) as tw_avg_dpr, 
f_roundsf(table2.truncated_mean_a,2) as t_avg_ebit, f_roundsf(table2.truncated_weighted_mean_a,2) as tw_avg_ebit,
f_roundsf(table3.truncated_mean_a,2) as t_avg_ev, f_roundsf(table3.truncated_weighted_mean_a,2) as tw_avg_ev,
f_roundsf(table4.truncated_mean_a,2) as t_avg_ndpy, f_roundsf(table4.truncated_weighted_mean_a,2) as tw_avg_ndpy,
round(table5.truncated_mean_a,1) as t_avg_tat, round(table5.truncated_weighted_mean_a,1) as tw_avg_tat,
f_roundsf(table6.truncated_mean_a,2) as t_avg_gpm, f_roundsf(table6.truncated_weighted_mean_a,2) as tw_avg_gpm,
f_roundsf(table7.truncated_mean_a,2) as t_avg_gi, f_roundsf(table7.truncated_weighted_mean_a,2) as tw_avg_gi,
f_roundsf(table8.truncated_mean_a,2) as t_avg_opm, f_roundsf(table8.truncated_weighted_mean_a,2) as tw_avg_opm,
f_roundsf(table9.truncated_mean_a,2) as t_avg_roa, f_roundsf(table9.truncated_weighted_mean_a,2) as tw_avg_roa,
f_roundsf(table10.truncated_mean_a,2) as t_avg_roic, f_roundsf(table10.truncated_weighted_mean_a,2) as tw_avg_roic,
f_roundsf(table11.truncated_mean_a,2) as t_avg_a, f_roundsf(table11.truncated_weighted_mean_a,2) as tw_avg_a,
f_roundsf(table12.truncated_mean_a,2) as t_avg_e, f_roundsf(table12.truncated_weighted_mean_a,2) as tw_avg_e


from (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 09504 -- Dividend payout ratio
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 09504 -- Dividend payout ratio
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table1

left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 18191 -- EBIT
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 18191 -- EBIT
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table2 on table1.year = table2.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 18100 -- EV
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 18100 -- EV
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table3 on table1.year = table3.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 03255 -- Net Debt Paydown Yield
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 03255 -- Net Debt Paydown Yield
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table4 on table1.year = table4.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08401 -- Total Asset Turnover
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08401 -- Total Asset Turnover
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table5 on table1.year = table5.year



left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08306 -- Gross Profit Margin
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08306 -- Gross Profit Margin
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table6 on table1.year = table6.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 01100 -- Gross Income
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 01100 -- Gross Income
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table7 on table1.year = table7.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08316 -- Operating Profit Margin
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08316 -- Operating Profit Margin
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table8 on table1.year = table8.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08326 -- Return on Assets
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08326 -- Return on Assets
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table9 on table1.year = table9.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08376 -- Return on Invested Capital
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 08376 -- Return on Invested Capital
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table10 on table1.year = table10.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 02999 -- Assets
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 02999 -- Assets
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table11 on table1.year = table11.year


left join (
select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
(select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 3501 -- Equities
group by w2.fieldid, w2.year
) stdevTable
join (
select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

from wsfactorsubset w1
join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
where w2.fieldid = 3501 -- Equities
) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and f.data>stdevTable.ThreeSigM and f.data<stdevTable.ThreeSigP
) k
group by k.year
) table12 on table1.year = table12.year

order by year asc

"""

def stringBoxSmall(s): 

    string = """
    set statement_timeout to 1200000;

    select 
    p.wscode,
    a.year,
    round(a.num,1) as data

    from (
    select wscode
    from wsfactorsubset
    where fieldid = 5055 
    group by wscode
    ) p

    join (
    select w2.fieldid, w2.wscode, w2.year, w2.data as num
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    where w2.fieldid = """+ str(s) + """ and w2.year >= 1980
    group by w2.wscode, w2.fieldid, w2.data, w2.year
    ) a on a.wscode=p.wscode

    """
    return string

def stringBoxSmallTruncated(s): 

    
    string = """

    set statement_timeout to 1200000;

    select a.wscode, a.year, round(a.num,1) as data, b.ThreeSigP, b.ThreeSigM

    from (
    select w2.fieldid, w2.wscode, w2.year, w2.data as num
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    where w2.fieldid = """+ str(s) + """
    and w2.year >= 1980
    group by w2.wscode, w2.fieldid, w2.data, w2.year
    ) a 

    join (

    select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.fieldid, w2.year ) b on b.year = a.year 
    """

    return string 

stringTEST = """

set statement_timeout to 1200000;

declare @ClassificationTypeID int = 1

select * from SRPA_ENT..[security] s
join SRPA_ENT..securityidentifier si on si.securityid = s.securityid and si.securitycodetypeid = 11 --WSCodes only
join SRPA_ENT..securitycountry sc on sc.securityid = s.securityid and sc.ClassificationTypeID = @ClassificationTypeID
join SRPA_ENT..securitysector ss on ss.securityid = s.securityid and ss.ClassificationTypeID = @ClassificationTypeID
join (
select distinct wscode,year,WSFieldID as fieldid,ROUND(Value,0) as data  from [wshistory].[ws].[LoadData] d
where d.WSFieldID = 730 -- GROSS INCOME
and [year] >= 1980
and FrequencyID = 'A' and FrequencyNum =1
) d on si.securitycode =d.wscode
where s.AssetTypeID=1 --equities only

order by sc.countryid, ss.sectorid, d.wscode
"""

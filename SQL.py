
TruncationLookup = {"DividendPayoutRatioMinus":      0,     "DividendPayoutRatioPlus":        100,
                    "GrossProfitMarginMinus":       -3000,  "GrossProfitMarginPlus":          100,
                    "OperatingProfitMarginMinus":   -12000, "OperatingProfitMarginPlus":      100,
                    "GrossProfitOverAssetsMinus":   -150,   "GrossProfitOverAssetsPlus":      150,
                    "EBITOverEVMinus":              -5,     "EBITOverEVPlus":                 5,
                    "NetDebtPaydownYieldMinus":     -1000,  "NetDebtPaydownYieldPlus":        1000,
                    "TotalAssetTurnoverMinus":       0,     "TotalAssetTurnoverPlus":         5,
                    "ReturnOnAssetsMinus":          -500,   "ReturnOnAssetsPlus":             50,
                    "ReturnOnInvestedCapitalMinus": -500,   "ReturnOnInvestedCapitalPlus":    50,
                    "AssetsOverEquityMinus":         0,     "AssetsOverEquityPlus":           50 
                    }


def stringCoverage(): 
    
    string = """

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
	    from wsfactorsubsetfilled Price
	    inner join wscountry c on c.wscode = Price.wscode
	    inner join wsfactorsubsetfilled f
	    on f.wscode = Price.wscode
	    and f.timeseriesfrequency = Price.timeseriesfrequency
	    and f.year = Price.year
	    and f.fieldid in(09504,18191,18100,3255,08401,08306,8316,30005,08326,08376,02999,03501,01001,05201,7210)
	    left join wsfactorsubsetfilled MCap
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
	    from wsfactorsubsetfilled Price
	    inner join wscountry c on c.wscode = Price.wscode
	    left join wsfactorsubsetfilled MCap
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
    return string


def stringDataforOneFactor(s):

    string = """
    set statement_timeout to 1200000;

    select 
    p.wscode,
    a.year,
    round(a.num,3) as data

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
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """ and w2.year >= 1980
    group by w2.wscode, w2.fieldid, w2.data, w2.year
    ) a on a.wscode=p.wscode
    """

    return string


def stringDataforOneFactorTruncated(s): 

    if (s == 9504):
        truncationP = TruncationLookup["DividendPayoutRatioPlus"]
        truncationM = TruncationLookup["DividendPayoutRatioMinus"]

    if (s == 30007):
        truncationP = TruncationLookup["GrossProfitMarginPlus"]
        truncationM = TruncationLookup["GrossProfitMarginMinus"]

    if (s == 8316):
        truncationP = TruncationLookup["OperatingProfitMarginPlus"]
        truncationM = TruncationLookup["OperatingProfitMarginMinus"]

    if (s == 30006):
        truncationP = TruncationLookup["GrossProfitOverAssetsPlus"]
        truncationM = TruncationLookup["GrossProfitOverAssetsMinus"]

    if (s == 30002):
        truncationP = TruncationLookup["EBITOverEVPlus"]
        truncationM = TruncationLookup["EBITOverEVMinus"]

    if (s == 30004):
        truncationP = TruncationLookup["NetDebtPaydownYieldPlus"]
        truncationM = TruncationLookup["NetDebtPaydownYieldMinus"]

    if (s == 8401):
        truncationP = TruncationLookup["TotalAssetTurnoverPlus"]
        truncationM = TruncationLookup["TotalAssetTurnoverMinus"]

    if (s == 8326):
        truncationP = TruncationLookup["ReturnOnAssetsPlus"]
        truncationM = TruncationLookup["ReturnOnAssetsMinus"]

    if (s == 8376):
        truncationP = TruncationLookup["ReturnOnInvestedCapitalPlus"]
        truncationM = TruncationLookup["ReturnOnInvestedCapitalMinus"]

    if (s == 30003):
        truncationP = TruncationLookup["AssetsOverEquityPlus"]
        truncationM = TruncationLookup["AssetsOverEquityMinus"]


    string = """
    set statement_timeout to 1200000;

    select a.wscode, a.year, round(a.num,3) as data, b.ThreeSigP, b.ThreeSigM

    from (
    select w2.fieldid, w2.wscode, w2.year, w2.data as num
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    where w2.fieldid = """+ str(s) + """
    and w2.data <= """+ str(truncationP) + """
    and w2.data >= """+ str(truncationM) + """
    and w2.year >= 1980
    group by w2.wscode, w2.fieldid, w2.data, w2.year
    ) a 

    join (

    select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    and w2.data <= """+ str(truncationP) + """
    and w2.data >= """+ str(truncationM) + """
    group by w2.fieldid, w2.year ) b on b.year = a.year 
    """

    return string 


stringMeanWeighted =  """
    set statement_timeout to 1200000;

    select
    p.year,
    round(p.factor_val,3) as t_avg_dpr,
    round(p.weighted_factor_val,3) as tw_avg_dpr,
    round(d.factor_val,1) as t_avg_ndpy,
    round(d.weighted_factor_val,1) as tw_avg_ndpy,
    round(e.factor_val,1) as t_avg_tat,
    round(e.weighted_factor_val,1) as tw_avg_tat,
    round(f.factor_val,3) as t_avg_gpm,
    round(f.weighted_factor_val,3) as tw_avg_gpm,
    round(g.factor_val,1) as t_avg_gi,
    round(g.weighted_factor_val,1) as tw_avg_gi,
    round(h.factor_val,1) as t_avg_opm,
    round(h.weighted_factor_val,1) as tw_avg_opm,
    round(i.factor_val,1) as t_avg_roa,
    round(i.weighted_factor_val,1) as tw_avg_roa,
    round(j.factor_val,1) as t_avg_roic,
    round(j.weighted_factor_val,1) as tw_avg_roic,
    round(k.factor_val,1) as t_avg_ae,
    round(k.weighted_factor_val,1) as tw_avg_ae,
    round(m.factor_val,3) as t_avg_ebitev,
    round(m.weighted_factor_val,3) as tw_avg_ebitev

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
    where w2.fieldid = 30004 -- Net Debt Paydown Yield
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
    where w2.fieldid = 30003 --  Assets/Equity
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

    left join (
    select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = 30002 -- EBIT/EV
    group by w2.fieldid, w2.year
    ) m on m.year=p.year

    left join (
    select w2.fieldid, w2.year, avg(w2.data) as factor_val, SUM(w2.data*w3.data)/SUM(case when w2.data is not null then w3.data else 0 end) as weighted_factor_val
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = 30001 -- Gross income (banking)
    group by w2.fieldid, w2.year
    ) n on n.year=p.year

    order by year asc 

    """




def stringMeanWeightedTruncated(s): 


    string = """
            set statement_timeout to 1200000;
            select 
            table13.year, 
            round(table1.truncated_mean_a,3) as t_avg_dpr, round(table1.truncated_weighted_mean_a,3) as tw_avg_dpr, 
            round(table4.truncated_mean_a,1) as t_avg_ndpy, round(table4.truncated_weighted_mean_a,1) as tw_avg_ndpy,
            round(table5.truncated_mean_a,1) as t_avg_tat, round(table5.truncated_weighted_mean_a,1) as tw_avg_tat,
             round(table6.truncated_mean_a,3) as t_avg_gpm, round(table6.truncated_weighted_mean_a,2) as tw_avg_gpm,
            f_roundsf(table7.truncated_mean_a,2) as t_avg_gi, f_roundsf(table7.truncated_weighted_mean_a,2) as tw_avg_gi,
            f_roundsf(table8.truncated_mean_a,2) as t_avg_opm, f_roundsf(table8.truncated_weighted_mean_a,2) as tw_avg_opm,
            f_roundsf(table9.truncated_mean_a,2) as t_avg_roa, f_roundsf(table9.truncated_weighted_mean_a,2) as tw_avg_roa,
            f_roundsf(table10.truncated_mean_a,2) as t_avg_roic, f_roundsf(table10.truncated_weighted_mean_a,2) as tw_avg_roic,
            f_roundsf(table11.truncated_mean_a,2) as t_avg_ae, f_roundsf(table11.truncated_weighted_mean_a,2) as tw_avg_ae,
            round(table13.truncated_mean_a,3) as t_avg_ebitev, round(table13.truncated_weighted_mean_a,3) as tw_avg_ebitev

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
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year
            and f.data <= """+ str(TruncationLookup["DividendPayoutRatioPlus"]) + """ and f.data >= """+ str(TruncationLookup["DividendPayoutRatioMinus"]) + """             
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
            where w2.fieldid = 30004 -- Net Debt Paydown Yield
            group by w2.fieldid, w2.year
            ) stdevTable
            join (
            select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

            from wsfactorsubset w1
            join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
            join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
            where w2.fieldid = 30004 -- Net Debt Paydown Yield
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year 
            and f.data <= """+ str(TruncationLookup["NetDebtPaydownYieldPlus"]) + """ and f.data >= """+ str(TruncationLookup["NetDebtPaydownYieldMinus"]) + """
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
            ) f on f.fieldid = stdevTable.fieldid 
            and f.data <= """+ str(TruncationLookup["TotalAssetTurnoverPlus"]) + """ and f.data >= """+ str(TruncationLookup["TotalAssetTurnoverMinus"]) + """
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
            where w2.fieldid = 30007 -- Gross Profit Margin
            group by w2.fieldid, w2.year
            ) stdevTable
            join (
            select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

            from wsfactorsubset w1
            join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
            join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
            where w2.fieldid = 30007 -- Gross Profit Margin
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year
            and f.data <= """+ str(TruncationLookup["GrossProfitMarginPlus"]) + """ and f.data >= """+ str(TruncationLookup["GrossProfitMarginMinus"]) + """ 
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
            where w2.fieldid = 30006 -- Gross Income over Assets
            group by w2.fieldid, w2.year
            ) stdevTable
            join (
            select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

            from wsfactorsubset w1
            join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
            join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
            where w2.fieldid = 30006 -- Gross Profit over Assets
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year 
            and f.data <= """+ str(TruncationLookup["GrossProfitOverAssetsPlus"]) + """ and f.data >= """+ str(TruncationLookup["GrossProfitOverAssetsMinus"]) + """ 
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
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year 
            and f.data <= """+ str(TruncationLookup["OperatingProfitMarginPlus"]) + """ and f.data >= """+ str(TruncationLookup["OperatingProfitMarginMinus"]) + """ 
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
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year 
            and f.data <= """+ str(TruncationLookup["ReturnOnAssetsPlus"]) + """ and f.data >= """+ str(TruncationLookup["ReturnOnAssetsMinus"]) + """ 
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
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year 
            and f.data <= """+ str(TruncationLookup["ReturnOnInvestedCapitalPlus"]) + """ and f.data >= """+ str(TruncationLookup["ReturnOnInvestedCapitalMinus"]) + """
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
            where w2.fieldid = 30003 -- Assets/Equity
            group by w2.fieldid, w2.year
            ) stdevTable
            join (
            select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

            from wsfactorsubset w1
            join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
            join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
            where w2.fieldid = 30003 -- Assets/Equity
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year 
             and f.data <= """+ str(TruncationLookup["AssetsOverEquityPlus"]) + """ and f.data >= """+ str(TruncationLookup["AssetsOverEquityMinus"]) + """             
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

            left join (
            select k.year, avg(k.data) as truncated_mean_a, SUM(k.data*k.mcap_data)/SUM(case when k.data is not null then k.mcap_data else 0 end) as truncated_weighted_mean_a from
            (select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from (
            select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
            from wsfactorsubset w1
            join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
            join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
            where w2.fieldid = 30002 -- EBIT/EV
            group by w2.fieldid, w2.year
            ) stdevTable
            join (
            select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

            from wsfactorsubset w1
            join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
            join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
            where w2.fieldid = 30002 -- EBIT/EV
            ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year
            and f.data <= """+ str(TruncationLookup["EBITOverEVPlus"]) + """ and f.data >= """+ str(TruncationLookup["EBITOverEVMinus"]) + """ 
            ) k
            group by k.year
            ) table13 on table1.year = table13.year

            order by year asc
            """

    return string



def stringTruncationDenom(s): 
    
    string = """
    set statement_timeout to 1200000;

    select k.year, count(k.data) as count_noweight, sum(k.mcap_data) as count_weight from
    (
	    select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from 
	    (
		    select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
		    from wsfactorsubset w1
		    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
		    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
		    where w2.fieldid = """+ str(s) + """
		    and w2.year >= 1980 
		    group by w2.fieldid, w2.year
	    ) stdevTable
	    join 
	    (
		    select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

		    from wsfactorsubset w1
		    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
		    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
		    where w2.fieldid = """+ str(s) + """
		    and w2.year >= 1980 
	    ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year 
    ) k
    group by k.year
    order by k.year asc
    """

    return string



def stringTruncationNum(s):

    if (s == 9504):
        truncationP = TruncationLookup["DividendPayoutRatioPlus"]
        truncationM = TruncationLookup["DividendPayoutRatioMinus"]

    if (s == 30007):
        truncationP = TruncationLookup["GrossProfitMarginPlus"]
        truncationM = TruncationLookup["GrossProfitMarginMinus"]

    if (s == 8316):
        truncationP = TruncationLookup["OperatingProfitMarginPlus"]
        truncationM = TruncationLookup["OperatingProfitMarginMinus"]

    if (s == 30006):
        truncationP = TruncationLookup["GrossProfitOverAssetsPlus"]
        truncationM = TruncationLookup["GrossProfitOverAssetsMinus"]

    if (s == 30002):
        truncationP = TruncationLookup["EBITOverEVPlus"]
        truncationM = TruncationLookup["EBITOverEVMinus"]

    if (s == 30004):
        truncationP = TruncationLookup["NetDebtPaydownYieldPlus"]
        truncationM = TruncationLookup["NetDebtPaydownYieldMinus"]

    if (s == 8401):
        truncationP = TruncationLookup["TotalAssetTurnoverPlus"]
        truncationM = TruncationLookup["TotalAssetTurnoverMinus"]

    if (s == 8326):
        truncationP = TruncationLookup["ReturnOnAssetsPlus"]
        truncationM = TruncationLookup["ReturnOnAssetsMinus"]

    if (s == 8376):
        truncationP = TruncationLookup["ReturnOnInvestedCapitalPlus"]
        truncationM = TruncationLookup["ReturnOnInvestedCapitalMinus"]

    if (s == 30003):
        truncationP = TruncationLookup["AssetsOverEquityPlus"]
        truncationM = TruncationLookup["AssetsOverEquityMinus"]


    string = """
    set statement_timeout to 1200000;
    select k.year, count(k.data)*100 as count_noweight, sum(k.mcap_data)*100 as count_weight from
    (
	    select f.year, f.data, f.mcap_data, stdevTable.ThreeSigP, stdevTable.ThreeSigM from 
	    (
		    select w2.fieldid, w2.year, (avg(w2.data)+3*STDDEV(w2.data)) as ThreeSigP, (avg(w2.data)-3*STDDEV(w2.data)) as ThreeSigM
		    from wsfactorsubset w1
		    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
		    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
		    where w2.fieldid = """+ str(s) + """
		    and w2.year >= 1980 
            and w2.data <= """+ str(truncationP) + """ 
            and w2.data >= """+ str(truncationM) + """ 
		    group by w2.fieldid, w2.year
	    ) stdevTable
	    join 
	    (
		    select w2.data, w2.fieldid, w2.year, w2.wscode, w3.data as mcap_data

		    from wsfactorsubset w1
		    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
		    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
		    where w2.fieldid = """+ str(s) + """
		    and w2.year >= 1980 
	    ) f on f.fieldid = stdevTable.fieldid and f.year = stdevTable.year and (f.data > stdevTable.ThreeSigP or f.data < stdevTable.ThreeSigM) 

    ) k
    group by k.year
    order by k.year asc
    """

    return string


def getPercentiles(s):
    
    string = """
    set statement_timeout to 1200000;
    select
    p.year, 
    round(a.num,3) as Per0_1,
    round(b.num,3) as Per1,
    round(c.num,3) as Per5,
    round(d.num,3) as Per25,
    round(e.num,3) as Per50,
    round(f.num,3) as Per75,
    round(g.num,3) as Per95,
    round(h.num,3) as Per99,
    round(i.num,3) as Per999

    from (
    select year, count(data) as num
    from wsfactorsubset
    where fieldid = 5055
    group by year
    ) p

    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.001) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) a on a.year=p.year

    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.01) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) b on b.year=p.year


    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.05) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) c on c.year=p.year

    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.25) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) d on d.year=p.year

    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.5) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) e on e.year=p.year

    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.75) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) f on f.year=p.year


    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.95) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) g on g.year=p.year


    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.99) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) h on h.year=p.year

    left join (
    select distinct w2.fieldid, w2.year, 
    percentile_disc(0.999) within group (order by w2.data)   
    over(partition by w2.year) as num 
    from wsfactorsubset w1
    join wsfactorsubset w2 on w1.wscode = w2.wscode and w1.year = w2.year and w1.fieldid = 5055
    join wsfactorsubset w3 on w1.wscode = w3.wscode and w1.year = w3.year and w3.fieldid = 7210
    where w2.fieldid = """+ str(s) + """
    group by w2.year, w2.fieldid, w2.data
    ) i on i.year=p.year

    order by p.year asc;
    """ 

    return string

import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import SQL as sqlquery
import string


def getCoverageCountry(year,threshold,engine):
 
    df = pd.read_sql_query(sqlquery.stringCountryCoverage,engine)

    print("Year \t Country \t\t Coverage")

    for row in df.itertuples():
        coverage = row.count_gi/row.count_market

        if (coverage <= threshold) and (row.year >= year):
            print("%i \t %s \t\t %.2f"  % (row.year,row.country,coverage))



def makeHeatMapCountry(engine):

        df = pd.read_sql_query(sqlquery.stringCountryCoverage,engine)

        Plot = go.Heatmap(
        x = df.country,
        y = df.year,
         z=round(df.count_gi/df.count_market,2)
        )
        
        layout = go.Layout(
            title='Coverage per country (Gross Income)'
        )

        fig = go.Figure(data=[Plot], layout=layout)
        py.iplot(fig, filename='CoverageCountryHeatmap')

def makeCoveragePlot(engine):

            df = pd.read_sql_query(sqlquery.stringCoverage, engine)

 
            DividendPayoutRatio = go.Scatter(
            x = df.year,
            y = df.count_dpr/df.count_market,
            mode = 'lines',
            name = 'Dividend Payout Ratio'   )
            EBIT = go.Scatter(
            x = df.year,
            y = df.count_ebit/df.count_market,
            mode = 'lines',
            name = 'EBIT'   
            )
            EV = go.Scatter(
            x = df.year,
            y = df.count_ev/df.count_market,
            mode = 'lines',
            name = 'EV'   
            )
            NetDebtPaydownYield = go.Scatter(
            x = df.year,
            y = df.count_ndpy/df.count_market,
            mode = 'lines',
            name = 'Net Debt Paydown Yield'   
            )
            TotalAssetTurnover = go.Scatter(
            x = df.year,
            y = df.count_tat/df.count_market,
            mode = 'lines',
            name = 'Total Asset Turnover'   
            )
            GrossProfitMargin = go.Scatter(
            x = df.year,
            y = df.count_gpm/df.count_market,
            mode = 'lines',
            name = ' Gross Profit Margin'   
            )
            GrossIncome = go.Scatter(
            x = df.year,
            y = df.count_gi/df.count_market,
            mode = 'lines',
            name = 'Gross Income'   
            )
            OperatingProfitMargin = go.Scatter(
            x = df.year,
            y = df.count_opm/df.count_market,
            mode = 'lines',
            name = 'Operating Profit Margin'   
            )
            ReturnOnAssets = go.Scatter(
            x = df.year,
            y = df.count_roa/df.count_market,
            mode = 'lines',
            name = 'Return on Assets'   
            )
            ReturnOnInvestedCapital = go.Scatter(
            x = df.year,
            y = df.count_roic/df.count_market,
            mode = 'lines',
            name = 'Return on Invested Capital'   
            )
            AssetsOverEquity = go.Scatter(
            x = df.year,
            y = df.count_ae/df.count_market,
            mode = 'lines',
            name = 'Assets/Equity'   
            )

            data = [DividendPayoutRatio,EBIT,EV,NetDebtPaydownYield,TotalAssetTurnover,
                GrossProfitMargin,GrossIncome,OperatingProfitMargin,
                ReturnOnAssets,ReturnOnInvestedCapital,AssetsOverEquity]

            layout = go.Layout(
            title='Total coverage',
                xaxis=dict( title = 'Year'), 
                yaxis=dict( title = 'Coverage', range=[0, 1.0] )
    
            )

            fig = go.Figure(data=data, layout=layout)
            py.iplot(fig, filename='Coverage3')


def makeCoveragePlotNew(engine):

            df = pd.read_sql_query(sqlquery.stringCoverageWeighted, engine)
            
            factorNames = ['DividendPayoutRatio','EBIT','EV','NetDebtPaydownYield','TotalAssetTurnover',
                            'GrossProfitMargin','GrossIncome','OperatingProfitMargin',
                            'ReturnOnAssets','ReturnOnInvestedCapital','AssetsOverEquity']

            factorIDs = [9504,18191,18100,3255,8401,8306,1100,8316,8326,8376,2999]

            n = len(factorIDs)

            arrayOfFactors = []

            for i in range(n):
                                           
                temp = go.Scatter(
                x = df[df['fieldid'] == factorIDs[i]].year,
                y = df[df['fieldid'] == factorIDs[i]].equalwgtcoverage,
                mode = 'lines',
                name = factorNames[i] 
                ) 
                                              
                arrayOfFactors.append(temp)
                
         
            layout = go.Layout(
            title='Total coverage',
                xaxis=dict( title = 'Year'), 
                yaxis=dict( title = 'Coverage', range=[0, 1.0])
            )

            fig = go.Figure(data=arrayOfFactors, layout=layout)
            py.iplot(fig, filename='Coverage3')


def makePlotAvg(engine):

            df = pd.read_sql_query(sqlquery.stringMean, engine)
            #df = pd.read_sql_query(sqlquery.stringMedian, engine)

            DividendPayoutRatio = go.Scatter(
            x = df.year,
            y = df.avg_dpr,
            mode = 'lines',
            name = 'Dividend Payout Ratio'   )
            EBIT = go.Scatter(
            x = df.year,
            y = df.avg_ebit,
            mode = 'lines',
            name = 'EBIT'   
            )
            EV = go.Scatter(
            x = df.year,
            y = df.avg_ev,
            mode = 'lines',
            name = 'EV'   
            )
            NetDebtPaydownYield = go.Scatter(
            x = df.year,
            y = df.avg_ndpy,
            mode = 'lines',
            name = 'Net Debt Paydown Yield'   
            )
            TotalAssetTurnover = go.Scatter(
            x = df.year,
            y = df.avg_tat,
            mode = 'lines',
            name = 'Total Asset Turnover'   
            )
            GrossProfitMargin = go.Scatter(
            x = df.year,
            y = df.avg_gpm,
            mode = 'lines',
            name = ' Gross Profit Margin'   
            )
            GrossIncome = go.Scatter(
            x = df.year,
            y = df.avg_gi,
            mode = 'lines',
            name = 'Gross Income'   
            )
            OperatingProfitMargin = go.Scatter(
            x = df.year,
            y = df.avg_opm,
            mode = 'lines',
            name = 'Operating Profit Margin'   
            )
            ReturnOnAssets = go.Scatter(
            x = df.year,
            y = df.avg_roa,
            mode = 'lines',
            name = 'Return on Assets'   
            )
            ReturnOnInvestedCapital = go.Scatter(
            x = df.year,
            y = df.avg_roic,
            mode = 'lines',
            name = 'Return on Invested Capital'   
            )
            AssetsOverEquity = go.Scatter(
            x = df.year,
            y = df.avg_ae,
            mode = 'lines',
            name = 'Assets/Equity'   
            )

            data = [DividendPayoutRatio,EBIT,EV,NetDebtPaydownYield,TotalAssetTurnover,
                GrossProfitMargin,GrossIncome,OperatingProfitMargin,
                ReturnOnAssets,ReturnOnInvestedCapital,AssetsOverEquity]

            layout = go.Layout(
            #title='Total coverage',
                xaxis=dict( title = 'Year'), 
                yaxis=dict( title = 'Mean factor value')
                #yaxis=dict( title = 'Median factor value')
            )

            fig = go.Figure(data=data, layout=layout)
            py.iplot(fig, filename='MeanFactorValue2')
            #py.iplot(fig, filename='MedianFactorValue')

def makeBoxPlot(engine):

            df = pd.read_sql_query(sqlquery.stringBoxSmall, engine)
            df2 = pd.read_sql_query(sqlquery.stringMean, engine)
                    
            years = [1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,
                     1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]
            n = len(years)
            
            arrayOfFactors = []

            df.plot.box()

            for i in range(n):
                                           
                temp = go.Box(
           
                x = df[df['year'] == years[i]].year,
                y = df[df['year'] == years[i]].data,
                showlegend=False,
            #    name = 'Gross Income',
                boxpoints= False,                    
                marker=dict(
                color='orange'
                ),
                #boxmean='sd' 
                ) 
                                              
                arrayOfFactors.append(temp)
            
            arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_ae, mode = 'lines', name = 'Mean', marker=dict(color='black')))

            factorName = 'Assets Equity Box'

            layout = go.Layout(
            title= factorName,
                xaxis=dict( title = 'Year'), 
                yaxis=dict( title = 'Factor val.', range=[0, 130000000000.]),
                #boxmode='group',
                showlegend=False 
               )

            fig = go.Figure(data=arrayOfFactors, layout=layout)
            py.iplot(fig, filename=factorName)





def makeBoxPlotNoTruncation(engine, factorval):

            df = pd.read_sql_query(sqlquery.stringBoxSmall(factorval), engine)
            df2 = pd.read_sql_query(sqlquery.stringMeanWeighted, engine)
                    
            years = [1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,
                     1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,
                     2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,
                     2010,2011,2012,2013,2014,2015,2016]

            n = len(years)
            
            arrayOfFactors = []


            for i in range(n):
                                                         
                temp = go.Box(
 
                x = df[df['year'] == years[i]].year,
                y = df[df['year'] == years[i]].data,
                showlegend=False,
                boxpoints= False,                    
                marker=dict(
                color='orange'
                ),
                ) 
                                              
                arrayOfFactors.append(temp)
            
           
            ymax = 0

            if (factorval == 9504):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_dpr, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_dpr, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Dividend Payout Ratio'
                ymax = 120

            if (factorval == 18191):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_ebit, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_ebit, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'EBIT'
                ymax = 30E+9

            if (factorval == 18100):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_ev, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_ev, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'EV'
                ymax = 750E+9

            if (factorval == 3255):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_ndpy, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_ndpy, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Net Debt Paydown Yield'
                ymax = 300E+9
 
            if (factorval == 8401):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_tat, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_tat, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Total Asset Turnover'
                ymax = 50

            if (factorval == 8306):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_gpm, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_gpm, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Gross Profit Margin'
                ymax = 850

            if (factorval == 1100):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_gi, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_gi, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Gross Income'
                ymax = 150E+9

            if (factorval == 8316):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_opm, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_opm, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Operating Profit Margin'
                ymax = 2600

            if (factorval == 8326):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_roa, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_roa, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Return on Assets'
                ymax = 2600

            if (factorval == 8376):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_roic, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_roic, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Return on Invested Capital'
                ymax = 130
                                                                                                                                           
            if (factorval == 2999):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_a, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_a, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Assets'
                ymax = 1E+12

            if (factorval == 3501):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.avg_e, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.mcapweightedavg_e, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Equities'
                ymax = 0.4E+12


            layout = go.Layout(
            title= factorName,
                xaxis=dict( title = 'Year'), 
                yaxis=dict( title = 'Factor val.', range=[0, ymax]),
                showlegend=False 
               )

            fig = go.Figure(data=arrayOfFactors, layout=layout)
            py.iplot(fig, filename=factorName)


def makeBoxPlotTruncation(engine, factorval):

            
            df = pd.read_sql_query(sqlquery.stringBoxSmallTruncated(factorval), engine)
            df2 = pd.read_sql_query(sqlquery.stringMeanWeightedTruncated, engine)
      
           
            years = [1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,
                     1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,
                     2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,
                     2010,2011,2012,2013,2014,2015,2016]

            n = len(years)
            
            arrayOfFactors = []


            for i in range(n):
                                                                    
                temp = go.Box(
 
                x = df[df['year'] == years[i]].year,
                y = df[(df['data'] < df['threesigp']) & (df['data'] > df['threesigm']) & (df['year'] == years[i])].data,
                showlegend=False,
                boxpoints= False,                    
                marker=dict(
                color='orange'
                ),
                ) 
                                              
                arrayOfFactors.append(temp)
            

            ymax = 0

            if (factorval == 9504):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_dpr, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_dpr, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Dividend Payout Ratio (Truncated)'
                ymax = 120

            if (factorval == 18191):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_ebit, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_ebit, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'EBIT (Truncated)'
                ymax = 30E+9

            if (factorval == 18100):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_ev, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_ev, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'EV (Truncated)'
                ymax = 750E+9

            if (factorval == 3255):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_ndpy, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_ndpy, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Net Debt Paydown Yield (Truncated)'
                ymax = 300E+9

            if (factorval == 8401):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_tat, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_tat, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Total Asset Turnover (Truncated)'
                ymax = 50

            if (factorval == 8306):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_gpm, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_gpm, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Gross Profit Margin (Truncated)'
                ymax = 850

            if (factorval == 1100):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_gi, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_gi, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Gross Income (Truncated)'
                ymax = 150E+9

            if (factorval == 8316):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_opm, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_opm, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Operating Profit Margin (Truncated)'
                ymax = 2600

            if (factorval == 8326):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_roa, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_roa, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Return on Assets (Truncated)'
                ymax = 2600

            if (factorval == 8376):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_roic, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_roic, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Return on Invested Capital (Truncated)'
                ymax = 130
                                                                                                                                            
            if (factorval == 2999):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_a, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_a, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Assets (Truncated)'
                ymax = 1E+12

            if (factorval == 3501):
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.t_avg_e, mode = 'lines', name = 'Eq. weighted Mean', marker=dict(color='black')))
                arrayOfFactors.append( go.Scatter( x = df2.year, y = df2.tw_avg_e, mode = 'lines', name = 'MCap. weighted Mean', marker=dict(color='blue')))
                factorName = 'Equities (Truncated)'
                ymax = 0.4E+12


            layout = go.Layout(
            title= factorName,
                xaxis=dict( title = 'Year'), 
                yaxis=dict( title = 'Factor val.', range=[0, ymax]),
                showlegend=False 
               )

            fig = go.Figure(data=arrayOfFactors, layout=layout)
            py.iplot(fig, filename=factorName)


def makeTest(engine):

    df = pd.read_sql_query(sqlquery.stringTEST, engine)
    p = df.pivot(index='Item', columns=1980, values=df.data)
    print(d)

    #N = 100
    #y_vals = {}
    ##for i in range() list(string.ascii_uppercase):
    #     y_vals[letter] = np.random.randn(N)+(3*np.random.randn())
        
    ##df = pd.DataFrame(y_vals)
    #df = pd.read_sql_query(sqlquery.stringTEST, engine)
    #df.head()

    #data = []

    #for col in df.columns:
    #    data.append(  go.Box( y=df[col], name=col, showlegend=False ) )

    #data.append( go.Scatter( x = df.columns, y = df.mean(), mode='lines', name='mean' ) )

    ## IPython notebook
    ## py.iplot(data, filename='pandas-box-plot')

    #url = py.plot(data, filename='pandas-box-plot')

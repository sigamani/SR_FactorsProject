import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import SQL2 as sqlquery
import string

from plotly.tools import FigureFactory as FF


def makeCoveragePlot(engine):

    df = pd.read_sql_query(sqlquery.stringCoverage(), engine)

    factorIDs = [9504,18191,18100,3255,8401,8306,30005,8316,8326,8376,2999,3501]

    factorNames = ['Dividend Payout Ratio','EBIT','EV','Net Debt Paydown Yield','Total Asset Turnover',
                   'Gross Profit Margin','Gross Income','Operating Profit Margin',
                   'Return On Assets','Return On Invested Capital','Assets','Equity']
    
    n = len(factorIDs)
    arrayOfFactors = []

    for i in range(n):
                                             
        temp = go.Scatter(
        x = df[df['fieldid'] == factorIDs[i]].year,
        y = df[df['fieldid'] == factorIDs[i]].mcapwgtcoverage,
        mode = 'lines',
        name = factorNames[i] 
        ) 
        arrayOfFactors.append(temp)
      
                     
    layout = go.Layout(
    title='Total coverage (market cap. weighted)',
    xaxis=dict( title = 'Year'), 
    yaxis=dict( title = 'Coverage', range=[0, 1.0])
    )

    fig = go.Figure(data=arrayOfFactors, layout=layout)
    py.iplot(fig, filename='Coverage4')






def makeBoxPlot(engine, factorval, isTruncated):

    if (isTruncated):
        df = pd.read_sql_query(sqlquery.stringDataforOneFactorTruncated(factorval), engine)
        dfMean = pd.read_sql_query(sqlquery.stringMeanWeightedTruncated(factorval), engine)  
    else:
        df = pd.read_sql_query(sqlquery.stringDataforOneFactor(factorval), engine)
        dfMean = pd.read_sql_query(sqlquery.stringMeanWeighted, engine)

    years = [1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,
             1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,
             2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,
             2010,2011,2012,2013,2014,2015,2016]

    n = len(years)
    
    listOfFactors = []


    if (factorval == 9504):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_dpr, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 100
        ymin = 0.0
            
        if isTruncated:
            factorName = 'Dividend Payout Ratio (Truncated)'
        else:
            factorName = 'Dividend Payout Ratio (Non-truncated)'


    if (factorval == 30007):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_gpm, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 100
        ymin = 0.0
            
        if isTruncated:
            factorName = 'Gross Profit Margin (Truncated)'
        else:
            factorName = 'Gross Profit Margin (Non-truncated)'


    if (factorval == 8316):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_opm, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 80
        ymin = -80
            
        if isTruncated:
            factorName = 'Operating Profit Margin (Truncated)'
        else:
            factorName = 'Operating Profit Margin (Non-truncated)'

    if (factorval == 30006):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_gi, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymin = -50
        ymax = 150
            
        if isTruncated:
            factorName = 'Gross Profit over Assets (Truncated)'
        else:
            factorName = 'Gross Profit over Assets (Non-truncated)'


    if (factorval == 30002):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_ebitev, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 0.5
        ymin = 0
            
        if isTruncated:
            factorName = 'EBIT over EV (Truncated)'
        else:
            factorName = 'EBIT over EV (Non-truncated)'


    if (factorval == 30004):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_ndpy, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 100
        ymin = -100
            
        if isTruncated:
            factorName = 'Net Debt Paydown Yield (Truncated)'
        else:
            factorName = 'Net Debt Paydown Yield (Non-truncated)'

    if (factorval == 8401):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_tat, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 5
        ymin = 0
            
        if isTruncated:
            factorName = 'Total Asset Turnover (Truncated)'
        else:
            factorName = 'Total Asset Turnover (Non-truncated)'

    if (factorval == 8326):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_roa, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 30
        ymin = -30
            
        if isTruncated:
            factorName = 'Return on Assets (Truncated)'
        else:
            factorName = 'Return on Assets (Non-truncated)'

    if (factorval == 8376):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_roic, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 30
        ymin = -30
            
        if isTruncated:
            factorName = 'Return on Invested Capital (Truncated)'
        else:
            factorName = 'Return on Invested Capital (Non-truncated)'

    if (factorval == 30003):
        listOfFactors.append( go.Scatter( x = dfMean.year, y = dfMean.tw_avg_ae, mode = 'lines', name = 'Weighted Mean', marker=dict(color='blue')))
        ymax = 50
        ymin = 0
            
        if isTruncated:
            factorName = 'Assets over Equity (Truncated)'
        else:
            factorName = 'Assets over Equity (Non-truncated)'


    for i in range(n):
         
        if isTruncated:
            y1 = df[(df['data'] <= df['threesigp']) & (df['data'] >= df['threesigm']) & (df['year'] == years[i])]
            #y1 = df[df['year'] == years[i]]
        else: 
            y1 = df[df['year'] == years[i]]
                                                                            
        temp = go.Box(
        x = df[df['year'] == years[i]].year,
        y = y1.data, 
        showlegend=False,
        boxpoints= False, 
        boxmean='sd',             
        marker=dict(
        color='rgba(207, 114, 255, 0.5)'
        ),
        ) 
                                              
        listOfFactors.append(temp)
                   

    layout = go.Layout(
    title= factorName,
        xaxis=dict( title = 'Year'), 
        yaxis=dict( title = 'Factor value', range=[ymin, ymax]),
        showlegend=False 
        )

    fig = go.Figure(data=listOfFactors, layout=layout)
    py.plot(fig, filename=factorName)



def makeTruncationPlot(engine,factorval): 

    dfNum = pd.read_sql_query(sqlquery.stringTruncationNum(factorval), engine)
    dfDenom = pd.read_sql_query(sqlquery.stringTruncationDenom(factorval), engine)

    PLOT = go.Scatter(
    x = dfNum.year,
    y = dfNum.count_weight/dfDenom.count_weight,
    mode = 'lines',
    name = 'MCap. weight'   )

    PLOT2 = go.Scatter(
    x = dfNum.year,
    y = dfNum.count_noweight/dfDenom.count_noweight,
    mode = 'lines',
    name = 'Equal weight'   )

    data = [PLOT, PLOT2]

    layout = go.Layout(
    title='Truncation',
    xaxis=dict( title = 'Year'), 
    yaxis=dict( title = '% Removed', range=[0, 5.] )    
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=str(factorval)+'-truncation')


def makePercentilePlot(engine,factorval):
    
    df = pd.read_sql_query(sqlquery.getPercentiles(factorval), engine)

    if (factorval == 30002):
        ymax = 2
        ymin = -5
        factorName = 'EBIT over EV'

    if (factorval == 9504):
        ymax = 100
        ymin = 0
        factorName = 'Dividend Payout Ratio'

    if (factorval == 30007):
        ymax = 100
        ymin = 0
        factorName = 'Gross Profit Margin'
    
    if (factorval == 8316):
        ymax = 100
        ymin = 0
        factorName = 'Operating Profit Margin'

    if (factorval == 30006):
        ymax = 150
        ymin = -60
        factorName = 'Gross Profit over Assets'

    if (factorval == 30004):
        ymax = 5000
        ymin = -1500
        factorName = 'Net debt paydown yield'

    if (factorval == 8401):
        ymax = 5
        ymin = 0
        factorName = 'Total asset turnover'

    if (factorval == 8326):
        ymax = 50
        ymin = -600
        factorName = 'Return on Assets'

    if (factorval == 8376):
        ymax = 50
        ymin = -400
        factorName = 'Return on Invested Capital'

    if (factorval == 30003):
        ymax = 50
        ymin = 0
        factorName = 'Assets over Equity'

    P01 = go.Scatter(
    x = df.year,
    y = df.per0_1,
    line=dict(
    width = 2, 
    color='rgb(255, 0, 0)',
    dash = 'dash'),
    name = '0.1%'   )

    P1 = go.Scatter(
    x = df.year,
    y = df.per1,
    line=dict(
    color='rgb(200, 0, 0)',
    dash = 'dot'),
    name = '1%'   )

    P5 = go.Scatter(
    x = df.year,
    y = df.per5,
    line=dict(
    color='rgb(150, 0, 0)',
    dash = 'dot'),
    name = '5%'   )

    P25 = go.Scatter(
    x = df.year,
    y = df.per25,
    marker=dict(
    color='rgb(50, 0, 0)'
    ),
    mode = 'lines',
    name = '25%'   )

    P50 = go.Scatter(
    x = df.year,
    y = df.per50,
    marker=dict(
    color='black'
    ),
    mode = 'lines',
    name = '50%'   )

    P75 = go.Scatter(
    x = df.year,
    y = df.per75,
    marker=dict(
    color='rgb(50, 0, 0)'
    ),
    mode = 'lines',
    name = '75%'   )

    P95 = go.Scatter(
    x = df.year,
    y = df.per95,
    line=dict(
    color='rgb(150, 0, 0)',
    dash = 'dot'),
    name = '95%'   )

    P99 = go.Scatter(
    x = df.year,
    y = df.per99,
    line=dict(
    color='rgb(200, 0, 0)',
    dash = 'dot'
    ),
    name = '99%'   )

    P999 = go.Scatter(
    x = df.year,
    y = df.per999,
    line=dict(
    width = 2, 
    color='rgb(255, 0, 0)',
    dash = 'dash'
    ),
    name = '99.9%'   )

    data = [P01,P1,P5,P25,P50,P75,P95,P99,P999]

    layout = go.Layout(
    title=factorName,
    xaxis=dict( title = 'Year'), 
    yaxis=dict( title = 'Factor value', range=[ymin, ymax] )    
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=factorName+"-Percentiles")



def makeCorrelationByFactorVal(engine):

    df = pd.read_sql_query(string2, engine)
    corr = df.corr(method='spearman')

    fig = FF.create_annotated_heatmap(x = list(corr.columns.values), y = list(corr.columns.values), z=np.round(corr.values,2))


    fig['layout'].update(
        title='Correlations by factor val. (Dec 2015)',
        xaxis=dict(ticks='', ticksuffix='', side='bottom'),
        width=450,
        height=300,
        margin=go.Margin(
        l=180,
        r=80,
        b=100,
        t=100,
        pad=4
        ),
        autosize=False
    )

    py.iplot(fig, filename='Correlations')


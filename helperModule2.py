import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import csv
import xlrd
import xlwt
import os
import scipy.stats as st
from plotly.tools import FigureFactory as FF
from xlutils.copy import copy



def getMarketsAnalyzerOutput(s):


    dir = r"C:\\Users\\michael\\Desktop\\Test_output\\"

    factors = ['Book Value', 'Div Pay Ratio (N)', 'Div Yld', 'Engs Yld', 'Cfl Yld',
               'Sales to Pr', 'EBIT to EV (N)', 'EBITDA to Pr', 'RoA (N)', 'RoE', 'ROIC (N)',
               'Sustainable GR', 'Asset Turnover (N)', 'Gross Prof to Assts (N)', 'Sales Gr', 
               'Inc to Sales', 'Op Prof Marg (N)', 'Gross Prof Marg (N)', 'Ass to Eq (N)']
  
    countries = ['UNITED STATES', 'CHINA', 'JAPAN', 'UNITED KINGDOM', 'SWITZERLAND', 'GERMANY', 'HONG KONG',
                 'FRANCE', 'CANADA', 'AUSTRALIA', 'NETHERLANDS', 'SOUTH AFRICA', 'SINGAPORE']


    if (s == 'Return_10Year'):
        plottitle = '10 Year Return (%)'
        y=21
        x=4
        rounddp=0
        percent=100
    if (s == 'Return_1Year'):
        plottitle = '12 Month Return (%)'
        y=22
        x=4
        rounddp=0
        percent=100
    if (s == 'TrackingError'):
        plottitle = 'Tracking Error (%)'
        y=21
        x=6
        rounddp=0
        percent=100
    if (s == 'TrackingError_2Year'):
        plottitle = '2 Year Tracking Error (%)'
        y=22
        x=6
        rounddp=0
        percent=100
    if (s == 'StdDev'):
        plottitle = 'Standard Deviation'
        y=23
        x=6
        rounddp=3
        percent=1
    if (s == 'StdDev_2Year'):
        plottitle = '2 Year Standard Deviation'
        y=24
        x=6
        rounddp=3
        percent=1
    if (s == 'StyleBeta'):
        plottitle = 'Beta'
        y=25
        x=6
        rounddp=2
        percent=1
    if (s == 'Regularity_3Month'):
        plottitle = '3 Month Regularity'
        y=21
        x=8
        rounddp=3
        percent=1
    if (s == 'Regularity_6Month'):
        plottitle = '6 Month Regularity'
        y=22
        x=8
        rounddp=3
        percent=1
    if (s == 'Regularity_12Month'):
        plottitle = '12 Month Regularity'
        y=23
        x=8
        rounddp=3
        percent=1
    if (s == 'Identity'):
        plottitle = 'Identity (%)'
        y=25
        x=2
        rounddp=0
        percent=100
    if (s == 'Attrib'):
        plottitle = 'Attribution'
        y=23
        x=2
        rounddp=2
        percent=1


    corr = [] 
    for i in range(len(factors)):

            corr.append([])
            for coun in countries:

                factor = factors[i].replace(" (N)","")

                file = dir + "Michael Style 50-100 " + factor + " " + coun + " MC M1 200611 to 201610 Dec.xlsx"
                book=xlrd.open_workbook(file)                         
                sheet=book.sheet_by_name('Style Graph')
                value = sheet.cell_value(y,x)
                corr[i].append(value*percent)


    fig = FF.create_annotated_heatmap(x = countries, y = factors, z=np.round(corr,rounddp))

    fig['layout'].update(
        title=plottitle,
        xaxis=dict(ticks='', ticksuffix='', side='bottom'),
        width=450,
        height=300,
            margin=go.Margin(
            l=180,
            r=50,
            b=100,
            t=100,
            pad=4
            ),
        autosize=False
    )

    py.plot(fig, filename=s)




def changeName(dir, country):

    for filename in os.listdir(dir):
        if (country in filename):

            temp = filename.split(country)[-1].split('MC')[0]
            filename2= filename.replace(temp,' ')
            os.system("move \"" +dir+filename + "\" \"" +dir+ filename2+"\"")
         
    

def getCorrelationOfReturns(country):

    dir = r"C:\\Users\\michael\\Desktop\\Test_output\\"

    factors = ['Book Value', 'Div Pay Ratio (N)', 'Div Yld', 'Engs Yld', 'Cfl Yld',
               'Sales to Pr', 'EBIT to EV (N)', 'EBITDA to Pr', 'RoA (N)', 'RoE', 'ROIC (N)',
               'Sustainable GR', 'Asset Turnover (N)', 'Gross Prof to Assts (N)', 'Sales Gr', 
               'Inc to Sales', 'Op Prof Marg (N)', 'Gross Prof Marg (N)', 'Ass to Eq (N)']

        
    nfactors = len(factors)        
    arr = []

    for j in range(nfactors):    

        factor = factors[j].replace(" (N)","")
        file = dir + "Michael Style 50-100 " + factor + " " + country + " MC M1 200611 to 201610 Dec.xlsx"

        book=xlrd.open_workbook(file)                         
        sheet=book.sheet_by_name('Return Data')

        list = []
        for i in range(5,123):
            value = sheet.cell_value(12,i)
            list.append(value)

        arr.append([])
        arr[j].append(list)
    

    results = []        
    for k in range(nfactors):

        results.append([])
        for l in range(nfactors):
                    
            corr = np.corrcoef(arr[k],arr[l])
            temp = corr[0,1]
            temp2 = round(temp,2)
            results[k].append(temp2)

    fig = FF.create_annotated_heatmap(x = factors, y = factors, z=results)

    fig['layout'].update(
        title=country+' (Correlation)',
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

    py.iplot(fig, filename=country+'-Correlation')


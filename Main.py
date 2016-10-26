import os
import requests
import SQL as sqlquery
import psycopg2
from sqlalchemy import create_engine
import plotly.plotly as py
import helperModule as m
import pypyodbc

py.sign_in('michael.sigamani_sr', '16jtbqurle')

#REDSHIFT CONNECTION
engine = create_engine("postgresql+psycopg2://michael:Enterpr1$e@sr-data.cqwafjoudxie.eu-west-1.redshift.amazonaws.com:5439/worldscope" )

#LOCAL CONNECTION
#engine = pypyodbc.connect('Driver={SQL Server};Server=localhost;Database=WSHistory;')

# 1) Make coverage plot of all 11 factors considered:
#m.makeCoveragePlot(engine)

# 2i) Make heatmap of coverage per country:   
#m.makeHeatMapCountry(engine)

# 2ii) Output country and year where coverage falls below threshold (Start year, < threshold)
#m.getCoverageCountry(1980,0.7,engine)

# 3) Get median factor value per year
#m.makePlotAvg(engine)

# 4) Different method coverage
#m.makeCoveragePlot2(engine)


#m.makeBoxPlotNoTruncation(engine,3501)
m.makeBoxPlotTruncation(engine,3501)

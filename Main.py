import os
import requests
import SQL as sqlquery
import psycopg2
from sqlalchemy import create_engine
import plotly.plotly as py
import helperModule2 as m
import pypyodbc



#py.sign_in('michael.sigamani_sr', '16jtbqurle')
py.sign_in('sigamani1982','lrix3k0xxv')

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

#m.makeBoxPlotNoTruncation(engine,30002)
#m.makeBoxPlotTruncation(engine,30004)


#m.makeBoxPlotTruncation(engine,30002)




# New box plots
#m.makeBoxPlot(engine,8316,False)
#m.makeBoxPlot(engine,8316,True)
m.makeTruncationPlot(engine,8316)


# 5) Make percentile plots
#m.makePercentilePlot(engine, 30007) 

#for n in (9504,30007,8316,30006,30002,30004,8401,8326,8376,30003):
#    print('Making percentile plot %i' % (n))
#    m.makePercentilePlot(engine,n)
        


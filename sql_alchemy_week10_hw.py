#shaheda choudhury 
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

'''
inspector = inspect(engine)
inspector.get_table_names()

columns = inspector.get_columns('measurement')
for x in columns: 
    print(c['name'], c['type'])'''

# Design a query to retrieve the last 12 months of precipitation data and plot the results
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date 1 year ago from the last data point in the database
un_ano = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
precp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

# Save the query results as a Pandas DataFrame and set the index to the date column
precp_df = pd.DataFrame(precp_data)
precp_df = precp_df.set_index('date')

# Sort the dataframe by date
precp_df = precp_df.sort_values(by = ['date'])

# Use Pandas Plotting with Matplotlib to plot the data
prep_graph = precp_df.plot()
plt.title("Precipitation between 8/23/2016 and 8/23/2017")
plt.ylabel("Amount of Precipitation")
plt.xlabel("Date")

#checking for the correct data dates
print(precp_df.tail()) 
print(precp_df.head())

# Use Pandas to calcualte the summary statistics for the precipitation data
stats = precp_df.describe()
print(stats)

# Design a query to show how many stations are available in this dataset?
station_count = session.query(Station.id).count()
print(station_count)

# What are the most active stations? (i.e. what stations have the most rows)?
station_counts = session.query(Station.station, func.count(Measurement.id)).select_from(Measurement).\
    join(Station, Measurement.station == Station.station).group_by(Station.station).\
    order_by(func.count(Measurement.id).desc()).all()

# List the stations and the counts in descending order.
for s in station_counts:
    print(s)

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
low_temp = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').all()
print(low_temp)

high_temp = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').all()
print(high_temp)

avg_temp = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.station == 'USC00519281').all()
print(avg_temp)

# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
station_data = session.query(Measurement.tobs, Measurement.date).\
filter(Measurement.station == 'USC00519281', Measurement.date >= un_ano).all()
station_data

station_d_df = pd.DataFrame(station_data, columns = ['date', 'temps'])
print(station_d_df.head())

station_data_hist = station_d_df.hist(bins = 12)

plt.title("Highest freqency of temp observations")
plt.ylabel("Frequency")
plt.xlabel("Observations count")
display(station_data_hist)


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.

start_date = '2016-08-23'
end_date = '2017-08-23'

trip_avg = calc_temps(start_date, end_date)
print(trip_avg) 

# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

#this plot will not work! 
p1= plt.bar(trip_avg, height = 10, width = .8, yerr=trip_avg)
plt.ylabel('Temps')
plt.title('Trip Avg Temp')
plt.show()

#I can't get this plot to work, I really dislike making charts and graphs on matplotlib and I worked on trying to get this work for a long time(3 weeks) and I'm giving up.


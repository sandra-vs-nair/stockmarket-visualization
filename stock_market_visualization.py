# -----------------------------------------------------------
# Creating a candlestick chart of stock-market data using python.
#
# (C) 2020 Sandra VS Nair, Trivandrum
# email sandravsnair@gmail.com
# -----------------------------------------------------------

from pandas_datareader import data
from bokeh.models.annotations import Title
from bokeh.plotting import figure,show,output_file
import datetime

#The time period for which you need the data.
starttime=datetime.datetime(2018,5,2)
endttime=datetime.datetime(2018,5,20)

#pandas_datareader imports data from a number of online sources.
#Parameters: Stock symbol, Data source, Start time and End time.
stock_data=data.DataReader(name="AAPL", data_source="yahoo", start=starttime, end=endttime)

#Setting properties of the plot.
plot=figure(x_axis_type='datetime',width=1000,height=300)
t = Title()
t.text = 'Candlestick chart'
plot.title = t
plot.grid.grid_line_alpha=0.3

#Twelve horus in milliseconds.
twelve_hours=12*60*60*1000

#Updating status of the stock.
def status_update(open_price,close_price):
    if close_price > open_price:
        value="Increase"
    elif open_price > close_price:
        value="Decrease"
    else:
        value="Equal"
    return value

#Finding mean value of opening price and closing price.
def middle_value(open_price,close_price):
    value=(open_price+close_price)/2 
    return value

#Finding the difference between opening price and closing price.
def height(open_price,close_price):
    value=abs(close_price-open_price)
    return value

#Adding three more columns to the table.
stock_data["Status"]=[status_update(open_price,close_price) for open_price,close_price in zip(stock_data.Open,stock_data.Close)]
stock_data["Middle"]=[middle_value(open_price,close_price) for open_price,close_price in zip(stock_data.Open,stock_data.Close)]
stock_data["Height"]=[height(open_price,close_price) for open_price,close_price in zip(stock_data.Open,stock_data.Close)]
    
#Adding rectangles and segments to the plot
 
#Four mandatory parameters
#1. x-coordinate of central point of rectangles
#2. y-coordinate of central point of rectangles
#3. Width
#4. Height

plot.rect(stock_data.index[stock_data.Status=="Increase"], stock_data.Middle[stock_data.Status=="Increase"], \
          twelve_hours, stock_data.Height[stock_data.Status=="Increase"],fill_color="green",line_color="black")
plot.rect(stock_data.index[stock_data.Status=="Decrease"], stock_data.Middle[stock_data.Status=="Decrease"], \
          twelve_hours,stock_data.Height[stock_data.Status=="Decrease"],fill_color="red",line_color="black")

#Four mandatory parameters
#1. Highest x-coordinate.
#2. Highest y-coordinate.
#3. Lowest x-coordinate.
#4. Lowest y-coordinate.

plot.segment(stock_data.index,stock_data.High,stock_data.index,stock_data.Low,color="black")

#Saving the plot.
output_file("Candlestick.html")

#Displaying the plot.
show(plot)
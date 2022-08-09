import pandas as pd
import os
import matplotlib.pyplot as plt

"""

merge all file in one file
clean data
add columns 
and make tasks:    1) What was the best month for sales?
                   2) What city had the highest number of sales? 
                   3) what time should we display  advertisements to maximize likelihood of customer's buying product?
                   
    finally --> all taks's plot
"""

pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', None)

files = [file for file in os.listdir('./data')]

all_month_data = pd.DataFrame()
for file in files:
    df = pd.read_csv('./data/' + file)
    all_month_data = pd.concat([all_month_data,df])

all_month_data.to_csv('all_data.csv',index=False)

all_data = pd.read_csv('all_data.csv')

all_data['Month'] = all_data['Order Date'].str[:2]

#clean data delete all nan
nan_df = all_data[all_data.isna().any(axis = 1)]
all_data = all_data.dropna(how='all')

#find or and delete it
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']


all_data['Month'] = all_data['Month'].astype('int32')

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'],errors='coerce')
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'],errors='coerce')

#add sales column
all_data['sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

res = all_data.groupby('Month').sum()

#add city column
def get_city(address):
    return address.split(',')[1]


def get_state(address):
    return address.split(',')[2].split(' ')[1]


all_data['Purchase Address'] = all_data['Purchase Address'].astype('str')
all_data['City'] = all_data['Purchase Address'].apply(lambda x:get_city(x) + ' (' + get_state(x) + ')')

#What city had the highest number of sales?

city_res = all_data.groupby('City').sum()

#convert all_data series to_datetime
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

#add hour column
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
hours = [hour for hour,df in all_data.groupby('Hour')]


#advetisement
# plt.plot(hours,all_data.groupby(['Hour']).count())
# plt.xticks(hours)
# plt.xlabel('Hour')
# plt.ylabel('Number of orders')
# plt.grid()
# plt.show()


# best month sales plot
# months = range(1,13)
# plt.bar(months,res['sales'])
# plt.xticks(months)
# plt.ylabel('Sales in USD ($)')
# plt.xlabel('Month number')
# plt.show()

#city plot

# cities = [city for city, df in all_data.groupby('City')]
# plt.bar(cities,city_res['sales'])
# plt.xticks(cities,rotation='vertical',size=8)
# plt.ylabel('Sales in USD ($)')
# plt.xlabel('City Name')
# plt.show()

print(all_data)
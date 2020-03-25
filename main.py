import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date
from datetime import timedelta
import logging
import requests
from datetime import datetime, timedelta
from upload import *

logging.basicConfig(level=logging.WARNING)

# open the CSV file
CONFIRMED_CASES = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

DEATHS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'


def getFormattedDate():
    today = date.today() - timedelta(days=1)
    return today.strftime('%m/%d/%y')


def plot_timeseries_by_country(S, dir, prefix, type_of_data):
    corona_data = pd.read_csv(type_of_data)
    countries = sorted(corona_data['Country/Region'].unique())
    for country in (countries):
        country_data = corona_data[corona_data['Country/Region'] == country]
        # sum all the rows together for each column, and select only the data columns
        by_date = country_data.sum(axis=0).filter(like='/20')
        yesterday_cases = country_data.sum(axis=0).tail(1)[0]
        if yesterday_cases > 0:
            labels = get_x_labels(country_data)

            plt.close()
            fig = plt.figure()
            plt.title('Plot of confirmed cases by date: {}'.format(country))
            plt.figure(figsize=(20, 15))
            plt.plot(by_date)
            plt.xlabel('Dates')
            plt.ylabel('Total Number of Cases')
            plt.xticks(labels, rotation=45)
            plot_name = prefix+country+'.png'
            plt.savefig(os.path.realpath('plots/' + dir) + '/' + plot_name)
            plt.clf()
            upload(S, dir, plot_name, 'COVID 19 ' +
                   dir + ' Cases in ' + country)

def get_x_labels(country_data):
    dates = country_data.filter(like='/20')
    x_labels = dates.columns.values
    labels = []
    idx = 0
    for date in dates:
        if idx % 3 == 0:
            labels.append(date)
        idx += 1
    return labels


S = login()

plot_timeseries_by_country(S,
                           'confirmed', 'COVID_Confirmed_Cases_', CONFIRMED_CASES)
plot_timeseries_by_country(S,
                           'deaths', 'COVID_Deaths_', DEATHS)

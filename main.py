import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date
from datetime import timedelta


# open the CSV file
CONFIRMED_CASES = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

DEATHS = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'

RECOVERED_CASES = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'


def getFormattedDate():
    today = date.today() - timedelta(days=1)
    return today.strftime('%m/%d/%y')


def plot_timeseries_by_country(dir, prefix, type_of_data):
    corona_data = pd.read_csv(type_of_data)
    countries = sorted(corona_data['Country/Region'].unique())
    for country in (countries):
        country_data = corona_data[corona_data['Country/Region'] == country]
        # sum all the rows together for each column, and select only the data columns
        by_date = country_data.sum(axis=0).filter(like='/20')
        yesterday_cases = country_data.sum(axis=0).tail(1)[0]
        if yesterday_cases > 0:
            plt.close()
            fig = plt.figure()
            plt.title('Confirmed cases by date: {}'.format(country))
            plt.plot(by_date)
            plt.savefig(os.path.realpath('plots/' + dir) +
                        '/'+prefix+country+'.png')
            plt.clf()

plot_timeseries_by_country(
    'confirmed', 'COVID_Confirmed_Cases_', CONFIRMED_CASES)
plot_timeseries_by_country(
    'deaths', 'COVID_Deaths_', DEATHS)
plot_timeseries_by_country(
    'recovered', 'COVID_Recovered_', RECOVERED_CASES)

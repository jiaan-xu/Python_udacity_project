import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Get user input on city, month and day to filter the data on.

        User is asked to select a city from a list of three.
        Invalid inputs are handled by asking the user to try again.

        User is then asked to select a month from a list of six.
        Invalid inputs are handled by asking the user to try again.

        User is finally asked to select a day of the week.
        Invalid inputs are handled by asking the user to try again.

    Output: The function returns a string with (city, month, day)
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        try:
            cities = ['chicago', 'new york city', 'washington']
            city = str(input('Please enter the name of a city between chicago, new york city and washington:').lower())
            if city not in cities:
                print('Oopsie, that was not a valid input. Please try again')
                continue
        except:
            print('Oopsie, that was not a valid input. Please try again')
            continue
        else:
            break
    while True:
        try:
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
            month = str(input('Now please enter a month to filter the data to. Enter any month between January and June or enter "all" if you don\'t want to filter by month:').lower())
            if month not in months:
                print('Oopsie, that was not a valid input. Please try again')
                continue
        except:
            print('Oopsie, that was not a valid input. Please try again')
            continue
        else:
            break
    while True:
        try:
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
            day = str(input('Now please enter a day of the week to filter the data to. Enter any day from Monday to Sunday or enter "all" if you don\'t want to filter by day:').lower())
            if day not in days:
                print('Oopsie, that was not a valid input. Please try again')
                continue
        except:
            print('Oopsie, that was not a valid input. Please try again')
            continue
        else:
             break
    print('-'*40)
    return (city, month, day)


def load_data(city, month, day):
    """
    Load the user inputs as filters for the dataframe.

        Args:
            city: the city chose by the user in the get_filters() function
            month: the month chosen by the user in the get_filters() function
            day: the day chose by the user in the get_filters() function

    Output: The function returns a dataframe filtered for the city, month and day chosen
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title()) + 1
        df = df[df['month']== month]
    if day != 'all':
        df = df[df['day_of_week']== day.title()]

    return df


def time_stats(df):
    """
    Get statistical data on popular travel times for bikeshares.

        Args:
            df: the dataframe obtain from the load_data function
    Output: most popular month, most popular day of the week, most popular start hour for bikeshares.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    month = df['Start Time'].dt.month
    print('Most popular month of the year:',month.mode()[0])
    day_of_week = df['Start Time'].dt.weekday_name
    print('Most popular day of the week:', day_of_week.mode()[0])
    hours = df['Start Time'].dt.hour
    print('Most popular hour of the day:', hours.mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Get statistical data on rental stations for bikeshares.

        Args:
            df: filtered dataframe obtain from the loda_data() function
    Output: most popular start and end stations, most popular combination of stations.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print('The most popular Start Station is:', df['Start Station'].mode()[0])
    print('The most popular End Station is:', df['End Station'].mode()[0])
    print('The most popular combination of stations is:', df.groupby(['Start Station', 'End Station']).count().sort_values(by = ['Start Station', 'End Station'], axis=0).iloc[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Get statistical data on trip durations for bikeshares.

        Args:
            df: filtered dataframe obtain from the loda_data() function
    Output: total travel time, average travel time.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    durations=[]
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    for start_time, end_time in zip(df['Start Time'], df['End Time']):
        time_delta = (end_time - start_time)
        duration_sec= time_delta.total_seconds()
        durations.append(int(duration_sec))
    print('The total travel time was:', sum(durations), 'seconds')
    print('The average travel time was:', sum(durations)/len(durations), 'seconds')


def user_stats(df):
    """
    Get statistical data on customers of the company.

        Args:
            df: filtered dataframe obtain from the loda_data() function
    Output: count of different customer types, gender information, birth year information.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df['User Type'].fillna('Customer')
    user_types = df['User Type'].value_counts()
    print(user_types)
    try:
        df['Gender'].fillna('Unknown')
        genders = df['Gender'].value_counts()
        print(genders)
    except:
        print('No Gender information for this city')
    try:
        df['Birth Year'].fillna('Unknown')
        print('The earliest birth year is:', int(min(df['Birth Year'])))
        print('The most recent birth year is:', int(max(df['Birth Year'])))
        print('The most common birth year is:', int(df['Birth Year'].mode()[0]))
    except:
        print('No Birth Year information for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Displaying raw data to the user if he wants to view it:

        Args:
            df: filtered dataframe obtain from the loda_data() function
    Output: if user says 'yes', 5 rows or more of the filtered dataframe are displayed
    """

    count = 0

    while True:
        answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ')
        try:
            if answer.lower() == 'yes':
                print(df.iloc[count:count+5])
                count += 5
            if answer.lower() == 'no':
                break
        except:
            print('That was not a valid input, please try again.')
            continue



def main():
    """
    Interactive data analysis experience.

    Output: data analysis of the bikeshare database based on user input.
    """

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

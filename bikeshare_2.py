import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*40)
    while True:
        try:
            # get user input for city (chicago, new york city, washington)
            print('Which CITY do you like to see? Pick one and full-spelling')
            city = input('chicago | new york city | washington\n').lower()
            print('-'*40)
            # get user input for month (all, january, february, ... , june)
            print('Which MONTH do you like to see? Pick one and full-spelling')
            month = input('all | january | february | march | april | may | june\n').lower()
            print('-'*40)
            # get user input for day of week (all, monday, tuesday, ... sunday)
            print('Which DAY do you like to see? Pick one and full-spelling')
            day = input('all | monday | tuesday | wednesday | thursday | friday | saturday | sunday\n').lower()
            print('-'*40)
            # if the input not good, raise it
            if ((city not in ['chicago', 'new york city', 'washington']) or
                (month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']) or
                (day not in ['all', 'monday', 'tuesday', 'thursday', 'friday', 'saturday', 'sunday'])):
                    raise Exception
            confirm = (input('Looks like you want {0}, {1}, {2}. If not, type no, else type yes\n'.format(city,month,day)))
            if confirm.lower() == 'no':
                raise Exception

            break
        except:
            print('Well, wrong input, try again........')
            print('-'*40)

    print('-'*40)
    print('||| You are all set. Generating...... |||')
    print('-'*40)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mo = df['month'].mode()[0]
    print('------Most common month is: {}'.format(mo))

    # display the most common day of week
    da = df['day_of_week'].mode()[0]
    print('Most common day of week is: {}'.format(da))

    # display the most common start hour
    hr = df['Start Time'].dt.hour.mode()[0]
    print('-Most common start hour is: {}'.format(hr))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    stion = df['Start Station'].mode()[0]
    print('Most common start station is: {}'.format(stion))

    # display most commonly used end station
    etion = df['End Station'].mode()[0]
    print('--Most common end station is: {}'.format(etion))

    # display most frequent combination of start station and end station trip
    tion_comb = df['Start Station'] + ' |>->->| ' + df['End Station']
    combtion = tion_comb.mode()[0]
    print('---------Most common trip is: {}'.format(combtion))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('--Total travel time is: {}'.format(total))

    # display mean travel time
    avg = df['Trip Duration'].mean()
    print('Average travel time is: {}'.format(avg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    # put in the city as a arg
    # to determine if gender / birth year stats can be calculated

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ut = df['User Type'].value_counts()
    for atype in ut.index:
        print('Type--{0}, Count--{1}'.format(atype, ut[atype]))

    # Display counts of gender
    if 'Gender' in df:
        gd = df['Gender'].value_counts()
        for agender in gd.index:
            print('Type--{0}, Count--{1}'.format(agender, gd[agender]))
    else:
        print('Gender is not presented in the city of given dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        ymin = df['Birth Year'].min()
        ymax = df['Birth Year'].max()
        ymode = df['Birth Year'].mode()[0]
        print('Year of birth:')
        print('-----Earliest: {}'.format(ymin))
        print('--Most Recent: {}'.format(ymax))
        print('--Most Common: {}'.format(ymode))
    else:
        print('Birth Year is not presented in the city of given dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def nice5(df, idx):
    '''
    Print 5 lines of raw data from df, start from idx
    Keep printing 5 lines until showed halting
    '''
    while True:
        seeraw = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
        if seeraw.lower() == 'no':
            break
        print(df[idx:idx+5])
        idx += 5


def main():
    while True:
        # generate needed dataframe via user demand
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # generate stats info
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # if needed, generate raw data line, 5 lines once
        idx = 0
        nice5(df, idx)

        # restart or not
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

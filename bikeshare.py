import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns (all lowercase)
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['chicago', 'new york city', 'washington']
    prompt = 'Would you like to see data for Chicago, New York City, or Washington? '
    city = check_response(prompt, valid_cities)

    # Ask if user wants to filter by day, month, neither, or both
    valid_filters = ['weekday', 'month', 'both', 'neither']
    prompt = 'Would you like to filter the data by weekday, month, both, or neither? '
    filter_pref = check_response(prompt, valid_filters)

    # Default day and month to 'all', in case user has chosen not to filter by them
    month = 'all'
    day = 'all'
            
    # TO DO: get user input for month (all, january, february, ... , june)
    if filter_pref == 'month' or filter_pref == 'both':
        valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        prompt = "Please choose a month between January and June for which to view data (or 'all'): "
        month = check_response(prompt, valid_months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_pref == 'weekday' or filter_pref == 'both':
        valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        prompt = "Please choose a weekday for which to view data (or 'all'): "
        day = check_response(prompt, valid_days)
                
    print('-'*40)
    return city, month, day

def check_response(user_prompt, valid_list):
    good_input = False
    try:
        while not good_input:
            response = input(user_prompt).lower()
            if response in valid_list:
                good_input = True
            else:
                print('Invalid entry.  Please try again.')
    except:
        print('Invalid input. Exiting.')

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
    # convert the End Time column as well, for consistency
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
 
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
 
    # Begin output string to tell user what filters have been applied
    filter_str = 'Analysing data for ' + city.title() + ' for '

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

        # add to output string with filter day
        filter_str += day.title() + 's in '
        
    else:
        # add to output string for all weekdays
        filter_str += 'all days in '
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
 
        # add to output string with filter month, with appropriate suffix
        if month == 1:
            filter_str += 'the ' + str(month) + 'st month...'
        elif month == 2:
            filter_str += 'the ' + str(month) + 'nd month...'
        elif month == 3:
            filter_str += 'the ' + str(month) + 'rd month...'
        else:
            filter_str += 'the ' + str(month) + 'th month...'
            
    else:
        # add to output string for no month filter
        filter_str += 'all months...'

    print(filter_str)
                  
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_time = df['month'].mode()[0]
    print('The most common month for bike share hire is: ', common_time)

    # TO DO: display the most common day of week
    common_time = df['day_of_week'].mode()[0]
    print('The most common day of the week for bike share hire is: ', common_time)

    # TO DO: display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    common_time = df['Start Hour'].mode()[0]
    print('The most common hour to start a bike hire is: {}:00'.format(common_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_station = df['Start Station'].mode()[0]
    print('The most common station from which to start a ride is: ', common_station)

    # TO DO: display most commonly used end station
    common_station = df['End Station'].mode()[0]
    print('The most common station at which to end a ride is: ', common_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + ':::' + df['End Station']
    common_station = df['Station Combo'].mode()[0]
    separator = common_station.find(':::')
    start_station = common_station[:separator]
    end_station = common_station[separator + 3:]
    print('The most common trip is from {} to {}'.format(start_station, end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    num_days, num_hours, num_mins, num_secs = time_breakdown(total_time)
    print('Total travel time is {} days, {} hours, {} minutes, and {} seconds.' \
          .format(num_days, num_hours, num_mins, num_secs))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    num_days, num_hours, num_mins, num_secs = time_breakdown(mean_time)
    print('Average travel time is {} days, {} hours, {} minutes, and {} seconds.' \
          .format(num_days, num_hours, num_mins, num_secs))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def time_breakdown(total_secs):
    """Breaks number of seconds into days, hours, mins, and seconds
    Returns
        days (int):  Number of days in the time object
        hours (int): Number of hours in the time object (between 0 and 23)
        mins (int):  Number of minutes in the time object (between 0 and 59)
        secs (int):  Number of seconds in the time object (between 0 and 59) """
    days = int(total_secs // (3600 * 24))
    hours = int((total_secs // 3600) % 24)
    mins = int((total_secs // 60) % 60)
    secs = int(total_secs % 60)
    
    return days, hours, mins, secs

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The number of users by type for {} are:'.format(city.title()))
    for row in user_types.index:
        print('{}: {:,}'.format(row, user_types[row]))

    if city == 'washington':
        print('Gender and birth year breakdown is not available for Washington.')
    else:
    # TO DO: Display counts of gender
        print('Gender breakdown for {} is:'.format(city.title()))
        gender_counts = df['Gender'].value_counts()
        for row in gender_counts.index:
            print('{}: {:,}'.format(row, gender_counts[row]))
            
    # TO DO: Display earliest, most recent, and most common year of birth
        print('The earliest year of birth for users in {} is {:.0f}.'.format(city.title(), df['Birth Year'].min()))
        print('The most recent year of birth for users in {} is {:.0f}.'.format(city.title(), df['Birth Year'].max()))
        print('The most common year of birth for users in {} is {:.0f}.'.format(city.title(), df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df, city):
    """ Displays X records of data at a time for the user until they no 
        longer wish to see more data, using the original columns from the dataset
        X defaults to 5 if user does not choose between 1 and 10 rows to display
        Suppresses Gender and Birth Year columns for Washington  """
    
    # Assemble column list, depending if we're analysing Washington or not
    if city != 'washington':
        column_list = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', \
                          'End Station', 'User Type', 'Gender', 'Birth Year']
    else:
        column_list = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', \
                          'End Station', 'User Type']
    
    # Ask user if they want to see X records of data
    more_data = input('Would you like to view the first few records in the dataset? \
                      Enter yes or no.\n')
    if more_data.lower() == 'yes':
        # If 'yes', ask user how many rows of data they wish to see at once
        valid_rows = range(1,11)
        prompt = "How many (1-10) rows of data would you like to see at once? "
        if num_records not in valid_rows:
            print('Invalid response, defaulting to 5 rows.')
            num_records = 5

        # if 'yes' show the first num_records rows and ask again
        start_index = 0
        
        # keep asking and displaying until user says 'no' or we reach the end of the data
        while True:
            for i in range(start_index, start_index + num_records):
                
                # ensure we're not beyond the end of the data
                if i < df.shape[1]:
                    print(df[column_list].iloc[i])
                    
            # ask user again.  If 'yes', start X rows later
            more_data = input('Would you like to view {} more records of data?\n'.format(num_records))
            if more_data.lower() == 'yes':
                start_index += num_records
            # if 'no', exit
            else:
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
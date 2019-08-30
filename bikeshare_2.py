from datetime import timedelta
import time
import os.path
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv' }

CITY = ('chicago',
        'new york city',
        'washington')

MONTH = ('january', 
         'february',
         'march', 
         'april', 
         'may', 
         'june')

DAY = ('monday',
       'tuesday',
       'wednesday',
       'thursday',
       'friday',
       'saturday',
       'sunday')

total_run_time = 0

def query_time(func):
    """
    decorator function to log function execution time and capture total program execution time
    """
    def wrapper_function(*args, **kwargs):
        global total_run_time

        start_time = time.time()
        run_func = func(*args, **kwargs)
        total_time = time.time() - start_time
        total_run_time += total_time
        print(f"\nThis took {round(total_time, 4)} seconds.")
        print('-'*40)
        return run_func
    return wrapper_function


def get_user_input(prompt, validation_list):
    """ 
    prompts the user to input their selections and validates those selections are correct against a defined input list

    Arguments:
        (str) prompt - prompt to display in the terminal
        (list) validation_list - list of strings to validate that input is within expected values
    Returns:
        (list) user_input - list of strings holding users selections
    """
    print(prompt)
    
    print('Type \'view\' to list valid selections')
    print('-' * len(prompt))

    while True:
        user_input = list(map(str.strip, input().lower().split(",")))

        if 'view' in user_input:
            print(', '.join(list(x.title() for x in validation_list)))
            continue
        elif 'all' in user_input:
            return validation_list
        elif verify_user_input(user_input, validation_list):
            break
        else:
            print('Please enter valid input parameters: ')

    return user_input

def verify_user_input(user_input, validation_list):
    """
    Check if user input exists in predefined tuples
    """
    for i in user_input:
        if not i in validation_list:
            return False
    return True

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nWelcome! Let\'s explore some US bikeshare data!\n')
    print('Please input any multiple selections in a comma seperated list')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_user_input('Which city would you like to view? (Please select only one)',
                    CITY)

    # if user types in multiple cities, take first selection only
    if len(city) > 1:
        print(f"Multiple city selections made, only {str(city[0]).title()} will be used...")

    # get user input for month (all, january, february, ... , june)
    month = get_user_input('\nPlease select month(s) or type \'all\':',
                            MONTH)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input('\nPlease select day(s) of the week or type \'all\':',
                            DAY)

    return city, month, day


def load_data(city, file_path=''):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    file_path += str(CITY_DATA[city[0]]).replace(' ', '_')
    
    if os.path.exists(file_path):
        try:
            print('Loading data...')
            df = pd.read_csv(file_path)
            print(f"{len(df.index)} rows imported...")
        except:
            print('Error loading bikeshare data')
            return None
    else:
        print(f"Bikeshare data not found in {file_path}")
        return None

    return df


def parse_date_columns(df, *date_fields):
    """
    applies a datetime format to fields passed in as *args

    Returns:
        (DataFrame) df - a dataframe with the parsed data fields
    """
    try:
        print('Parsing date fields...')
        for date_field in date_fields:
            df[date_field] = pd.to_datetime(df[date_field])
    except TypeError:
        print('Error formatting selected field in DataFrame')
    return df


def apply_filters(df, month, day):
    """ 
    Applies uer selected filters for month(s) and day(s) to dataframe
    
    Args:
        (DataFrame) df - DataFrame to be filtered
        (list) month - Selected month(s)
        (list) day - Selected day(s)
    Returns:
        (DataFrame) - a filtered pandas DataFrame
     """
    # drop the source data index column as we don't need it
    df = df.drop(df.columns[0], axis=1)

    # parse date fields into the correct format
    df = parse_date_columns(df, 'Start Time', 'End Time')

    print('Adding derived columns...')
    # add derived columns for filtering of data
    df['day_of_month'] = df['Start Time'].dt.day
    df['month'] = df['Start Time'].dt.month_name()
    df['weekday_name'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['start_end_stations'] = df['Start Station'] + '/' + df['End Station']

    print('Applying user filters...')
    # apply user selected filters for month(s) and day(s)
    df = df[df['month'].isin([i.title() for i in month])]
    df = df[df['weekday_name'].isin([d.title() for d in day])]
    print(f'{len(df.index)} rows after filtering applied...')

    return df


def stats_output(df, column, text_interpolation):
    '''
    Generate a string to be output to the console for time_stats and station_stats

    Args:
        (DataFrame) df - dataframe to calculate value counts on
        (str) column - column in data frame to apply counts
        (str) text_interpolation - text to inject into returned string
    Returns:
        (str) - interpolated string output
    '''
    return f'The most common {text_interpolation} is \'{df[column].value_counts().idxmax()}\' with {df[column].value_counts().max()} observations.'


@query_time
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # display the most common month - ignore if only one selection made
    print(stats_output(df, 'month', 'month for travel'))

    # display the most common day of week - ignore if only one selection made
    print(stats_output(df, 'weekday_name', 'day of the week for travel'))

    # display the most common start hour
    print(stats_output(df, 'hour', 'hour of the day for travel'))


@query_time
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # display most commonly used start station
    print(stats_output(df, 'Start Station', 'start station'))

    # display most commonly used end station
    print(stats_output(df, 'End Station', 'end station'))

    # display most frequent combination of start station and end station trip
    print(stats_output(df, 'start_end_stations', 'combination of start and end station'))


@query_time
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time / 60 / 60
    print(f'Total Travel time was {round(total_travel_time_hours)} hours ({total_travel_time} seconds).')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_delta = str(timedelta(seconds=mean_travel_time))
    print(f'The mean travel time was {mean_travel_time_delta} ({mean_travel_time} seconds.)')


@query_time
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types
    print("User Type count:")
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        print("\nGender count:")
        print(df['Gender'].value_counts())
    except KeyError:
        print('Gender field not found in this dataset. Skipping...')

    # Display earliest, most recent, and most common year of birth
    try:
        print("\nBirth year stats:")
        print(f"Earliest: {str(int(df['Birth Year'].min()))}")
        print(f"Most recent: {str(int(df['Birth Year'].max()))}")
        print(f"Most common: {str(int(df['Birth Year'].value_counts().idxmax()))}")
    except KeyError:
        print('Birth Year field not found in this dataset. Skipping...')

    
def print_data_from_rows(df, num_rows=5, column_trim=0):
    """
    prints dataframe in n row chunks and asks user to either print next x lines or quit.

    Args:
        (DataFrame) df - takes a single dataframe to print out to the screen
        (int) num_rows - how many rows to print - default of 5
        (int) column_trim - how many colums to remove from the end of dataFrame - used to remove
              derived columns when viewing the data

    Yields: 5 rows of the dataframe object
    """
    for i in range(0, len(df.index), num_rows):
        print(f"Printing rows {i} to {i + num_rows} of {len(df.index)}...")
        yield df.iloc[i: i+num_rows, :-column_trim]


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, 'data/')
        if df is None:
            print('No data is loaded into DataFrame. Are the files saved in the correct directory?')
            break
        df = apply_filters(df, month, day)

        try:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            print(f"Total execution time: {round(total_run_time,4)} seconds.")
        except TypeError:
            print('A problem was encountered while trying to process the data. Exiting...')
            break

        user_answer = input('Would you like to view the raw data? Enter yes or no.\n').strip()
        if user_answer[0].lower() == 'y':
            for chunk in print_data_from_rows(df, column_trim=5):
                print(chunk)
                if input('\nView next 5 rows? (Y/n)\n').strip().lower()[0] == 'y':
                    continue
                else:
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
	main()

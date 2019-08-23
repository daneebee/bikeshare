import time # not used yet
import os.path
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv' }

CITY = ("chicago",
        "new york city",
        "washington")

MONTH = ("january", 
         "february",
         "march", 
         "april", 
         "may", 
         "june")

DAY = ("monday",
       "tuesday",
       "wednesday",
       "thursday",
       "friday",
       "saturday",
       "sunday")


class UserFilterSelections:
    city = []
    day = []
    month = []


class QueryTimer:
    """ 
    class to log run time of panda functions
    log start and end time to auto-calculate total running time
    stores class variable 'overall_time' to keep track of overall total running time
    for all instances of QueryTimer class

    Methods:
        set_start_time - log function start time
        set_end_time - log function end time, total time and overall time
                       of all functions run so far
        get_total_time - return f string of total function run time
    """
    overall_time = 0

    def set_start_time(self, time):
        self.start_time = time

    def set_end_time(self, time):
        self.end_time = time
        self.total_time = self.end_time - self.start_time
        QueryTimer.overall_time += self.total_time

    def get_total_time(self):
        return f"\nThis took {round(self.total_time, 4)} seconds."


def get_user_input(prompt, validation_list):
    """ doc string goes here """
    print(prompt)
    
    print("Type 'view' to list valid selections")
    print("-" * len(prompt))

    while True:
        user_input = list(map(str.strip, input().lower().split(",")))

        if "view" in user_input:
            print(", ".join(list(x.title() for x in validation_list)))
            continue
        elif "all" in user_input:
            return validation_list
        elif verify_user_input(user_input, validation_list):
            break
        else:
            print("Please enter valid input parameters: ")

    return user_input

def verify_user_input(user_input, validation_list):
    ''' 
    Check if user input exists in predefined tuples
    '''
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
    print("Please input any multiple selections in a comma seperated list")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_user_input("Which city would you like to view? (Please select only one)",
                    CITY)

    # if user types in multiple cities, take first selection only
    if len(city) > 1:
        print(f"Multiple city selections made, only {str(city[0]).title()} will be used...")

    # get user input for month (all, january, february, ... , june)
    month = get_user_input("\nPlease select month(s) or type 'all':",
                            MONTH)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input("\nPlease select day(s) of the week or type 'all':",
                            DAY)

    return city, month, day


def load_data(city, file_path=""):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_path += str(CITY_DATA[city[0]]).replace(" ", "_")
    
    if os.path.exists(file_path):
        try:
            print('Loading data...')
            df = pd.read_csv(file_path)
            print(f"{len(df.index)} rows imported...")
        except:
            print("Error loading bikeshare data")
            return None
    else:
        print(f"Bikeshare data not found in {file_path}")
        return None

    return df


def parse_date_columns(df, *date_fields):
    """
    applies a datetime format to fields passed in as *args
    """
    try:
        print('Parsing date fields...')
        for date_field in date_fields:
            df[date_field] = pd.to_datetime(df[date_field])
    except TypeError:
        print("Error formatting selected field in DataFrame")
    return df


def apply_filters(df, month, day):
    """ 
    Applies uer selected filters for month(s) and day(s) to dataframe
    
    Args:
        (DataFrame) df - DataFrame to be filtered
        (list) month - Selected month(s)
        (list) day - Selected day(s)
    Returns:
        DataFrame
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

    print('Applying user filters...')
    # apply user selected filters for month(s) and day(s)
    df = df[df["month"].isin([i.title() for i in month])]
    df = df[df["weekday_name"].isin([d.title() for d in day])]
    print(f"{len(df.index)} rows after filtering applied...")

    # drop rows with missing data as we can't use these to display our stats
    # move to indivual functions for stats
    #df = df.dropna()
    #print(f"{len(df.index)} rows after removing records with null values...")
    
    return df

def time_stats_output(df, column, text_interpolation):
    return f"The most common {text_interpolation} for travel is {df[column].value_counts().idxmax()} with {df[column].value_counts().max()} observations."


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    qt = QueryTimer()
    qt.set_start_time(time.time())

    # display the most common month - ignore if only one selection made
    print(time_stats_output(df, 'month', 'month'))

    # display the most common day of week - ignore if only one selection made
    print(time_stats_output(df, 'weekday_name', 'day of the week'))

    # display the most common start hour
    print(time_stats_output(df, 'hour', 'hour'))

    qt.set_end_time(time.time())
    print(qt.get_total_time())
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    qt = QueryTimer()
    qt.set_start_time(time.time())

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip

    qt.set_end_time(time.time())
    print(qt.get_total_time())
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    qt = QueryTimer()
    qt.set_start_time(time.time())

    # display total travel time


    # display mean travel time

    qt.set_end_time(time.time())
    print(qt.get_total_time())
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    qt = QueryTimer()
    qt.set_start_time(time.time())

    # Display counts of user types


    # Display counts of gender


    # Display earliest, most recent, and most common year of birth

    qt.set_end_time(time.time())
    print(qt.get_total_time())
    print('-'*40)


def print_data_from_rows(df, num_rows=5):
    '''
    prints dataframe in n row chunks and asks user to either print next x lines or quit.

    Args:
        (DataFrame) df - takes a single dataframe to print out to the screen
        (int) num_rows - how many rows to print - default of 5

    Yields: 5 rows of the dataframe object
    '''
    for i in range(0, len(df.index), num_rows):
        print(f"Printing rows {i} to {i + num_rows} of {len(df.index)}...")
        yield df.iloc[i: i+num_rows, :-4]


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, "data/")
        df = apply_filters(df, month, day)

        try:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            total_execution_time = round(QueryTimer.overall_time, 2)
            print(f"Total execution time: {total_execution_time} seconds.")
        except TypeError:
            print("A problem was encountered while trying to process the data. Exiting...")
            break

        user_answer = input("Would you like to view the raw data? Enter yes or no.\n").strip()
        if user_answer[0].lower() == 'y':
            for chunk in print_data_from_rows(df):
                print(chunk)
                if input("\nView next 5 rows? (Y/n)\n").strip().lower()[0] == 'y':
                    continue
                else:
                    break
            # function to show 5 rows of raw data at time - use generator?
            pass

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

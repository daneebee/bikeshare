import time
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


class QueryTimer:
    """ 
    class to log run time of panda functions
    log start and end time to auto-calculate total running time
    stores class variable 'overall_time' to keep track of overall total running time
    for all instances of QueryTimer class
    """
    overall_time = 0

    def set_start_time(self, time):
        self.start_time = time

    def set_end_time(self, time):
        self.end_time = time
        self.total_time = self.end_time - self.start_time
        QueryTimer.overall_time += self.total_time

    def get_total_time(self):
        return f"This took {round(self.total_time, 2)} seconds."


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

    if len(city) > 1:
        print(f"Multiple city selections made, only {str(city[0]).title()} will be used...")

    # get user input for month (all, january, february, ... , june)
    month = get_user_input("\nPlease select month(s) or type 'all':",
                            MONTH)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input("\nPlease select day(s) of the week or type 'all':",
                            DAY)

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
    file_path = "data/" + str(CITY_DATA[city[0]]).replace(" ", "_")
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
        except:
            print("Error loading bikeshare data")
            return None
    else:
        print(f"Bikeshare data not found in {file_path}")
        return None

    # check if any columns contain NaN data
    print(df.isnull().any())

    return apply_filters(df, month, day)


def apply_filters(df, month, day):
    """ doc string here """

    # apply column formatting - move to new function
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['day'] = df['Start Time'].dt.day
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    df = df[df["month"].isin([i.title() for i in month])]
    df = df[df["day_of_week"].isin([d.title() for d in day])]

    print(df.head(10))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    qt = QueryTimer()
    qt.set_start_time(time.time())

    # display the most common month


    # display the most common day of week


    # display the most common start hour

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


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if not df is None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            total_execution_time = round(QueryTimer.overall_time, 2)
            print(f"Total execution time: {total_execution_time} seconds.")
        else:
            print("Dataset returned no results or is empty.")

        user_answer = input("Would you like to view the raw data? Enter yes or no.\n").strip()
        if user_answer[0].lower() == 'y':
            # function to show 5 rows of raw data at time - use generator?
            pass

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

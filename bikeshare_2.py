import time
import os.path
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITY = ("chicago",
        "new york city",
        "washington")

MONTH = ("all", 
         "january", 
         "february",
         "march", 
         "april", 
         "may", 
         "june")

DAY = ("all",
       "monday",
       "tuesday",
       "wednesday",
       "thursday",
       "friday",
       "saturday",
       "sunday")

class QueryTimer:
    overall_time = 0

    """ doc string goes here """
    def set_start_time(self, time):
        self.start_time = time

    def set_end_time(self, time):
        self.end_time = time
        self.total_time = self.end_time - self.start_time
        QueryTimer.overall_time += self.total_time

    def get_total_time(self):
        return f"This took {round(self.total_time, 2)} seconds".format()


def get_user_input(prompt, validation_list):
    """ doc string goes here """
    print(prompt)
    
    print("Type 'view' to list valid selections")
    print("-" * len(prompt))

    while True:
        output = input().strip().lower()

        if output == "view":
            print(", ".join(list(x.title() for x in validation_list)))
        elif output in validation_list:
            break
        else:
            print("Please enter a valid input: ")

    return output


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Welcome! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_user_input("Which city would you like to view?",
                    CITY)

    # get user input for month (all, january, february, ... , june)
    month = get_user_input("\nPlease selet a month or type 'all':",
                            MONTH)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input("\nPlease select a day of the week or type 'all':",
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
    file_path = "data/" + str(CITY_DATA[city]).replace(" ", "_")
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
        except:
            print("Error loading bikeshare data")
            return None
    else:
        print("Bikeshare data not found")
        return None

    # filter the data
    if not month == "all":
        pass
    if not day == "all":
        pass

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month


    # display the most common day of week


    # display the most common start hour


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types


    # Display counts of gender


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
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
            print(f"Total execution time: {total_execution_time} seconds".format())

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

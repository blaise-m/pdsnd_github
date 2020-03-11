import time
import datetime
import pandas as pd
import numpy as np
import os
import platform


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = { 'Chicago': 'chicago',
            'New York City': 'new york city',
            'Washington, DC': 'washington'}

MONTHS = { 'a': 'January',
            'b': 'February',
            'c': 'March',
            'd': 'April',
            'e': 'May',
            'f': 'June' }

MONTH_NUMBER = { 'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6 }

DAYS = { 'a': 'Monday',
        'b': 'Tuesday',
        'c': 'Wednesday',
        'd': 'Thursday',
        'e': 'Friday',
        'f': 'Saturday',
        'g': 'Sunday' }

DAY_NUMBER = { 'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6 }


DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTH_NAMES = ['', 'January', 'February', 'March', 'April', 'May', 'June']


def clear_screen():
    """
    Clears the terminal screen.
    """
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('clear')


def prompt(cl="clear"):
    """
    Prompts the user if he wants to proceed or terminate the program
    Clears screen if the user wants to proceed and continues running the program
    """
    try:
        choice = str(input("\n\nPress any key to proceed or z to exit: ")).lower()
        if choice == "z":
            quit()
        else:
            if cl == "clear":
                clear_screen()
    except Exception as e:
        print(e)
        quit()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """   

    print("\nWe will start by adding filters to the data to retain only the data of our interest.")
    print("\n\nThe bikeshare data covers the first 6 months of 2017 for three cities:")
    print("a. Chicago")
    print("b. New York City &")
    print("c. Washington, DC")

    proceed = 'no'    
    while proceed != "yes":
        try:
            choice = str(input("\n\nPlease select a city of your interest (enter a, b or c) to view the summary data: ")).lower()
            proceed = "yes"     
            if choice == "a":
                city = "Chicago"
            elif choice == "b":
                city = "New York City"
            elif choice == "c":
                city = "Washington, DC"
            else:
                print("Invalid input 👷👷👷. The valid entries are a, b or c.")
                proceed = 'no'
        except Exception as e:
            print("An error occurred while processing your input 👷👷👷. The valid entries are a, b or c.")
            proceed = 'no'

    print("\n\nWe have loaded the data for '{}' as instructed.".format(city))
    print("But as pointed out, the data covers a period of 6 months.")

    proceed = 'no'    
    while proceed != "yes":
        try:
            choice = str(input("Do you want to filter the data by month or should we proceed with unfiltered data? \
                \n\n\nEnter 'yes' to add the monthly filter or 'no' to proceed: ")).lower()
            proceed = "yes"     
            if choice=="no" or choice=="'no'":
                month_filter = False
                month = "all"
                day = "all"
            else:
                month_filter = True
        except Exception as e:
            print("An error occurred while processing your input 👷👷👷. The valid entries are 'yes' or 'no'.")
            proceed = 'no'
    
    if month_filter:
        proceed = 'no'    
        while proceed != "yes":
            print("\n\nThe month are summarized below:")
            print("a. January \nb. February \nc. March \nd. April \ne. May \nf. June")
            try:
                choice = str(input("\n\nPlease select a month to filter by: ")).lower()
                proceed = "yes"     
                if choice=="a" or choice=="b" or choice=="c" or choice=="d" or choice=="e" or choice=="f":
                    month = MONTHS[choice]
                else:
                    print("Invalid input 👷👷👷. The valid entries are a, b, c, d, e or f.")
                    proceed = 'no'
            except Exception as e:
                print("An error occurred while processing your input 👷👷👷. The valid entries are a, b, c, d, e or f.")
                proceed = 'no'
    
        print("\n\nWe now have the data for '{}' filtered by the month of '{}'.".format(city, month))
        print("We can filter the data even further by day, to get insight on the daily trends.")

        proceed = 'no'    
        while proceed != "yes":
            try:
                choice = str(input("Do you want to filter the data by the day of the week? \
                    \n\n\nEnter 'yes' to add the daily filter or 'no' to proceed: ")).lower()
                proceed = "yes"     
                if choice=="no" or choice=="'no'":
                    day_filter = False
                    day = "all"
                else:
                    day_filter = True
            except Exception as e:
                print("An error occurred while processing your input 👷👷👷. The valid entries are 'yes' or 'no'.")
                proceed = 'no'
        
        if day_filter:
            proceed = 'no'    
            while proceed != "yes":
                print("\n\nThe days of the week are summarized below:")
                print("a. Monday \nb. Tuesday \nc. Wednesday \nd. Thursday \ne. Friday \nf. Saturday \ng. Sunday")
                try:
                    choice = str(input("\n\nPlease select a day of the week to filter by: ")).lower()
                    proceed = "yes"     
                    if choice=="a" or choice=="b" or choice=="c" or choice=="d" or choice=="e" or choice=="f" or choice=="g":
                        day = DAYS[choice]
                    else:
                        print("Invalid input 👷👷👷. The valid entries are a, b, c, d, e, f or g.")
                        proceed = 'no'
                except Exception as e:
                    print("An error occurred while processing your input 👷👷👷. The valid entries are a, b, c, d, e, f or g.")
                    proceed = 'no'
        
            print("\n\nWe have successfully loaded the data for '{}' filtered by the month of '{}' and by the weekday '{}'.".format(city, month, day))
           
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

    city_data = pd.read_csv(CITY_DATA[CITIES[city]])

    if month == 'all':
        df = pd.DataFrame(city_data)
    elif day == 'all':
        df = pd.DataFrame(city_data)
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df = df[df['Start Time'].dt.month == MONTH_NUMBER[month]]
    else:
        df = pd.DataFrame(city_data)
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df = df[df['Start Time'].dt.month == MONTH_NUMBER[month]]
        df = df[df['Start Time'].dt.dayofweek == DAY_NUMBER[day]]

    return df


def explore_data(df):
    print("\n\nBelow are the first 5 entries in the loaded dataset:\n")
    print(df[:5])

    prev_count = 0
    next_count = 5
    
    proceed = 'no'    
    while proceed != "yes":
        try:
            choice = str(input("\n\nWould you like to view the next 5 entries? \nEnter 'yes' to view the next 5 entries or 'no' to proceed: ")).lower()
            
            if choice=="no" or choice=="'no'":
                proceed = "yes"
            else:
                print("\n\nBelow are the next 5 entries in the loaded dataset:\n")
                prev_count += 5
                next_count += 5
                print(df[prev_count: next_count])

                if next_count >= len(df):
                    proceed = "yes"

        except Exception as e:
            print("An error occurred while processing your input 👷👷👷. The valid entries are 'yes' or 'no'.")
            proceed = 'no'


def remove_blanks(df):
    print("We will first delete all the rows that are completely blank.")

    prompt("do_not_clear")
    df = df.dropna(how='all')

    print("\n\nWe have deleted all the rows that are completely blank. \n\nNew Summary:")
    print("-------------------------")
    print(df.isnull().sum())
    print("-------------------------")    
    
    if df.isnull().sum().sum() != 0:
        print("\n\nBut even after this initial data cleaning, though now each row atleast contains some data, we still have some blank entries.")
        print("We will proceed and fill or delete the blank entries in our dataset.")
        prompt("clear")

        print("\n\nIn an attempt to remove the remaining blank entries, there are several methods we can use:\n")
        print("a. Delete the row that contains the blank entry")
        print("b. Use the previous entry in the series to fill the blank")
        print("c. Use the next entry in the series to fill the blank\n")
        print("Note: \nWe can also use the average of the previous and next entries in the series if dealing with numeric data")
        print("In our case, we have data of mixed types so we will resort to the three methods stated above.")

        proceed = 'no'
        while proceed != "yes":
            try:
                choice = str(input("\n\nPlease select a desired method to use to remove the remaining blanks from this dataset: ")).lower()
                proceed = "yes"     
                if choice == "a":
                    df = df.dropna(axis=0)
                elif choice == "b":
                    df = df.fillna(method='ffill', axis=1)
                elif choice == "c":
                    df = df.fillna(method='backfill', axis=1)
                else:
                    print("\nInvalid input 👷👷👷. The valid entries are a or b or c.\n\n")
                    proceed = 'no'
            except Exception as e:
                print("\nInvalid input 👷👷👷. The valid entries are a or b or c.\n\n")
                proceed = 'no'
        
        if df.isnull().sum().sum() != 0:
            df = df.dropna(axis=0)
        
        return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n\n')
    start_time = time.time()

    # display the most common month
    # display the most common day of week
    # display the most common start hour

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    monthly_df = df.copy()
    monthly_df['Start Time'] = monthly_df['Start Time'].dt.month
    print("Monthly occurrencies")
    print("---------------------")  
    print(monthly_df['Start Time'].value_counts())
    max_monthly_df = monthly_df['Start Time'].value_counts().index[0]
    
    daily_df = df.copy()
    daily_df['Start Time'] = daily_df['Start Time'].dt.dayofweek
    print("\n\nDay of the week occurrencies")
    print("----------------------------")  
    print(daily_df['Start Time'].value_counts())
    max_daily_df = daily_df['Start Time'].value_counts().index[0]

    hourly_df = df.copy()
    hourly_df['Start Time'] = hourly_df['Start Time'].dt.hour
    max_hourly_df = hourly_df['Start Time'].value_counts().index[0]

    print("\n\nApplied filters:  a. City: {}   b. Month(s): {}   c. Day(s): {}".format(city, month, day))
    print("\n\nThe most frequent times of travel are as follows:\n")
    print("a. Most common month: {}".format(MONTH_NAMES[max_monthly_df]))
    print("b. Most common day of the week: {}".format(DAY_NAMES[max_daily_df]))
    print("c. Most common hour: {}:00 hrs".format(max_hourly_df))    
    
    print("\n\nThis took %s seconds." % (time.time() - start_time))


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trips...\n\n')
    start_time = time.time()

    # display most commonly used start station
    # display most commonly used end station
    # display most frequent combination of start station and end station trip

    print("Start Station occurrencies")
    print("----------------------------")  
    print(df['Start Station'].value_counts())
    start_df = df['Start Station'].value_counts().index[0]
    
    print("\n\nEnd Station occurrencies")
    print("-------------------------------------------")  
    print(df['End Station'].value_counts())
    end_df = df['End Station'].value_counts().index[0]

    df['trip'] = df['Start Station'] + " - " + df['End Station']
    start_end_df = df['trip'].value_counts().index[0]

    print("\n\nApplied filters:  a. City: {}   b. Month(s): {}   c. Day(s): {}".format(city, month, day))
    print("\n\nThe most popular stations and trips are as follows:")
    print("a. Most common start station: {}".format(start_df))
    print("b. Most common end station: {}".format(end_df))
    print("c. Most common trip: {} ==>>> {}".format(start_end_df.split(" - ")[0], start_end_df.split(" - ")[1]))
    

    print("\n\nThis took %s seconds." % (time.time() - start_time))


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n\n')
    start_time = time.time()

    # display total travel time
    # display mean travel time

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Time Delta'] = df['End Time'] - df['Start Time']
    total_df = df['Time Delta'].sum()
    mean_df = df['Time Delta'].mean()

    print("Applied filters:  a. City: {}   b. Month(s): {}   c. Day(s): {}".format(city, month, day))
    print("\n\nThe total and average trip durations are as follows:")
    print("a. The total trip duration is: {} hrs {} minutes and {} seconds" \
        .format(str(total_df).split(":")[0], str(total_df).split(":")[1], str(total_df).split(":")[2]))
    print("b. The average trip duration is: {} hrs {} minutes and {} seconds" \
        .format(str(mean_df).split(":")[0], str(mean_df).split(":")[1], str(mean_df).split(":")[2]))    
    
    print("\n\nThis took %s seconds." % (time.time() - start_time))


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n\n')
    start_time = time.time()

    # Display counts of user types
    # Display counts of gender
    # Display earliest, most recent, and most common year of birth

    df['User Count'] = df['Start Time']
    user_df = df[['User Type', 'User Count']].groupby(['User Type']).count()
    print("User Type occurrencies")
    print("-------------------------")  
    print(user_df)

    if "Gender" in df:
        df['Gender Count'] = df['Start Time'] 
        gender_df = df[['Gender', 'Gender Count']].groupby(['Gender']).count()
        print("\n\nGender occurrencies")
        print("-------------------------")  
        print(gender_df)

    print("\n\nApplied filters:  a. City: {}   b. Month(s): {}   c. Day(s): {}".format(city, month, day))
    
    if "Birth Year" in df:
        birth_year_df = df.groupby(['Birth Year']).count()
        print("\nSummary data for year of birth: \na. Earliest: {} \nb. Most recent: {} \nc. Most Common: {}" \
            .format(df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].value_counts().index[0]))

    print("\n\nThis took %s seconds." % (time.time() - start_time))


def start_analysis(df, city, month, day):
    
    print("\nThe analysis is broken down into the following areas:\n")
    print("a. The statistics on the most frequent times of travel")
    print("b. The statistics on the most popular stations and trip")
    print("c. The statistics on the total and average trip duration &")
    print("d. The statistics on bikeshare users\n")

    proceed = 'no'
    while proceed != "yes":
        try:
            choice = str(input("\n\nPlease select the desired area to view the summary statistics: ")).lower()
            proceed = "yes"     
            if choice == "a":
                time_stats(df, city, month, day)
            elif choice == "b":
                station_stats(df, city, month, day)
            elif choice == "c":
                trip_duration_stats(df, city, month, day)
            elif choice == "d":
                user_stats(df, city, month, day)
            else:
                print("\nInvalid input 👷👷👷. The valid entries are a or b or c.\n\n")
                proceed = 'no'
        except Exception as e:
            print("\nAn error occurred while processing your input 👷👷👷. The valid entries are a or b or c.\n\n")   
            print(e)         
            proceed = 'no'


def main():

    while True:
        print("\nHey there,")    

        print("\n\nOver the past decade, bicycle-sharing systems have been growing in number and popularity in cities")
        print("across the world. Bicycle-sharing systems allow users to rent bicycles on a very short-term basis for a")
        print("price. This allows people to borrow a bike from point A and return it at point B, though they can also")
        print("return it to the same location if they'd like to just go for a ride. Regardless, each bike can serve several")
        print("users per day.")

        print("\n\nThanks to the rise in information technologies, it is easy for a user of the system to access a dock within")
        print("the system to unlock or return bicycles. These technologies also provide a wealth of data that can be")
        print("used to explore how these bike-sharing systems are used. This program contains data provided by Motivate,")
        print("a bike share system provider for many major cities in the United States.")
        print("\n\nWe will use this data to explore US bikeshare. Select the options that suit your needs as you proceed")
        print("through the analysis.")

        prompt("clear")
        
        city, month, day = get_filters()        
        df = load_data(city, month, day).sort_index()

        print("\n\nBelow is a snapshot of the loaded data:\n")
        print(df)

        prompt("clear")
        print("\nWe now have the data loaded for analysis.")
        print("Would you like to explore the data further before proceeding to the analysis?")
        
        proceed = 'no'    
        while proceed != "yes":
            try:
                choice = str(input("\n\nEnter 'yes' to explore the data or 'no' to proceed to the analysis: ")).lower()
                explore = True
                proceed = 'yes'     
                if choice=="no" or choice=="'no'":
                    explore = False                
            except Exception as e:
                print("An error occurred while processing your input 👷👷👷. The valid entries are 'yes' or 'no'.")
                proceed = 'no'

        if explore:
            explore_data(df)

        clear_screen()

        start_analysis(df, city, month, day)

        proceed = 'no'    
        while proceed != "yes":
            try:
                choice = str(input("\n\nPress any key to proceed with the analysis or z to exit: ")).lower()
                proceed = 'yes'     
                if choice!="z":
                    clear_screen()
                    start_analysis(df, city, month, day)
                    proceed = 'no'
            except Exception as e:
                print("An error occurred while processing your input 👷👷👷. The valid entries are 'yes' or 'no'.")
                proceed = 'no'

        restart = input('\n\nWould you like to restart? Enter yes or no: ')
        clear_screen()
        
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
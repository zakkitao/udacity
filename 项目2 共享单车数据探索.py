#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np


# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[3]:


def process(raw):
    product1 = "\nPlease input which {} would like to know about:".format(raw)
    if raw == "city":
        byproduct = ["all","chicago","new york city","washington"]
    elif raw == "month":
        byproduct = ["all","january","february","march","april","may","june"]
    elif raw == "day":
        byproduct = ["all","monday","tuesday","thurday","wednesday","friday","saturday","sunday"]
    product2 = "\nSorry,please input correct option among{}:".format(byproduct)
    product3 = byproduct
    return product1,product2,product3
    
def process_again(processed_goods):
    ret = input(processed_goods[0]).lower()
    while ret not in processed_goods[2]:
        ret = input(processed_goods[1]).lower()
    return ret

def get_filters():
    city = process_again(process("city"))
    month = process_again(process("month"))
    day = process_again(process("day"))
    return city,month,day


# In[4]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    if city == "all":
        df1 = pd.read_csv(CITY_DATA["chicago"])
        df2 = pd.read_csv(CITY_DATA["washington"])
        df2["Gender"] = np.nan
        df2["Birth Year"] = np.nan
        df3 = pd.read_csv(CITY_DATA["new york city"])
        df = pd.concat([df1,df2,df3],keys = ["df1","df2","df3"])
    else:
        df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] =  df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]
    
    return df


# In[5]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    avert_date = pd.to_datetime(df["Start Time"])
    avert_month = avert_date.dt.month
    i = avert_month.mode()[0]
    m =("january","february","march","april","may","june")
    common_month = m[i-1]

    # TO DO: display the most common day of week
    common_day = df["day_of_week"].mode()[0]

    # TO DO: display the most common start hour
    avert_hour = avert_date.dt.hour
    common_hour = avert_hour.mode()[0]

    print("\nThe most common month is {}.".format(common_month))
    print("\nThe most common day of week is {}.".format(common_day))
    print("\nThe most common start hour is {}.".format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_st = df["Start Station"].mode()[0]

    # TO DO: display most commonly used end station

    common_end_st = df["End Station"].mode()[0]
    # TO DO: display most frequent combination of start station and end station trip
    combination = "start from " + df["Start Station"] + ",end at " + df["End Station"]
    common_combin = combination.mode()[0]

    print("\nThe most commonly used start station is {}.".format(common_start_st))
    print("\nThe most commonly used end station is {}.".format(common_end_st))
    print("\nThe most frequent combination of start station and end station trip is {}.".format(common_combin))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[7]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_time_t = df["Trip Duration"].sum()

    # TO DO: display mean travel time
    travel_time_m = df["Trip Duration"].mean()


    print("\nThe total travel time is {}s.".format(travel_time_t))
    print("\nThe mean travel time is {}s.".format(travel_time_m))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usertype_count = df["User Type"].value_counts()
    
    # TO DO: Display counts of gender
    gender_counts = df["Gender"].value_counts()
    
    # TO DO: Display earliest, most recent, and most common year of birth
    earliest_year = df["Birth Year"].min().astype("int")
    most_recent = df["Birth Year"].max().astype("int")
    common_year = df["Birth Year"].mode()[0].astype("int")

    print("\nThe counts of user types are:\n{}".format(usertype_count))
    print("\nThe counts of gender are:\n{}".format(gender_counts))
    print("\nThe earliest_year of birth is {},the most_recent year of birth is {},the most common year of birth is {}.".format(earliest_year,most_recent,common_year))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        try:
            city == "washington"
            user_stats(df)
        except:
            print("Sorry,the column is lack.")
        finally:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
	main()


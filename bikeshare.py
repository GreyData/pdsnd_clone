import time
import calendar as cal 
import pandas as pd
import numpy as np

print_width = 40
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

"""
Clear some lines in the output to improve readability
"""
def cls():
    print("\n"*20)

def printline(ques,ans=""):
    
    
    print("|", "*"*(print_width-len(ques) ),ques, " | " ,ans )

"""
Prompts user to choose one of the items available in the city dictionary file
Returns the key from the city data dictionary,
Catering for user input errors and future additions
    ** as long as city keys start with different characters
"""

def get_city():
    msg = "Please choose:"
    usr = "X" # default-non-existant user choice value
    
    #cater for spelling - consider first char only
    valid = [w[0].lower() for w in list(CITY_DATA.keys())] 
    
    #temp dictionary to link user choice to city keys
    choose =dict(zip(valid,list(CITY_DATA.keys()))) 
    
    #showavailable choices
    while usr not in valid:
        print(msg)
        for x in list(CITY_DATA.keys()):
            print("[{}] {}".format((x[0]).upper(),x.capitalize() ))

        try:
            usr = input("Selection -? ")[0].lower() # first character only, lowercase 
        except:
            usr = 'X'
        
        #only used when first pass fails
        msg = "Invalid Choice! \n Only [C]hoose:"

    print("Chosen {} - ".format(choose[usr]) )
    
    return choose[usr]

"""
Accepts a numeric value to represent the month, or no filter choice [0 ..12]
"""
def get_month():
 
    ui = 99
    while ui not in range(13):
        try:
            print("please enter the month [1 - 12] you wish to filter by? [0] for All")
            ui = int(input("?_ "))
        except:
            ui=13
            print("please enter a month number from 0 to 12")
        finally:
            print("...")
            
    if ui==0:
        ans= "All"
    else:
        ans= cal.month_name[ui]

    print("Selected {}".format(ans))
    return ui


def get_day():
    ans = None

    print("0: no filter")
    for i in range(7): print("{}: {} ".format(i+1,cal.day_name[i]))
    print("Would you like to filter by a weekday? 0 for no filter")
    while ans not in range(8):
        try:
            ans = int(input("0..7 ?_"))
        except:
            ans = None
            print("try again")

    if ans==0:
        response = 'All'
    else:
        response = cal.day_name[i-1]             
    
    print("Selected day filter is: {}".format(response))
    return ans

def top(df,field):
    try:
        t = df[field].value_counts().idxmax()
    except:
        t = "NotFound"

    return t 


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = get_city()
    #city = "chicago"

    month = get_month()  #0-12 returned
    
    #day ="tuesday"
    day = get_day()  # 0-7
    
    print('-'*print_width)
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

    df = pd.read_csv(CITY_DATA[city],parse_dates=['Start Time'])
    df['StartMonth'] = df['Start Time'].dt.month
        
    df['WeekDay'] = df['Start Time'].dt.weekday
    df['StartHr'] = df['Start Time'].dt.hour
    
    ##most popular hour
    #popular_hour = df['hour'].mode()[0]

    # filter dataframe, creating new
    if month != 0:
        df = df[df["StartMonth"] == month]
       
    if day != 0:
        df = df[df["WeekDay"] == day]

    print(df["StartMonth"].value_counts())
    print(CITY_DATA[city])

    #df = ""
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #printline(" most common month :", df["StartMonth"].mode() )
    printline("most common month :", top(df,"StartMonth"))
    printline("most common weekday :", top(df,"WeekDay"))
    printline("most common starting Hour :", top(df,"StartHr")) #df['Start Time'].dt.hour.value_counts().idxmax())
    printline("This took %s seconds." % (time.time() - start_time))

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    printline('nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    
    printline("most common Start Station :", top(df,"Start Station"))
    printline("most common End Station :", top(df,"End Station"))
    df['Trip Name'] = df['Start Station'][:10] + ' -to- ' + df['End Station'][:10] 
    printline("most common Journey :", top(df,"Trip Name"))

    printline("This took %s seconds." % (time.time() - start_time))
    #print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    printline('*')
    printline('Calculating Trip Duration...')
    start_time = time.time()
    df['EndDate'] =pd.to_datetime(df['End Time'])
    printline("Total trip durations", (pd.to_datetime(df['End Time']) - df['Start Time']).sum())

    # TO DO: display total travel time
    # TO DO: display mean travel time
    avgtime = int(df['Trip Duration'].mean()//60 )
    printline("Average Trip minutes",avgtime )
    printline("This took %s seconds." % (time.time() - start_time))
    #print('-'*40)

def print_values(df,field):
    try:
        usr_field = df[field].value_counts()
        for u,v in usr_field.iteritems():
            printline(  str(u) ,  str(v) )
    except:
        printline("No detail for ",field)
    
def proc_dob(df):
    try:
        minYr = str(df['Birth Year'].min())[4]
        maxYr = str(df['Birth Year'].max())[:4]
        meanYr = str(df['Birth Year'].mean())[:4]
        printline("Earliest Year",minYr)
        printline("Latest Year",maxYr)
        printline("Most common year",meanYr)
    except:
        printline("This dataset ontains NO Birth year stats")

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\n')
    printline('Calculating User Stats...')
    start_time = time.time()

    # TO DO: Display counts of user types
    print_values( df,'User Type')
    
    #printline("Types of users",user_types )
    print_values( df,'Gender')
    # TO DO: Display counts of gender
    # TO DO: Display earliest, most recent, and most common year of birth
    proc_dob(df)

    printline("This took %s seconds." % (time.time() - start_time))
    #print('-'*40)

def main():
      
    while True:
        
        city, month, day = get_filters()
        cls()
                
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        printline("*")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart[0].lower() != 'y': #es':
            break

if __name__ == "__main__":
	main()



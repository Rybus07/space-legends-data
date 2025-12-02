from datetime import datetime, timedelta # added timedelta for pause message
from zoneinfo import ZoneInfo # for local Philadelphia timezone
import dateutil.parser as dateparser
import pprint # changed to import the whole module
import requests
import time # for sleep timer
import json # for saving the file at the end
import sys

def launch_date_filter(start_year, end_year):

    if start_year == 'earliest':
        start_date = f"1957-01-01"
    else:
        start_date = f"{start_year}-01-01"

    start_time = dateparser.parse(start_date)
    
    if end_year == 'most recent':
        end_time = datetime.now()
    else:
        end_date = f"{end_year}-12-31"
        end_time = dateparser.parse(end_date)

    # Visual check
    #print("Start date:", start_time.isoformat())
    #print("End date:", end_time.isoformat())

    #Set the filter parameters with the start and end date:
    net_filters = f'net__gte={start_time.isoformat()}&net__lte={end_time.isoformat()}'

    return net_filters




def fetchall_previous_launches(time_zone = 'America/New_York', collection_mode = 'test', verbose = True, save= True):
    '''
    This function allows for you a quick and easy way to request all launches previous from Launch Library 2. \n

    There are 2 specific inputs to make the call:\n
        1. time_zone : Which utilizes the built in ZoneInfo package to help with pagaination\n
        (Note): Placeholder is in time zone 'America/New_York' change it to suit your region.\n
        2. mode : Allows you to select either 'test' or 'full collection' modes\n
        This allows the user to either test the function to understand its functionality and see what data returns with a call, or collect all of the data from the API.\n

    !!!! WARNING !!!!\n
    This code will take time to collect all the launches due to a built in sleep timer, please make sure your computer
    does not sleep during the running of the code.
    '''
    #Defining a list variable to capture all the launches from the api request
    all_launches = []

    #Also defining the api call count to ensure we don't exceed maximum call count
    api_call_count = 0

    #This will be our all data collection, once mode = 'full collection'
    #if (start_date == 'earliest') and (end_date = 'most recent'):

    # Setting up API parameters
    mode = 'mode=detailed' #setting this mode to detailed returns all related objects
    limit = 'limit=100' #this is the max!
    ordering = 'ordering=net' #orders in ascending date order, I think

    #Assemble the full URL
    current_url = "https://ll.thespacedevs.com/2.3.0/launches/previous/" + "?" + "&".join(
        (mode, limit, ordering)
    )

    if verbose:
        print(f'Query URL: {current_url}') # Visual check

    # Configuration for the data fetch mode
    #TEST_MODE = True  # Set to True for test run, False for full collection

    # Set parameters based on mode
    try:
        if collection_mode == 'test':
            max_calls = 12  # limit to 12 calls for testing
            pause_after_call_num = 4  # pause after 4 calls
            pause_duration_in_seconds = 180  # 3 minutes
        elif collection_mode == 'full collection':
            max_calls = None  # no limit, collect everything
            pause_after_call_num = 14  # pause after 14 calls
            pause_duration_in_seconds = 3630  # 1 hour 30 seconds
        else:
            raise ValueError(f"Invalid mode '{collection_mode}'. Expected 'test' or 'full collection'.")
    except ValueError as e:
        print(e)
        sys.exit(0)
    
    if verbose:
        print(f"Running in {'TEST' if collection_mode == 'test' else 'FULL COLLECTION'} mode")
        print("STARTING DATA ACQUISITION")

    while current_url and (max_calls is None or api_call_count < max_calls):

        if verbose:
            print(f"Request #: {api_call_count + 1}")
        response = requests.get(current_url)

        if response.status_code == 200:

            # Parse the JSON response into a dictionary
            raw_data = response.json()

            # launch records are inside the 'results' key
            # Add the new launches from the dictionary to our sample list
            all_launches.extend(raw_data['results'])

            # THIS IS THE PAGINATION: Get the URL for the next page.
            # If it's the last page, data['next'] will be 'None' and the 'while' loop will stop.
            current_url = raw_data['next']

            if verbose:
                print(f"Success! So far collected {len(all_launches)} total launches.")

            api_call_count += 1

            # pause after specified number calls to comply with rate limits
            if api_call_count % pause_after_call_num == 0 and current_url is not None:

                # Get local region time for pause message
                your_tz = ZoneInfo(time_zone)
                time_in_your_region = datetime.now(your_tz)
                length_of_pause = timedelta(seconds=pause_duration_in_seconds)
                resume_time = time_in_your_region + length_of_pause

                # Output PAUSE message with local Philadelphia time API calls resume
                if verbose:
                    print(f"{api_call_count} CALLS MADE. PAUSING FOR {pause_duration_in_seconds / 60:.0f} MIN.")
                    print(f"Resuming at {resume_time.strftime('%I:%M:%S %p %Z')}")

                time.sleep(pause_duration_in_seconds)

                if verbose:
                    print("RESUMING API CALLS")
        else:
            # If it fails, prints an error and stop
            if verbose:
                print(f"Error! Status code: {response.status_code}")
            current_url = None # Stop the loop

    if verbose:
        print(f"FINISHED: Collected {len(all_launches)} total launches!!!")

    if save:
        launch_save(all_launches, collection_name = 'raw_launch_data')

    return all_launches    




def fetch_launches_by_specific_time_period(net_filter, time_zone = 'America/New_York', collection_mode = 'test', verbose= True):
    '''
    This function is a quick and easy way to request launch data for certain time periods from Launch Library 2.

    '''

    #Defining a list variable to capture all the launches from the api request
    all_launches = []

    #Also defining the api call count to ensure we don't exceed maximum call count
    api_call_count = 0

    #This will be our all data collection, once mode = 'full collection'
    #if (start_date == 'earliest') and (end_date = 'most recent'):

    # Setting up API parameters
    mode = 'mode=detailed' #setting this mode to detailed returns all related objects
    limit = 'limit=100' #this is the max!
    ordering = 'ordering=net' #orders in ascending date order, I think

    #Assemble the full URL
    current_url = "https://ll.thespacedevs.com/2.3.0/launches/previous/" + "?" + "&".join(
        (net_filter, mode, limit, ordering)
    )

    if verbose:
        print(f'Query URL: {current_url}') # Visual check

    # Configuration for the data fetch mode
    #TEST_MODE = True  # Set to True for test run, False for full collection

    # Set parameters based on mode
    try:
        if collection_mode == 'test':
            max_calls = 12  # limit to 12 calls for testing
            pause_after_call_num = 4  # pause after 4 calls
            pause_duration_in_seconds = 180  # 3 minutes
        elif collection_mode == 'full collection':
            max_calls = None  # no limit, collect everything
            pause_after_call_num = 14  # pause after 14 calls
            pause_duration_in_seconds = 3630  # 1 hour 30 seconds
        else:
            raise ValueError(f"Invalid mode '{collection_mode}'. Expected 'test' or 'full collection'.")
    except ValueError as e:
        print(e)
        sys.exit(0)
    
    if verbose:
        print(f"Running in {'TEST' if collection_mode == 'test' else 'FULL COLLECTION'} mode")
        print("STARTING DATA ACQUISITION")

    while current_url and (max_calls is None or api_call_count < max_calls):

        if verbose:
            print(f"Request #: {api_call_count + 1}")
        response = requests.get(current_url)

        if response.status_code == 200:

            # Parse the JSON response into a dictionary
            raw_data = response.json()

            # launch records are inside the 'results' key
            # Add the new launches from the dictionary to our sample list
            all_launches.extend(raw_data['results'])

            # THIS IS THE PAGINATION: Get the URL for the next page.
            # If it's the last page, data['next'] will be 'None' and the 'while' loop will stop.
            current_url = raw_data['next']

            if verbose:
                print(f"Success! So far collected {len(all_launches)} total launches.")

            api_call_count += 1

            # pause after specified number calls to comply with rate limits
            if api_call_count % pause_after_call_num == 0 and current_url is not None:

                # Get local region time for pause message
                your_tz = ZoneInfo(time_zone)
                time_in_your_region = datetime.now(your_tz)
                length_of_pause = timedelta(seconds=pause_duration_in_seconds)
                resume_time = time_in_your_region + length_of_pause

                # Output PAUSE message with local Philadelphia time API calls resume
                if verbose:
                    print(f"{api_call_count} CALLS MADE. PAUSING FOR {pause_duration_in_seconds / 60:.0f} MIN.")
                    print(f"Resuming at {resume_time.strftime('%I:%M:%S %p %Z')}")

                time.sleep(pause_duration_in_seconds)

                if verbose:
                    print("RESUMING API CALLS")
        else:
            # If it fails, prints an error and stop
            if verbose:
                print(f"Error! Status code: {response.status_code}")
            current_url = None # Stop the loop

    if verbose:
        print(f"FINISHED: Collected {len(all_launches)} total launches!!!")

    return all_launches 


def launch_by_year(start_year, end_year, time_zone = 'America/New_York', mode = 'test', verbose=True):

    net_filter = launch_date_filter(start_year, end_year)

    launch_data = fetch_launches_by_specific_time_period(net_filter, time_zone, mode, verbose)

    return launch_data




def launch_update(json_file, end_year = 'most recent',time_zone = 'America/New_York', collection_mode = 'test', verbose = True):
    '''
    This function allows a user to input in their previous json file of launches and it will be able to update the data frame by concatinating
    the recent launches that happened after your previous collection date to your json file.
    '''
    #obtaining the collection date of previous launches to determine our collection start point
    last_collection_date = json_file['collection_date']
    #last_collection_date = json_file['launches'][-1]['net']

    #to avoid grabbing the same lauch we will add 1 second to the previous launch time 


    #Breaking apart the saved json file to only focus on launches to make it easier to append missing values
    launch_data = json_file['launches']

    #obtaining the net filter for updated launches

    #parsing the last collection date to 
    start_time = dateparser.parse(last_collection_date)
    
    if end_year == 'most recent':
        end_time = datetime.now()
    else:
        end_date = f"{end_year}-12-31"
        end_time = dateparser.parse(end_date)

    print(f"Collecting launches from {start_time} to {end_time}")
    #Set the filter parameters with the start and end date:
    net_filters = f'net__gte={start_time.isoformat()}&net__lte={end_time.isoformat()}'

    new_launches = fetch_launches_by_specific_time_period(net_filters, time_zone, collection_mode, verbose)

    new_collection_enddate = new_launches[-1]['net']
    
    updated_launch_data = json_file['launches'] + new_launches

    print('='*40)
    print("UPDATED LAUNCH COLLECTION INFO")
    print('='*40)

    return updated_launch_data




#############To be edited further#############
def launch_save(all_launches, collection_name = 'raw_launch_data'):
    # Add collection metadata
    collector_name = collection_name  # change to your name

    final_data = {
        'collector': collector_name,
        'total_launches': len(all_launches),
        'collection_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'launches': all_launches
    }
    print(f"Saving {len(all_launches)} launches to a file...")

    # 'with open' handles closing the file automatically
    with open(f'raw_baseline_launches_{collector_name}.json', 'w', encoding='utf-8') as f:
        # json.dump writes the list to the file
        json.dump(final_data, f, indent=4)

    print("Save complete!")

"""Stock analysis program for SE 320 - Software Construction
Author: Taylor Hancock
Date:   02/10/2025
Class:  SE320 - Software Construction
Assignment: Assignment 03 - API Requests
"""

from datetime import date
from requests import get

def download_data(ticker: str) -> dict:
    """Downloads historic data about the specified stock price
    
    Argument:
        ticker (string): the ticker code to search for

    Returns:
        Dictionary of json output summarizing stock data for the given ticker
    """
    YEAR_PERIOD = 5

    # capitalize (all ticker names capitalized)
    ticker = ticker.upper()

    # calc start date
    today = date.today()
    start = str(today.replace(year=today.year - YEAR_PERIOD))

    # url handling
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    full_url = base_url + path

    # use a header so it works (otherwise it throws an error)
    response = get(full_url, headers={"User-Agent": "Mozilla/5.0"}).json()

    return response

def process_data(dataset: dict) -> dict:
    """Calculates and returns statistics for closing prices from the dataset

    Argument:
        dataset (dict): dictionary to get the statistics from
    
    Returns:
        Dict containing min, max, average, and median of the closing prices in the provided dataset
    """

    # create list of closing prices for each day in dataset
    closing_data = [float(day['close'][1:]) for day in dataset['data']['tradesTable']['rows']]

    # calculate each statistic
    max_closing = max(closing_data)
    min_closing = min(closing_data)
    avg_closing = sum(closing_data) / len(closing_data)
    med_closing = median(closing_data)

    # turn into dict and return
    return {"max": max_closing, "min": min_closing, "avg": avg_closing, "median": med_closing}     
        
def median(input: list[float]) -> float:
    """Calculates the median value of a list
    
    Arguments:
        input (list of floats): the list of floats to find the median of

    Returns:
        Float containing the median value of the list
    """

    # get size
    input_size = len(input)

    # get half size (cast to int)
    mid_index = int(input_size / 2)

    # sort values
    input.sort()
    
    # if there is a middle value, return it
    if input_size % 2 != 0:
        return input[mid_index]
    
    # if there is not a middle value, return the average of the two middle values
    return (input[mid_index] + input[mid_index + 1]) / 2


if __name__ == "__main__":
    ticker = "LMT"
    data = download_data(ticker)
    closing_stats = process_data(data)
    print(closing_stats)
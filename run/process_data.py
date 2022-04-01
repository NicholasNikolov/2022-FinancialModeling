""""
@author: Nicholas Nikolov

Orchestrator for data processing methods.
"""

import src.data_processing as prc


def process_data(ticker: str):
    print("src.db_connection.process_data")
    '''
    Orchestrate the automated data processing methods. These will properly format data
    for ML applications.
    
    Parameters:
        
    Returns:

    '''

    df = prc.read_format_df(ticker)
    
    df = prc.process_PREV_CLOSE(df)
    
    df = prc.process_OPEN(df)
    
    df = prc.process_DAYS_RANGE(df)
    
    df = prc.process_FIFTY_TWO_WK_RANGE(df)
    
    df = prc.process_TD_VOLUME(df)
    
    df = prc.process_AVERAGE_VOLUME_3MONTH(df)
    
    df = prc.process_MARKET_CAP(df)


    return df


if __name__ == '__main__':
    ### TESTING ###
    df = process_data("AAPL")
    df.head()
    ### TESTING ###

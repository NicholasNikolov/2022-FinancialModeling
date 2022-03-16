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
    df = prc.format_timestamp(df , 'DATE_TIME')

    return df


if __name__ == '__main__':
    ### TESTING ###
    df = process_data("AAPL")
    df.head()
    ### TESTING ###

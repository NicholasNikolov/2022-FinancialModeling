# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:19:48 2022

@author: nikol
"""

import mysql.connector
from numpy import reshape




def connect():
    print("Running src.db_connection.connect()")
    '''
    Establish the database connection for data write and read.
    '''
    connection = mysql.connector.connect(user='root', password='C!@ud1u$',
                                  host='127.0.0.1',
                                  database='yh_finance_db')
    
    return connection

    
def db_read(query , params):
    print("Running src.db_connection.db_write()")
    '''
    Write data to the database. This method only supports single query. The 
    method will open a connection at the start, execute the query, then close
    the connection. To prevent establishing multiple connections, use the 
    batch_query method and provide your queries as a list.
    
    Parameters:
    query (str) : The query being used.
    
    params (list) : List of parameters to use. Will be input into the query.
            Ensure use if the parameters are provided by a user to prevent
            SQL injections.
            
    Returns:
    None
    '''
    
    # Open database connection and declare the cursor.
    db = connect()
    cur = db.cursor(dictionary=True)
    
    # Declare the query and parameters to be used in query execution.
    query = query
    params = params
    
    # Execute query and extract the query select results.
    cur.execute(query , params)
    query_result = cur.fetchall()
    
    db.close()
    
    return query_result


def db_write(query , params):
    # Open database connection and declare the cursor.
    db = connect()
    cur = db.cursor()
    
    # Declare the query and parameters to be used in query execution.
    query = query
    params = params
    
    # Execute query and commit changes to the DB.
    cur.execute(query , params)
    db.commit()
    
    db.close()


def batch_write_query(query , param_list):
    print("Running src.db_connection.batch_query")
    '''
    Run a series of queries from a list. This will open a connection before running
    the series of queries that were passed. At the conclusion of the query runs
    the changes will be committed to the database before closing the connection.
    
    Parameters:
    query_dict (dict) : The dictionary containing the queries and parameters
            associated with the respective queries.
            
    Returns:
    None
    '''
    
    # If a single parameter is passed, clean up for the user. This allows users
    # to pass parameter lists with string entries rather than list of lists.
    # This check will auto format for the user. Note that params must be in
    # the form of a list even if only a single entry.
    if type(param_list[0]) == str:
        param_list = [[entry] for entry in param_list]
    
    db = connect()
    cur = db.cursor()
    
    for params in param_list:
        # Execute the query.
        cur.execute(query , params)
    
    # Commit DB changes.
    db.commit() 
    
    # Close connection
    db.close()
    




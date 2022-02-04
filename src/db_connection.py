# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:19:48 2022

@author: nikol
"""

import mysql.connector




def connect():
    print("Running src.db_connection.connect()")
    '''
    Establish the database connection for data write and read.
    '''
    connection = mysql.connector.connect(user='root', password='C!@ud1u$',
                                  host='127.0.0.1',
                                  database='yh_finance_db')
    
    return connection

    
def db_write(query , params):
    print("Running src.db_connection.db_write()")
    '''
    Write data to the database. This method only supports single row writes.
    '''
    
    # Open database connection and declare the cursor.
    db = connect()
    cur = db.cursor()
    
    # Declare the query and parameters to be used in query execution.
    query = query
    params = params
    
    # Execute query and commit changes to the DB.
    cur.execute(query)
    db.commit()
    
    # Close the connection to preserve the DB.
    db.close()
    
    

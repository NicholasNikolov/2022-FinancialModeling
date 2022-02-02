# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:19:48 2022

@author: nikol
"""

import mysql.connector




def connect():
    connection = mysql.connector.connect(user='root', password='C!@ud1u$',
                                  host='127.0.0.1',
                                  database='yh_finance_db')
    connection.close()
    
connect()
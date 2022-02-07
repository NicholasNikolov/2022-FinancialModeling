### WARNING!! ###
# Method is deprecated and will be removed. This is only
# used for testing and cleaning the DB in early implementations.

# Determine the DB to use
USE yh_finance_db;

# Disable safe updates to prevent error out of deprecated method.
SET SQL_SAFE_UPDATES = 0;

# Reset the count.
SET @count = 0;
UPDATE `financial_data` SET `financial_data`.`ID` = @count:= @count + 1;

# Reset the safe updates to prevent updates without WHERE clause.
SET SQL_SAFE_UPDATES = 1;
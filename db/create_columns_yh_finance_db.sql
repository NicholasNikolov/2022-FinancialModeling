# Column populator for yh_finance_db
ALTER TABLE `yh_finance_db`.`financial_data`
ADD COLUMN `ID` INT NOT NULL AUTO_INCREMENT,
ADD PRIMARY KEY (`ID`),
ADD COLUMN `ticker_symbol_id` VARCHAR(10) NOT NULL,
ADD COLUMN `PREV_CLOSE` VARCHAR(45) NULL AFTER `ticker_symbol_id`,
ADD COLUMN `OPEN` VARCHAR(45) NULL AFTER `PREV_CLOSE`,
ADD COLUMN `BID` VARCHAR(45) NULL AFTER `OPEN`,
ADD COLUMN `ASK` VARCHAR(45) NULL AFTER `BID`,
ADD COLUMN `DAYS_RANGE` VARCHAR(45) NULL AFTER `ASK`,
ADD COLUMN `FIFTY_TWO_WK_RANGE` VARCHAR(45) NULL AFTER `DAYS_RANGE`,
ADD COLUMN `TD_VOLUME` VARCHAR(45) NULL AFTER `FIFTY_TWO_WK_RANGE`,
ADD COLUMN `AVERAGE_VOLUME_3MONTH` VARCHAR(45) NULL AFTER `TD_VOLUME`,
ADD COLUMN `MARKET_CAP` VARCHAR(45) NULL AFTER `AVERAGE_VOLUME_3MONTH`,
ADD COLUMN `BETA_5Y` VARCHAR(45) NULL AFTER `MARKET_CAP`,
ADD COLUMN `PE_RATIO` VARCHAR(45) NULL AFTER `BETA_5Y`,
ADD COLUMN `EPS_RATIO` VARCHAR(45) NULL AFTER `PE_RATIO`,
ADD COLUMN `EARNINGS_DATE` VARCHAR(45) NULL AFTER `EPS_RATIO`,
ADD COLUMN `DIVIDEND_AND_YIELD` VARCHAR(45) NULL AFTER `EARNINGS_DATE`,
ADD COLUMN `EX_DIVIDEND_DATE` VARCHAR(45) NULL AFTER `DIVIDEND_AND_YIELD`,
ADD COLUMN `ONE_YEAR_TARGET_PRICE` VARCHAR(45) NULL AFTER `EX_DIVIDEND_DATE`;

ALTER TABLE `yh_finance_db`.`financial_data` 
CHANGE COLUMN `ID` `ID` INT NOT NULL ,
ADD PRIMARY KEY (`ID`)
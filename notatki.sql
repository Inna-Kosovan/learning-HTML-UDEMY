SELECT COUNT(*) FROM BINANCE_TRADE_ALL;
SELECT COUNT(*) FROM BINANCE_KLINE_ALL;
SELECT * FROM BINANCE_TRADE_ALL;
SELECT * FROM BINANCE_KLINE_ALL;







GRANT SELECT ON BINANCE_TRADE_ALL_SYGNAL TO your_user;
BINANCE_KLINE_ALL

SELECT status FROM v$instance;

SELECT status FROM v$instance;


SELECT *
FROM BINANCE_TRADE_ALL
WHERE (EVENT_TIME >= TO_TIMESTAMP('09/10/23 22:21:20', 'DD/MM/YY HH24:MI:SS'))
  AND (EVENT_TIME >= TO_TIMESTAMP('09/10/23 23:21:20', 'DD/MM/YY HH24:MI:SS'))
  AND (SYMBOL = 'BTCUSDT', 'ETHUSDT')
ORDER BY EVENT_TIME,  SYMBOL;
-----------------------------------------------------------------------------------------------------------------------------
SELECT *   
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME >= TO_TIMESTAMP('02/11/2023 12:39:39', 'DD/MM/YYYY HH24:MI:SS')
AND EVENT_TIME <= TO_TIMESTAMP('03/11/2023 13:39:39', 'DD/MM/YYYY HH24:MI:SS')
AND SYMBOL = 'BTCUSDT' ;

SELECT COUNT(*) 
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME >= TO_TIMESTAMP('11/10/2023 12:39:39', 'DD/MM/YYYY HH24:MI:SS')
AND EVENT_TIME <= TO_TIMESTAMP('11/10/2023 13:39:39', 'DD/MM/YYYY HH24:MI:SS')
AND SYMBOL = 'BTCUSDT' ;

-----------------------------------------------------------------------------------------------------------------------------------------

SELECT COUNT(*)
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME >= TO_TIMESTAMP('11/10/2023 12:39:39', 'DD/MM/YYYY HH24:MI:SS')
AND EVENT_TIME <= TO_TIMESTAMP('11/10/2023 13:39:39', 'DD/MM/YYYY HH24:MI:SS')
AND SYMBOL = 'ETHUSDT';

------------------------------------------------------------------------------------------------------------------------------------------------
SELECT *
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME >= TO_TIMESTAMP('12/10/2023 11:38:37', 'DD/MM/YYYY HH24:MI:SS')
AND EVENT_TIME <= TO_TIMESTAMP('12/10/2023 13:39:37', 'DD/MM/YYYY HH24:MI:SS')
AND SYMBOL = 'ETHUSDT' ;

SELECT *
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME >= TO_TIMESTAMP('10/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS')
AND EVENT_TIME <= TO_TIMESTAMP('11/10/2023 11:38:38', 'DD/MM/YYYY HH24:MI:SS')
AND SYMBOL = 'BTCUSDT' ;

EXEC DBMS_STATS.GATHER_TABLE_STATS('YOUR_SCHEMA_NAME', 'BINANCE_TRADE_ALL');

CREATE INDEX index_name
ON BINANCE_TRADE_ALL (PRICE);

CREATE INDEX IDX_QUANTITY
ON BINANCE_TRADE_ALL (QUANTITY);

CREATE INDEX index_name
ON BINANCE_TRADE_ALL (PRICE, QUANTITY)
ONLINE;


-- Step 1 & 2: Create a copy of the table with a new name and filtered data
CREATE TABLE BINANCE_TRADE_ALL_SYGNAL AS
SELECT *
FROM BINANCE_TRADE_ALL
WHERE 
    EVENT_TIME BETWEEN TO_DATE('10/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS') 
                 AND TO_DATE('11/10/2023 11:38:38', 'DD/MM/YYYY HH24:MI:SS')
    AND SYMBOL = 'BTCUSDT';

-- Step 3: Add a new column to the new table
ALTER TABLE BINANCE_TRADE_ALL_SYGNAL
ADD (SYGNAL NUMBER); 
-- Adjust the datatype and size as per your needs








DROP TABLE BINANCE_TRADE_ALL_SYGNAL;












DROP INDEX IDX_EVENT_SYMBOL_TIME;

CREATE INDEX IDX_EVENT_TIME
ON BINANCE_TRADE_ALL (EVENT_TIME);


SELECT /*+ INDEX(a IDX_QUANTITY) INDEX(a IDX_PRICE) INDEX(a IDX_SYMBOL) INDEX(a IDX_EVENT_TIME) */ *
FROM BINANCE_TRADE_ALL a
WHERE a.EVENT_TIME BETWEEN TO_TIMESTAMP('{start_time_str}', 'DD/MM/YYYY HH24:MI:SS')
AND TO_TIMESTAMP('{end_time_str}', 'DD/MM/YYYY HH24:MI:SS')
AND a.SYMBOL = '{symbol}';
   











SELECT OWNER, TABLE_NAME 
FROM ALL_TABLES 
WHERE TABLE_NAME = 'BINANCE_TRADE_ALL';

EXEC DBMS_STATS.GATHER_TABLE_STATS('BIADM', 'BINANCE_TRADE_ALL');


CREATE INDEX idx_event_symbol_time 
ON BINANCE_TRADE_ALL(SYMBOL, EVENT_TIME);

SELECT /*+ INDEX(a idx_event_symbol_time) */ 
       *
FROM BINANCE_TRADE_ALL a
WHERE a.EVENT_TIME BETWEEN TO_TIMESTAMP('10/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS') 
                      AND TO_TIMESTAMP('11/10/2023 11:38:38', 'DD/MM/YYYY HH24:MI:SS')
      AND a.SYMBOL = 'BTCUSDT';

SELECT /*+ INDEX(a idx_event_symbol_time) */ 
           *
        FROM BINANCE_TRADE_ALL a
        WHERE a.EVENT_TIME BETWEEN TO_TIMESTAMP('10/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS') 
        AND TO_TIMESTAMP('11/10/2023 11:38:38', 'DD/MM/YYYY HH24:MI:SS')
        AND a.SYMBOL = 'BTCUSDT';
SELECT /*+ INDEX(a idx_event_symbol_time) */
           *
        FROM BINANCE_TRADE_ALL a
        WHERE a.EVENT_TIME BETWEEN TO_TIMESTAMP('10/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS') 
        AND TO_TIMESTAMP('11/10/2023 11:38:38', 'DD/MM/YYYY HH24:MI:SS')
        AND a.SYMBOL = 'BTCUSDT';
SELECT * FROM ALL_INDEXES;
SELECT * FROM USER_INDEXES;
SELECT * FROM DBA_INDEXES;


SELECT * FROM ALL_IND_COLUMNS WHERE TABLE_NAME = 'BINANCE_TRADE_ALL';
SELECT * FROM USER_IND_COLUMNS WHERE TABLE_NAME = 'BINANCE_TRADE_ALL';

CREATE INDEX index_name
ON BINANCE_TRADE_ALL (QUANTITY);

--------------------------------------------------------------------------------------------------------------------
--Если вы хотите получить данные за предыдущие 24 часа на основе столбца EVENT_TIME, !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
--получить общее количество часов для этих данных и отфильтровать по столбцу SYMBOL
--со значением BTCUSDTиз BINANCE_TRADE_ALLтаблицы в базе данных Oracle, вы можете использовать следующий запрос:
------------------------------------------------------------------------------------------------------
SELECT EVENT_TIME, 
       24 AS TOTAL_HOURS,
       SYMBOL
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '1' DAY) AND SYSDATE
AND SYMBOL = 'BTCUSDT';
------------------------------------------------------------------------------------------------------------
-- TOTAL_ROWS+TOTAL_HOURS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WITH DateRangeData AS (
    SELECT EVENT_TIME, SYMBOL
    FROM BINANCE_TRADE_ALL
    WHERE EVENT_TIME > TO_DATE('10/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS')
    AND EVENT_TIME < TO_DATE('11/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS')
    AND SYMBOL = 'BTCUSDT'
)
SELECT 24 AS TOTAL_HOURS,  -- Assuming the range is 24 hours given your provided dates
       COUNT(*) AS TOTAL_ROWS
FROM DateRangeData;
-------------------------------------------------------------------------------------------------------------------------
-- мне нужен запрос для oracle столбец EVENT_TIME  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
--FROM таблцы BINANCE_TRADE_ALL вывести данные за >10.10.2023 11:37:37 и  < 11.10.2023 11:37:37
--напиши пример такого запроса для моих данных и сделать отбор по столбику symbol BTCUSDT
SELECT EVENT_TIME, SYMBOL
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME > TO_DATE('10/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS')
AND EVENT_TIME < TO_DATE('11/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS')
AND SYMBOL = 'BTCUSDT';
---------------------------------------------------------------------------------------------------------------
-- мне нужен запрос для oracle столбец EVENT_TIME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
--FROM таблцы BINANCE_TRADE_ALL   вывести все данные за >10.10.2023 11:37:37 и  < 11.10.2023 11:37:37
--напиши пример такого запроса для моих данных и сделать отбор по столбику symbol BTCUSD

SELECT *
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME > TO_DATE('10/10/2023 11:37:36', 'DD/MM/YYYY HH24:MI:SS')
AND EVENT_TIME < TO_DATE('11/10/2023 11:37:36', 'DD/MM/YYYY HH24:MI:SS')
AND SYMBOL = 'BTCUSDT';
--------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
--!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
-- мне нужен запрос для oracle столбец EVENT_TIME FROM таблцы BINANCE_TRADE_ALL 
-- вывести все строки и с указанием номеров строк за >10.10.2023 11:37:37 и  < 11.10.2023 11:37:37
-- отбор по столбику symbol BTCUSDT
WITH DateRangeData AS (
    SELECT EVENT_TIME, SYMBOL
    FROM BINANCE_TRADE_ALL
    WHERE EVENT_TIME > TO_DATE('10/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS')
    AND EVENT_TIME < TO_DATE('11/10/2023 11:37:37', 'DD/MM/YYYY HH24:MI:SS')
    AND SYMBOL = 'BTCUSDT'
)
SELECT ROW_NUMBER() OVER (ORDER BY EVENT_TIME) AS ROW_NUM, 
       EVENT_TIME, 
       SYMBOL,
       24 AS TOTAL_HOURS, 
       (SELECT COUNT(*) FROM DateRangeData) AS TOTAL_ROWS
FROM DateRangeData;
-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- oracle sql как мне получить в таблице BINANCE_KLINE_DATA_25_27_09 строки от 40 000 до 48000 по столбцу EVENT_TIME
SELECT *FROM ( SELECT t.*, ROW_NUMBER() OVER (ORDER BY EVENT_TIME) AS rn
    FROM BINANCE_TRADE_ALL t) WHERE rn BETWEEN 1 AND 1200000
AND SYMBOL = 'BTCUSDT';

WITH Previous24HoursData AS (
    SELECT EVENT_TIME, SYMBOL
    FROM BINANCE_TRADE_ALL
    WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '1' DAY) AND SYSDATE
    AND SYMBOL = 'BTCUSDT'
)
SELECT EVENT_TIME, 
       SYMBOL,
       24 AS TOTAL_HOURS,
       (SELECT COUNT(*) FROM Previous24HoursData) AS TOTAL_ROWS
FROM Previous24HoursData
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- данные за 1 день по столбцу
SELECT EVENT_TIME
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '1' DAY) AND SYSDATE;

-- данные за предыдущий  1 день по столбцу
SELECT EVENT_TIME
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '2' DAY) AND (SYSDATE - INTERVAL '1' DAY);

-- Counting the number of rows TOTAL_ROWS  количество строк
SELECT COUNT(*) AS TOTAL_ROWS
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '2' DAY) AND (SYSDATE - INTERVAL '1' DAY);

-- Retrieving the data
SELECT EVENT_TIME
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '2' DAY) AND (SYSDATE - INTERVAL '1' DAY);

-- Counting the number of rows
SELECT COUNT(*) AS TOTAL_ROWS
FROM BINANCE_TRADE_ALL
WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '2' DAY) AND (SYSDATE - INTERVAL '1' DAY);

--все столбцы из такой таблицы
--самый простой вид шаблона,где (*) означает все колонки

SELECT * FROM BINANCE_KLINE_DATA;
-- выбери все столбцы из такой таблицы
--самый простой вид шаблона,где (*) означает все колонки

-- посмотреть сколько строк в таблице


SELECT COUNT(*) FROM BINANCE_KLINE_DATA_25_27_09;

-- посмотреть сколько строк в таблице
SELECT COUNT(*) FROM PREDICT_25_27_09;
  
-- oracle sql как мне получить в таблице BINANCE_KLINE_DATA_25_27_09 строки от 40 000 до 48000 по столбцу EVENT_TIME
SELECT *FROM ( SELECT t.*, ROW_NUMBER() OVER (ORDER BY EVENT_TIME) AS rn
    FROM BINANCE_TRADE_ALL t) WHERE rn BETWEEN 1 AND 1200000;


-- oracle sql как мне получить в таблице BINANCE_KLINE_DATA_25_27_09 строки от 40 000 до 48000 по столбцу EVENT_TIME

 SELECT * 
        FROM ( 
            SELECT t.*, ROW_NUMBER() OVER (ORDER BY EVENT_TIME) AS rn
            FROM BINANCE_KLINE_DATA_25_27_09 t 
        )  
        WHERE rn BETWEEN 53607 AND 56331;

DESCRIBE BINANCE_KLINE_DATA_25_27_09;

SELECT value FROM v$parameter WHERE name='service_names';

as sysdba

SELECT EVENT_TIME, OPEN_PRICE FROM BINANCE_KLINE_DATA_25_27_09;

SELECT * 
FROM ( 
    SELECT t.*, ROW_NUMBER() OVER (ORDER BY EVENT_TIME) AS rn
    FROM PREDICT_25_27_09 t 
)  
WHERE rn BETWEEN 48008 AND 56331


SELECT COUNT(*) FROM PREDICT_25_27_0


SELECT instance_name FROM v$instance;

SELECT instance_name FROM v$instance;

SELECT * FROM (SELECT * FROM PREDICT_25_27_09 ORDER BY EVENT_TIME) WHERE ROWNUM >= 41008;


SELECT NAME, DB_UNIQUE_NAME FROM V$DATABASE;

SELECT EVENT_TIME, OPEN_PRICE, CLOSE_PRICE, HIGH_PRICE, LOW_PRICE FROM BINANCE_KLINE_DATA_25_27_09;

SELECT ROWNUM, OPEN_PRICE FROM BINANCE_KLINE_DATA_25_27_09 WHERE ROWNUM <= 100;


WITH 
  -- Generate a series of minutes within the specified time range
  MinuteSeries AS (
    SELECT 
      TO_TIMESTAMP('25.09.2023 22:00:00', 'DD.MM.YYYY HH24:MI:SS') + NUMTODSINTERVAL(level - 1, 'MINUTE') AS minute
    FROM 
      dual
    CONNECT BY 
      TO_TIMESTAMP('25.09.2023 22:00:00', 'DD.MM.YYYY HH24:MI:SS') + NUMTODSINTERVAL(level - 1, 'MINUTE') <= TO_TIMESTAMP('25.09.2023 23:59:59', 'DD.MM.YYYY HH24:MI:SS')
  )
SELECT
  ms.minute,
  -- Get the opening price, closing price, max high price, min low price, total volume, and total number of trades for each minute
  MIN(CASE WHEN TO_TIMESTAMP(KLINE_START_TIME, 'DD.MM.YYYY HH24:MI:SS') = ms.minute THEN OPEN_PRICE END) AS OPEN_PRICE_AT_START_MINUTE,
  MAX(CASE WHEN TO_TIMESTAMP(KLINE_END_TIME, 'DD.MM.YYYY HH24:MI:SS') = ms.minute + NUMTODSINTERVAL(1, 'MINUTE') THEN CLOSE_PRICE END) AS CLOSE_PRICE_AT_END_MINUTE,
  MAX(HIGH_PRICE) AS MAX_HIGH_PRICE,
  MIN(LOW_PRICE) AS MIN_LOW_PRICE,
  SUM(VOLUME) AS TOTAL_VOLUME,
  SUM(NUMBER_OF_TRADES) AS TOTAL_NUMBER_OF_TRADES
FROM
  HR.BINANCE_KLINE_DATA_25_27_09
JOIN
  MinuteSeries ms
ON
  TO_TIMESTAMP(KLINE_START_TIME, 'DD.MM.YYYY HH24:MI:SS') >= ms.minute
AND
  TO_TIMESTAMP(KLINE_START_TIME, 'DD.MM.YYYY HH24:MI:SS') < ms.minute + NUMTODSINTERVAL(1, 'MINUTE')
GROUP BY
  ms.minute
ORDER BY
  ms.minute;























































--читаем выведи мне информацию колонок region_id, country_name из таблицы countries
SELECT region_id, country_name FROM countries;

select to_char(sysdate, 'dd-mm-rr hh24:mi:ss') from dual;
--вытягиваем время текущее( которое сейчас на сервере)

select sysdate, sysdate + 5, sysdate + 5.5 from dual;


select * from BINANCE_KLINE_DATA_25_27_09 where kline_price  is null;
--читаем вывести информацию о работниках в которых нет комиссионных

--Вот пример, в котором строки сортируются гипотетически date_column 
--по возрастанию перед выбором первых 4000:
--Замените date_column
--фактическим именем столбца, по которому вы хотите выполнить сортировку.
SELECT * FROM  BINANCE_KLINE_DATA_25_27_09 ORDER BY EVENT_TIME  ASC
FETCH FIRST 4000 ROWS ONLY;

WITH Previous24HoursData AS (
    SELECT EVENT_TIME
    FROM BINANCE_TRADE_ALL
    WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '2' DAY) AND (SYSDATE - INTERVAL '1' DAY)
)
SELECT EVENT_TIME, 24 AS TOTAL_HOURS
FROM Previous24HoursData;


WITH Previous24HoursData AS (
    SELECT EVENT_TIME
    FROM BINANCE_TRADE_ALL
    WHERE EVENT_TIME BETWEEN (SYSDATE - INTERVAL '2' DAY) AND (SYSDATE - INTERVAL '1' DAY)
)
SELECT EVENT_TIME, 24 AS TOTAL_HOURS
FROM Previous24HoursData;


















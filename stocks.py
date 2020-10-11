# https://rapidapi.com/signup

import yfinance as yf
from datetime import datetime, timedelta
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# stocks = "MSFT AAPL GOOG TSLA AMZN FB KIRK V MA UNH NFLX CRM NKE HD COST KO AMT LOW UPS ZM MMM"
#data = yf.download(stocks, start=start, end=end, interval='5m', group_by='ticker')


class DataDownloader:
    def __init__(self, stocks):
        self.stocks = stocks
        self.raw_data = None
        self.transformed_data = None
        self.interval = '5m'
        self.end = datetime.utcnow()
        self.start = self.end - timedelta(7)
        self.PSQL = None

    def get_data(self, start=None, end=None, interval=None):
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        if interval is not None:
            self.interval = interval
        self.raw_data = yf.download(self.stocks, start=self.start, end=self.end, interval=self.interval, group_by='ticker')

    def transform_data(self):
        self.transformed_data = self.raw_data[[x for x in self.raw_data.columns if x[1] == 'Close']]
        self.transformed_data.columns = [x[0] for x in self.raw_data.columns if x[1] == 'Close']
        self.transformed_data = self.transformed_data.melt(ignore_index=False)
        self.transformed_data.columns = ['symbol', 'price']
        self.transformed_data = self.transformed_data.sort_values('symbol')

    def get_PSQL(self, dbname, user, host, password):
        self.PSQL = PSQLConnector(dbname, user, host, password)

    def insert_SQL(self, table=None):
        drop_table_sql = """drop table StockPrice;"""

        create_table_sql = """CREATE TABLE StockPrice (
        id serial PRIMARY KEY,
        datetime TIMESTAMP,
        symbol VARCHAR ( 10 ),
        price FLOAT
        );"""

        insert_sql = """INSERT INTO {0} (datetime, symbol, price) VALUES {1};"""

        if self.PSQL is None:
            self.get_PSQL('stocks', 'postgres', 'localhost', 'password')
        if table is None:
            table = 'stockprice'
        if self.raw_data is None:
            self.get_data()
        # Get values to be inserted for each time and stock
        values = ""
        for sym in self.stocks.split():
            tmp = self.raw_data[sym]['Close']
            for ts in tmp.index:
                values += "('{0}', '{1}', {2}),".format(ts, sym, tmp.loc[ts])
        values = ''.join(list(values)[0:-1])
        # remove old table
        self.PSQL.execute(drop_table_sql)
        # create fresh
        self.PSQL.execute(create_table_sql)
        # insert data
        self.PSQL.execute(insert_sql.format(table, values))
        # commit
        self.PSQL.cur.execute('COMMIT')

    def read_SQL(self, table):
        if self.PSQL is None:
            self.get_PSQL('stocks', 'postgres', 'localhost', 'password')
        sql = """SELECT * from {0};""".format(table)
        self.PSQL.execute(sql)
        self.transformed_data = pd.DataFrame(self.PSQL.cur.fetchall())
        self.transformed_data.drop(0, axis=1, inplace=True)
        self.transformed_data.columns = ['DateTime', 'symbol', 'price']
        self.transformed_data.set_index('DateTime', inplace=True)
        self.transformed_data = self.transformed_data.sort_values('symbol')

    def plot_raw(self, metric='Close', scale=None):
        #scale is the value at index 'scale' by which to scale each series by. 0 is first value, -1 is last
        for stock in self.stocks.split():
            values = self.raw_data[stock][metric]
            if scale is not None:
                values = values / values.iloc[scale]
            plt.plot(values.index, values.values, '-', label=stock, alpha=.5)
            plt.plot()
        plt.xticks(rotation=90)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=int(len(self.stocks.split()) / 10) + 1)
        plt.show()


class PSQLConnector:
    def __init__(self, dbname, user, host, password):
        self.conn = psycopg2.connect("dbname={0} \
        user={1} \
        host={2} \
        password={3}".format(dbname, user, host, password))
        self.cur = self.conn.cursor()

    def execute(self, sql):
        self.cur.execute(sql)



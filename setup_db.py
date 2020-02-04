import sqlite3
import pandas as pd
import json



#CODE TO INITIALIZE DATABASE
sql = "CREATE TABLE homes (id INTEGER PRIMARY KEY, name TEXT, host_id INTEGER,"\
        " host_name TEXT, neighbourhood_group TEXT, neighbourhood TEXT, latitude INTEGER,"\
        " longitude INTEGER, room_type TEXT, price INTEGER, minimum_nights INTEGER,"\
        " number_of_reviews INTEGER, last_review DATE, reviews_per_month DECIMAL(4,2),"\
        " calculated_host_listings_count INTEGER, availability_365 INTEGER);"

cur.execute(sql)


df = pd.read_csv(r'AB_NYC_2019.csv')
df.to_sql('homes', con=conn, if_exists='replace', index=False)


cur.execute("select * from homes limit 5;")

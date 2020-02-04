import os
from flask import Flask, request, jsonify
import sqlite3
import json

# Init App
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


# @app.route('/', methods = ['GET'])
# def index():
#     results = db.session.query(rooms).all()
#     for r in results:
#         print(r.name)
#     return ''

@app.route('/closest_rooms', methods = ['GET'])
def closest_rooms():

    query = request.args.get('query')
    long = request.args.get('long')
    lat = request.args.get('lat')
    print('params', query, long, lat)

    if lat and long and not query:
        rooms = find_closest_apartments(lat, long)

    if query and not (lat and long):
        rooms = query_search(query)

    if lat and long and query:
        rooms = find_closest_off_query(lat, long, query)

    if not lat and not long and not query:
        return 'please enter coordinates and/or query string'

    if (not lat and long) or (not long and lat):
        return 'please enter both longitude and latitude'

    return jsonify({'rooms': rooms})


def find_closest_apartments(source_latitude,source_longitude):
    #Finds closest apartments based soley off of coordinates

    conn = sqlite3.connect('rent.sqlite3')

    conn.enable_load_extension(True)
    conn.load_extension("extension-functions.so")
    cur = conn.cursor()

    sql_query = '''

        select
        name as HouseName,
        2 * 3961 *
        asin(
            sqrt(
                (sin(radians(({lat2} - latitude) / 2)))*(sin(radians(({lat2} - latitude) / 2))) +
                (cos(radians(latitude)) * cos(radians({lat2})) *
                    (sin(radians(({lon2} - longitude) / 2)))*(cos(radians(latitude)) * cos(radians({lat2})) *
                        (sin(radians(({lon2} - longitude) / 2)))))
                )
            )as distance,
        neighbourhood, room_type, price
        from homes
        order by 2 asc
        limit 10;

    '''.format(lat2=source_latitude,lon2=source_longitude)
    cur.execute(sql_query)
    all_rows = cur.fetchall()
    room_list = []
    for name, distance, neighbourhood, room_type, price in all_rows:
        room_info = {}
        room_info['name'] = name
        room_info['distance'] = distance
        room_info['neighbourhood'] = neighbourhood
        room_info['room_type'] = room_type
        room_info['price'] = price
        room_list.append(room_info)

    cur.close()
    conn.close()

    return room_list

def query_search(query_string):
    #Finds appartments based soley off of user input search
    query = ""
    col_name = "name"
    for word in query_string.split(): query +=  col_name + " like \'%"+word +"%\' or "
    query = query[:-4]

    conn = sqlite3.connect('rent.sqlite3')

    conn.enable_load_extension(True)
    conn.load_extension("extension-functions.so")
    cur = conn.cursor()

    sql_query = '''

        select
        name, neighbourhood, room_type, price
        from homes
        where {query_name}
        limit 10;

    '''.format(query_name=query)
    cur.execute(sql_query)
    all_rows = cur.fetchall()
    room_list = []
    for name, neighbourhood, room_type, price in all_rows:
        room_info = {}
        room_info['name'] = name
        room_info['neighbourhood'] = neighbourhood
        room_info['room_type'] = room_type
        room_info['price'] = price
        room_list.append(room_info)

    cur.close()
    conn.close()

    return room_list

def find_closest_off_query(source_latitude, source_longitude, query_string):
    # Finds closest appartments to coordinates from a query search based off user input search
    query = ""
    col_name = "name"
    for word in query_string.split(): query +=  col_name + " like \'%"+word +"%\' or "
    query = query[:-4]
    print(query)

    conn = sqlite3.connect('rent.sqlite3')

    conn.enable_load_extension(True)
    conn.load_extension("extension-functions.so")
    cur = conn.cursor()

    sql_query = '''

        select
        name,
        2 * 3961 *
        asin(
            sqrt(
                (sin(radians(({lat2} - latitude) / 2)))*(sin(radians(({lat2} - latitude) / 2))) +
                (cos(radians(latitude)) * cos(radians({lat2})) *
                    (sin(radians(({lon2} - longitude) / 2)))*(cos(radians(latitude)) * cos(radians({lat2})) *
                        (sin(radians(({lon2} - longitude) / 2)))))
                )
            )as distance,
        neighbourhood, room_type, price
        from homes
        where name in (
            select
            name
            from homes
            where {query_name}
        )
        order by 2 asc
        limit 10;

    '''.format(query_name=query, lat2=source_latitude, lon2=source_longitude)

    cur.execute(sql_query)
    all_rows = cur.fetchall()
    room_list = []
    for name, distance, neighbourhood, room_type, price in all_rows:
        room_info = {}
        room_info['name'] = name
        room_info['distance'] = distance
        room_info['neighbourhood'] = neighbourhood
        room_info['room_type'] = room_type
        room_info['price'] = price
        room_list.append(room_info)

    cur.close()
    conn.close()

    return room_list

# Run Server
if __name__ == '__main__':
    app.run(debug=True)

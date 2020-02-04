# Room4RentNYC

Start app by running python app.py (need python3)

To access rest api use a GET request on localhost:5000/closest_rooms with the following parameters:

long, lat, query

If using coordinates, please pass in both long and lat. If using query please pass in a search phrase.

You can use coordinates and/or query string.

Example requests:

localhost:5000/closest_rooms?query=empire&long=-73&lat=40
localhost:5000/closest_rooms?long=-73&lat=40
localhost:5000/closest_rooms?query=empire

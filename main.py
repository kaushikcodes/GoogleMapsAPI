import flask
from pprint import pprint as pp
import datetime
import time
import googlemaps
import csv
import os
API_KEY = 'AIzaSyDVsN12nDgOacsNQaFMRM-c8cUyHpnHvvo'

app = flask.Flask(__name__)
gmaps = googlemaps.Client(key=API_KEY)

@app.route("/", methods=['GET', 'POST'])
def form():
    return flask.render_template('./input.html')

@app.route("/directions", methods=['GET', 'POST'])
def caller():
    print("entered")
    origin = flask.request.form['origin']
    destination = flask.request.form['destination']
    if origin == destination:
        raise ValueError('Cannot enter same origin and destination')
    placedict = food_places(origin, destination)
    distdictionary = compute_distance(origin, destination)

    with open("downloaded.csv", 'w') as csvfile:
        write_to = csv.writer(csvfile)
        csv_columns = ['Directions','Distance']
        write_to.writerow(csv_columns)
        for key, val in distdictionary.items():
            write_to.writerow([key, val])

        write_to.writerow(["---------", "----------"])
        write_to.writerow(["Food Places in the proximity: "])
        write_to.writerow(["Name of place", "Rating of place"])
        for key, val in placedict.items():
            write_to.writerow([key, val])
    return flask.render_template('output.html', dirdict = distdictionary, placedict = placedict)

def compute_distance(origin, destination):
    now = time.time()
    directions_result = gmaps.directions(destination,
                                         origin,
                                         mode="walking",
                                         departure_time=now)
    #pp(directions_result)

    dirdict = {}
    stepdict = directions_result[0]['legs'][0]['steps']

    for i in range(len(stepdict)):
        dist = stepdict[i]['distance']['text']
        instr = stepdict[i]['html_instructions']
        dirdict[instr] = dist

    pp(dirdict)
    return dirdict

def food_places(origin, destination):
    temp1 = gmaps.geocode(origin)
    if len(temp1) == 0:
        raise ValueError("No origin found")
    temp = gmaps.geocode(destination)
    if len(temp) == 0:
        raise ValueError("No destination found")
    else:
        latitude = temp[0]['geometry']['location']['lat']
        long = temp[0]['geometry']['location']['lng']
        loc = str(latitude) + ', ' + str(long)
        places_result = gmaps.places_nearby(
            location=loc, radius=100, type='food')

        placedict = {}
        resdict = places_result['results']
        lst = []
        for i in range(len(resdict)):
            keyss = resdict[i].keys()
            if('rating' in keyss) and ('user_ratings_total' in keyss):
                name = resdict[i]['name']
                rating = resdict[i]['rating']
                if(rating > 3.5):
                    #print(name)
                    if (len(placedict) != 11):
                        placedict[name] = rating

        pp(placedict)
        return placedict #again render

@app.route("/convert", methods=['GET', 'POST'])
def convert():
    return flask.send_from_directory(os.getcwd(), "downloaded.csv")


if __name__ == '__main__':
    app.run(port=8001, host='127.0.0.1', debug=True, use_evalex=False)

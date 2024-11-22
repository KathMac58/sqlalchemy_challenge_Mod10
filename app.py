# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
# Create an app
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
# Add Endpoint called /
@app.route("/")
def home():
    # List all available routes
    print("Server received request for homepage...")
    return(
        f"Hi! Welcome to the Module 10 SQLAlchemy API!<br/>"
        f"Available Routes:<br/>"
        f"Daily Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Weather Stations: /api/v1.0/stations<br/>"
        f"Temperature Observations for 'USC00519281' from Previous Year: /api/v1.0/tobs<br/>"
        f"Min, Avg, Max Temp of Date: /api/v1.0/<start><br/>"
        f"Min, Avg, Max Temp of Dates: /api/v1.0/<start>/<end><br/>"
    )

#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/precipitation")
def Precipitation():

    # Create session - link Python to DB
    session = Session(engine)

    # Return Precipitation (prcp) data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-24").all()

    session.close()

    # Convert the list above to a dictionary
    prcp_values = []
    for date, prcp in results:
        prcp_dictionary = {}
        prcp_dictionary["date"] = date
        prcp_dictionary["prcp"] = prcp
        prcp_values.append(prcp_dictionary)
    return jsonify(prcp_values)

##########
@app.route("/api/v1.0/stations")
def Stations():

    # Create session - link Python to DB
    session = Session(engine)

    # Return List of Stations in Hawaii
    results = session.query(Measurement.station).order_by(Measurement.station).all()

    session.close()

    # Convert Stations to regular list
    station_list = list(np.ravel(results))

    ##return jsonify(station_list)
    return jsonify(station_list)

##########
@app.route("/api/v1.0/tobs")
def Tobs():

    # Create session - link Python to DB
    session = Session(engine)

    # Return TOBS list
    # The most active station is 'USC00519281'
    # The most recent date in the data set is:  2017-08-23
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station == 'USC00519281').\
                order_by(Measurement.date).all()
    
    session.close()

    #Convert the list above to a dictionary
    tobs_values = []
    for prcp, date, tobs in results:
        tobs_dictionary = {}
        tobs_dictionary["prcp"] = prcp
        tobs_dictionary["date"] = date
        tobs_dictionary["tobs"] = tobs
        tobs_values.append(tobs_dictionary)
        return jsonify(tobs_values)

##########
@app.route("/api/v1.0/<start><br/>")
def start(start_date):

    # Create session - link Python to DB
    session = Session(engine)

    # Return list, by a given start date, of min/max/avg tobs
    results = session.query(func.min(Measurement.tobs),\
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs)).filter(Measurement.station >= start_date).all()
    
    session.close()

    # Create a dictionary
    tobs_start_date = []
    for min, max, avg, in results:
        tobs_start_dictionary = {}
        tobs_start_dictionary["min_temp"] = min
        tobs_start_dictionary["max_temp"] = max
        tobs_start_dictionary["avg_temp"] = avg
        tobs_start_date.append(tobs_start_dictionary)
    return jsonify(tobs_start_date)

##########
@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):

    # Create session - link Python to DB
    session = Session(engine)

    # Return list, by a given start and end date, of min/max/avg tobs
    results = session.query(func.min(Measurement.tobs),\
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date).\
                            filter(Measurement.date <= end_date).all()
    session.close()

   # Create a dictionary
    tobs_start_end_date = []
    for min, max, avg, in results:
        tobs_start_end_dictionary = {}
        tobs_start_end_dictionary["min_temp"] = min
        tobs_start_end_dictionary["max_temp"] = max
        tobs_start_end_dictionary["avg_temp"] = avg
        tobs_start_date.append(tobs_start_dictionary)
    return jsonify(tobs_start_date)
 
if __name__ == "__main__":
    app.run(debug=True)


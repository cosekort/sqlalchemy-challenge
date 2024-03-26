# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measure_ref = Base.classes.measurement
station_ref = Base.classes.station 

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    
    # Query precipitation results

    prcp_scores = session.query(measure_ref.date, measure_ref.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precip = []
    for date, precipitation in prcp_scores:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = precipitation
        all_precip.append(precipitation_dict)
    return jsonify(all_precip)


    
@app.route("/api/v1.0/stations")
def stations(): 
    # Create our session (link) from Python to the DB
    session = Session(engine) 

    # Query station results 

    total_stations = session.query(station_ref.station,station_ref.id).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station, id in total_stations:
      station_dict = {}
      station_dict["station"] = station
      station_dict["id"] = id
      all_stations.append(station_dict)
      return jsonify(all_stations)


    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    
    one_year_prior = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    #Query tobs results
    temp_data = session.query(measure_ref.tobs).\
    filter(measure_ref.date >= one_year_prior).\
    filter(measure_ref.station == 'USC00519281').all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for tobs, date, station in temp_data:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["tobs"] = tobs
        tobs_dict["date"] = date 
        all_tobs.append(tobs_dict)
        return jsonify(all_tobs)
    
@app.route("/api/v1.0/<start>")
def start_date():
    # Create our session (link) from Python to the DB
    session = Session(engine) 
   
    start = dt.date(2017, 8, 23)
    
    #Query tobs results
    start_date = session.query(func.min(measure_ref.tobs), func.max(measure_ref.tobs), func.avg(measure_ref.tobs)).\
    filter(measure_ref.date >= start).all()
    
    # Create a dictionary from the row data and append to a list of all_passengers
    start_date_data = []
    for min,max,avg in start_date:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["average"] = avg
        start_date_data.append(start_dict)
        return jsonify(start_date)
    
@app.route("/api/v1.0/<start>/<end>")
def to_end():
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    
    start = dt.date(2017, 8, 23)
    end = dt.date(2010,1,1)
    #Query tobs results
    end_date = session.query(func.min(measure_ref.tobs), func.max(measure_ref.tobs), func.avg(measure_ref.tobs)).\
    filter(measure_ref.date >= start).\
    filter(measure_ref.date <= end).all() 

    
    # Create a dictionary from the row data and append to a list of all_passengers
    end_date_data = []
    for min, max, avg in end_date:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        end_date_data.append(end_date)
        return jsonify(end_date)
    

if __name__ == '__main__':
    app.run(debug=True)

        
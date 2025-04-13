# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


#################################################
# Database Setup
#################################################


engine = create_engine("sqlite:///Resources/hawaii.sqlite") # Create engine to hawaii.sqlite

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# API Homepage
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Find most recent date and calculate one year ago
    recent = session.query(func.max(Measurement.date)).scalar()
    year_ago = dt.datetime.strptime(recent, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query for last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    session.close()

    # Convert to dictionary with date as key
    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)                                                    #jsonify the data


# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Query all station names
    results = session.query(Station.station).all()
    session.close()

    # Flatten and return as JSON list
    station_list = list(np.ravel(results))
    return jsonify(station_list)                                                         


# Temperature Observations Route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Find most recent date and most active station
    recent = session.query(func.max(Measurement.date)).scalar()
    year_ago = dt.datetime.strptime(recent, "%Y-%m-%d") - dt.timedelta(days=365)

    top_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count().desc()).first()[0]

    # Query temp observations from top station
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == top_station)\
        .filter(Measurement.date >= year_ago).all()
    session.close()

    # Return list of observations
    tobs_list = [{date: temp} for date, temp in results]
    return jsonify(tobs_list)


# Start Date Route (Min, avg, Max from strt to latest date)
@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    session = Session(engine)

    # Query min, avg, max for dates >= start
    stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).first()
    session.close()

    return jsonify({"TMIN": stats[0], "TAVG": round(stats[1], 1), "TMAX": stats[2]})


# Start and End Date Route (Min, avg, Max from strt to end date)
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_range(start, end):
    session = Session(engine)

    # Query min, avg, max for range
    stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).first()
    session.close()

    return jsonify({"TMIN": stats[0], "TAVG": round(stats[1], 1), "TMAX": stats[2]})

# Run app
if __name__ == "__main__":
    app.run(debug=True)
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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

@app.route("/")
def home():
	"""List all available API routes"""
	return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
	"""Return dictionary of date and prcp information for the past year"""
	dateprcp = session.query(Measurement.date, Measurement.prcp).all()
	prcp_dict = {date: prcp for (date, prcp) in dateprcp}
	return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
	"""Return Json of all the stations in the dataset"""
	station_list = session.query(Station.station, Station.name).all()
	station_dict = {station_id: name for (station_id, name) in station_list}
	return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
	"""Return a JSON list of Temperature Observations (tobs) for the previous year."""
	datetobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
	tobs_dict = {date_tob: tob for (date_tob, tob) in datetobs}
	return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def from_start(start):
	"""Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
	start_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
	return jsonify(start_stats)




@app.route("/api/v1.0/<start>/<end>")
def from_start_end(start,end):
	"""Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
	start_end_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
	return jsonify(start_end_stats)


if __name__ == '__main__':
    app.run(debug=True)
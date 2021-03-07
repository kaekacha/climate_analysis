import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc 
from flask import Flask, jsonify
database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

#boiler plate code: Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")

    session = Session(engine)

    prcp_sesh = session.query(measurement.date, measurement.prcp).order_by(measurement.date).all()

    prcp_list = []
    for date, prcp in prcp_sesh:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

    session.close()

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")

    session = Session(engine)
    
    st_sesh = session.query(station.station).all()

    st_list = []
    for st in st_sesh:
        st_dict = {}
        st_dict["station"] = st
        st_list.append(st_dict)

    return jsonify(st_list)

    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")

    session = Session(engine)
    
    to_hist=session.query(measurement.date, measurement.tobs).filter(measurement.station==temps[0]).order_by(desc(measurement.date)).first()
    
    tobs_list= []
    for station, tobs in st_sesh:
        st_dict = {}
        st_dict["station"] = st
        st_list.append(st_dict)

    return jsonify(st_list)

    session.close()
'''
/api/v1.0/tobs

Query the dates and temperature observations of the most active station for the last year of data.

Return a JSON list of temperature observations (TOBS) for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>

Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

Hints

You will need to join the station and measurement tables for some of the queries.

Use Flask jsonify to convert your API data into a valid JSON response object.
'''

#boiler plate code
if __name__ == "__main__":
    app.run(debug=True)
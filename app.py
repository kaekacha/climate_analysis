#import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc 
from flask import Flask, jsonify
from datetime import datetime
from dateutil.relativedelta import *

#create orms from sqlite database tables "measurement" and "station"
database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

#boiler plate code: Create an app, being sure to pass __name__
app = Flask(__name__)

#created index/home route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start and /api/v1.0/start/end<br/>"
        f"      Note: Please manually enter dates in YYYY-MM-DD format for start, end paramaters in endpoints above."
    )

#create precipitation route
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

#create station route
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

#create tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")

    session = Session(engine)
    
    st_active=session.query(measurement.station,func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(desc(func.count(measurement.station))).first()
   
    tobs_active =session.query(measurement.date, measurement.tobs).\
        filter(measurement.station==st_active[0]).\
        order_by(desc(measurement.date)).first()

    recent_dt=tobs_active[0]
    
    import datetime
    from dateutil.relativedelta import relativedelta

    recent_dt_form = datetime.datetime.strptime(recent_dt, '%Y-%m-%d')
    recent_dt=recent_dt_form.date()
    past_dt=recent_dt+relativedelta(years=-1)
    tobs_pastyr_active=session.query(measurement.date, measurement.tobs).\
        filter(measurement.station==st_active[0]).filter(measurement.date>=past_dt).all()

    tobs_list= []
    for date, tobs in tobs_pastyr_active:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

    session.close()

#create manual start date entry route
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'start date' page...")
   
    session = Session(engine)

    import datetime
    from dateutil.relativedelta import relativedelta

    start_dt = datetime.datetime.strptime(start, '%Y-%m-%d')
    start_dt=start_dt.date()
    tobs_start=session.query(measurement.date,func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date>=start_dt).group_by(measurement.date).all()

    tobs_list= []
    for date, min, avg, max in tobs_start:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["min"] = min
        tobs_dict["avg"] = avg
        tobs_dict["max"] = max
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

    session.close()

#create manual start date entry route
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    print("Server received request for 'start and end dates' page...")

    session = Session(engine)

    import datetime
    from dateutil.relativedelta import relativedelta

    start_dt = datetime.datetime.strptime(start, '%Y-%m-%d')
    start_dt=start_dt.date()
    end_dt = datetime.datetime.strptime(end, '%Y-%m-%d')
    end_dt=end_dt.date()
    tobs_startend=session.query(measurement.date,func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date>=start_dt).filter(measurement.date<=end_dt).group_by(measurement.date).all()

    tobs_list= []
    for date, min, avg, max in tobs_startend:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["min"] = min
        tobs_dict["avg"] = avg
        tobs_dict["max"] = max
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

    session.close()

#boiler plate code
if __name__ == "__main__":
    app.run(debug=True)
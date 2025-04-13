# Module 10 - sqlalchemy-challenge: Hawaii Climate Analysis API

This project builds a Flask API that provides climate data for Honolulu, Hawaii, using a SQLite database.
The data includes daily weather measurements from various stations over several years. Users can interact with the API to retrieve precipitation, station data, and temperature observations for specified date ranges.

---

## Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- NumPy
- Pandas (in Jupyter)

---

## The API

### Access the API
Go to: http://127.0.0.1:5000/

### API Routes

/	API homepage with instructions and available routes
/api/v1.0/precipitation	JSON dictionary of precipitation data for the last 12 months
/api/v1.0/stations	JSON list of weather stations
/api/v1.0/tobs	Temperature observations (TOBS) from the most active station for the last year
/api/v1.0/<start>	Min, Avg, Max temperature from the start date to the most recent date
/api/v1.0/<start>/<end>	Min, Avg, Max temperature for a custom start–end date range

For the start and end dates, replace <start> and <end> with dates formatted as follows YYYY-MM-DD for example, /api/v1.0/2016-08-01/2017-08-01)
Valid dates range from 2010-01-01 to 2017-08-23


Example of API Routes

+ http://127.0.0.1:5000/api/v1.0/precipitation
+ http://127.0.0.1:5000/api/v1.0/stations
+ http://127.0.0.1:5000/api/v1.0/2016-08-01
+ http://127.0.0.1:5000/api/v1.0/2016-08-01/2017-08-01

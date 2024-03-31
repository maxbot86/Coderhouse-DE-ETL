CREATE TABLE IF NOT EXISTS XXXXXXXXX.logs_weather
(
	datetime_reg TIMESTAMP WITHOUT TIME ZONE
	,coor_lat VARCHAR(256)
	,coor_lon VARCHAR(256) 
	,datetime_log TIMESTAMP WITHOUT TIME ZONE
	,temperature_2m DOUBLE PRECISION
	,relative_humidity_2m BIGINT
	,precipitation_probability BIGINT
	,rain DOUBLE PRECISION
	,wind_speed_10m DOUBLE PRECISION
)
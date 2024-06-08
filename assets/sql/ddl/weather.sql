CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    min_temp FLOAT,
    max_temp FLOAT,
    rainfall FLOAT,
    humidity_9am INTEGER,
    humidity_3pm INTEGER,
    temp_9am FLOAT,
    temp_3pm FLOAT,
    current_temp FLOAT,
    current_humidity INTEGER,
    current_weather_description VARCHAR,
    created_by VARCHAR(50) NOT NULL DEFAULT current_user,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT current_timestamp,
    updated_by VARCHAR(50),
    updated_at TIMESTAMP WITH TIME ZONE,
	CONSTRAINT weather_date_check CHECK (date <= CURRENT_DATE),
    CONSTRAINT weather_min_max_temp_check CHECK (min_temp <= max_temp),
    CONSTRAINT weather_temp_9am_range_check CHECK (temp_9am BETWEEN -273.15 AND 100.0),
    CONSTRAINT weather_temp_3pm_range_check CHECK (temp_3pm BETWEEN -273.15 AND 100.0),
    CONSTRAINT weather_current_temp_range_check CHECK (current_temp BETWEEN -273.15 AND 100.0),
    CONSTRAINT weather_min_temp_range_check CHECK (min_temp BETWEEN -273.15 AND 100.0),
    CONSTRAINT weather_max_temp_range_check CHECK (max_temp BETWEEN -273.15 AND 100.0),
    CONSTRAINT weather_max_rainfall_check CHECK (rainfall <= 1000.0),
    CONSTRAINT weather_created_by_check CHECK (created_at <= CURRENT_TIMESTAMP),
    CONSTRAINT weather_updated_by_check CHECK (updated_at IS NULL OR updated_at <= CURRENT_TIMESTAMP)
);

COMMENT ON TABLE weather IS 'Table storing weather data including historical and current weather details';
COMMENT ON COLUMN weather.id IS 'ID of the table';
COMMENT ON COLUMN weather.date IS 'Date for the record about the weather';
COMMENT ON COLUMN weather.min_temp IS 'Minimum temperature of the day';
COMMENT ON COLUMN weather.max_temp IS 'Maximum temperature of the day';
COMMENT ON COLUMN weather.rainfall IS 'Rainfall in millimeters';
COMMENT ON COLUMN weather.humidity_9am IS 'Humidity percentage at 9 AM';
COMMENT ON COLUMN weather.humidity_3pm IS 'Humidity percentage at 3 PM';
COMMENT ON COLUMN weather.temp_9am IS 'Temperature at 9 AM';
COMMENT ON COLUMN weather.temp_3pm IS 'Temperature at 3 PM';
COMMENT ON COLUMN weather.current_temp IS 'Current temperature from the API';
COMMENT ON COLUMN weather.current_humidity IS 'Current humidity percentage from the API';
COMMENT ON COLUMN weather.current_weather_description IS 'Current weather description from the API';
COMMENT ON COLUMN weather.created_by IS 'User that created the record';
COMMENT ON COLUMN weather.created_at IS 'Datetime when the record was created';
COMMENT ON COLUMN weather.updated_by IS 'Last user that updated the record';
COMMENT ON COLUMN weather.updated_at IS 'Last timestamp when the record was updated';

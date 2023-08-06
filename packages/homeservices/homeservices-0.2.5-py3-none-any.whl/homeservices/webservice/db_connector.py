from influxdb_wrapper import influxdb_factory, DBConn
from types import MethodType


def read_last_measures(self, number_of_measures: int, sensor_id: str) -> list:
    points = self.select('DHT22', [('sensorid', sensor_id)],
                         order_by='time', order_asc=False,
                         limit=number_of_measures)
    return points


def db_factory(db_type: str = 'influx') -> DBConn:
    db_instance = influxdb_factory(db_type)

    # Dinamically add method
    setattr(db_instance, 'read_last_measures', MethodType(read_last_measures, db_instance))
    return db_instance

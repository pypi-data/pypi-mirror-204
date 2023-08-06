""" 
    An entry point for all the services in my home
"""
import os
from urllib import parse
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, request, make_response, Response
from flask_compress import Compress

from config_yml import Config

from revproxy_auth import RevProxyAuth

from elecmon import ElectricityMonitor

from .db_connector import db_factory


class HomeServices():
    """ Homeservices base class: An entry point for all the services in my home
    """
    def __init__(self,  template_folder: str, static_folder: str, template_config_path: str = None) -> None:
        """
        Args:
            template_folder (string): Path for the Flask templates
            static_folder (string): Path for the Flask static info
        """

        self.app = Flask(__name__,  template_folder=template_folder, static_folder=static_folder)

        self.revproxy_auth = RevProxyAuth()

        self.app.add_url_rule('/', 'auth', self.auth, methods=['GET', 'POST'])
        self.app.add_url_rule('/<path:path>', 'path_redirect', self.revproxy_auth.path_redirect,
                              methods=['GET', 'POST'])
        self.app.add_url_rule('/alexaintent', 'alexaintent', self.alexa_intent, methods=['GET'])
        self.app.add_url_rule('/customsensor', 'customsensor', self.custom_sensor, methods=['GET'])
        self.app.add_url_rule('/besthour', 'besthour', self.best_hour, methods=['GET'])

        Compress(self.app)

        if not template_config_path:
            template_config_path = os.path.join(Path(__file__).parent.resolve(), './config-template.yml')

        self.config = Config(self.get_class_name(), template_config_path, 'config.yml')

        influx_conn_type = self.config['influxdbconn'].get('type', 'influx')
        self.conn = db_factory(influx_conn_type)
        self.conn.openConn(self.config['influxdbconn'])

    @classmethod
    def get_class_name(cls) -> str:
        """
        Returns:
           string: class name
        """
        return "homeservices"

    def get_app(self) -> Flask:
        """
        Returns:
            Flask app: The flask app
        """
        return self.app

    def run(self) -> None:
        """Execution of the application
        """
        self.app.run()
        # self.app.run(host='0.0.0.0')

    def index(self) -> Response:
        """Main entry point

        Returns:
            http_response: response string
        """
        return 'This is the Pi server.'

    def auth(self) -> Response:
        """Main entry point
        Returns:
            http_response: response string
        """
        resp = self.revproxy_auth.path_redirect("/")
        return resp

 
    def _read_last_measures(self, number_of_measures: int, sensor_name: str) -> list:
        sensor_table = {'jardín': '2', 'cocina': '1', 'buhardilla': '3'}

        points = None

        if sensor_name in sensor_table:
            points = self.conn.read_last_measures(number_of_measures=number_of_measures, 
                                                  sensor_id=sensor_table[sensor_name])

        return points

    def best_hour(self) -> Response:
        """Answer to sensor requests. It returns

        Returns:
            http_response: json with temperature and humidity information
        """
        if request.method == 'GET':
            params = parse.parse_qs(parse.urlparse(request.url).query)
            # Parse GET param
            if 'device' in params:
                device = params['device'][0]

                if device == 'el lavavajillas':
                    time = 180
                elif device == 'la lavadora':
                    time = 60
                else:
                    response = make_response("Device not found", 404)
                    return response

                elec_mon = ElectricityMonitor()
                best_hour, price = elec_mon.get_better_timeslice(time, datetime.now())

                if best_hour.day == datetime.now().day:
                    if best_hour.hour == datetime.now().hour:
                        response_phrase = "Ya mismo, cuanto antes mejor."
                    else:
                        response_phrase = f"A las {best_hour.hour}."
                else:
                    response_phrase = f"A las {best_hour.hour} de mañana."

                response = make_response(response_phrase.encode('UTF-8'))
                response.mimetype = "text/plain"
                response.headers['Pragma'] = 'no-cache'
                response.headers["Expires"] = 0
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            else:
                response = make_response("Device not specified", 404)
            return response

    def custom_sensor(self) -> Response:
        """Answer to sensor requests. It returns

        Returns:
            http_response: json with temperature and humidity information
        """
        if request.method == 'GET':
            params = parse.parse_qs(parse.urlparse(request.url).query)
            # Parse GET param
            if 'sensor' in params:
                sensor = params['sensor'][0]

                points = self._read_last_measures(1, sensor)

                if points:
                    point = points[0]

                    response = make_response(json.dumps(f'{{"temp" : {point["temp"]}, "hum" : {point["humidity"]} }}'))
                    response.mimetype = "application/json"
                    response.headers['Pragma'] = 'no-cache'
                    response.headers["Expires"] = 0
                    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                else:
                    response = make_response("Sensor not found", 404)
            else:
                response = make_response("Sensor not specified", 404)
            return response

    def alexa_intent(self) -> Response:
        """Function to be called from alexa intent, that will return human-readable string to be speeched out by Alexa

        Returns:
           http_response: Verbose string human-readable with the information of the sensor temperature
        """
        if request.method == 'GET':
            params = parse.parse_qs(parse.urlparse(request.url).query)
            # Parse GET param
            if 'sensor' in params:
                sensor = parse.parse_qs(parse.urlparse(request.url).query)['sensor'][0]

                points = self._read_last_measures(4, sensor)

                trend = ''
                if points and len(points) == 4:
                    delta = points[0]['temp'] - points[3]['temp']
                    if delta > 0.6:
                        trend = ' y subiendo a saco'
                    elif delta > 0.3:
                        trend = ' y subiendo'
                    elif delta > 0.1:
                        trend = ' y subiendo ligeramente'
                    elif delta < -0.6:
                        trend = ' y bajando a saco'
                    elif delta < -0.3:
                        trend = ' y bajando'
                    elif delta < -0.1:
                        trend = ' y bajando ligeramente'

                    response_phrase = (f"Hace {points[0]['temp']} grados{trend},"
                                       f"y la humedad es del {points[0]['humidity']:.0f} por ciento.")

                    if points[0]['humidity'] > 98:
                        response_phrase += " Es muy posible que esté lloviendo."

                    if points[0]['temp'] < 5:
                        response_phrase += " ¡Joder, que frio hace!."
                    elif points[0]['temp'] < 10:
                        response_phrase += " Hace bastante fresquete."
                    elif points[0]['temp'] > 30:
                        response_phrase += " ¡Que calor hace!."
                    elif points[0]['temp'] > 35:
                        response_phrase += " ¡Joder, que nos achicharramos!."
                    response = make_response(response_phrase.encode('UTF-8'))
                    response.mimetype = "text/plain"
                    response.headers['Pragma'] = 'no-cache'
                    response.headers["Expires"] = 0
                    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                else:
                    response = make_response("Sensor not found", 404)
            else:
                response = make_response("Sensor not specified", 404)

            return response

import requests
import yaml
import logging

_LOGGER = logging.getLogger(__name__)

DEFAULT_MIN_MOISTURE = 20
DEFAULT_MAX_MOISTURE = 60
DEFAULT_MIN_CONDUCTIVITY = 500
DEFAULT_MAX_CONDUCTIVITY = 3000
DEFAULT_MIN_TEMPERATURE = 10
DEFAULT_MAX_TEMPERATURE = 30
DEFAULT_MIN_BRIGHTNESS = 1000
DEFAULT_MAX_BRIGHTNESS = 30000

class Plant():

    def __init__(self, name, config):
        """Initialize the Plant component."""
        self._config = config
        self._name = name
        self._species = self._config.get('species')
        self._plantbook_token = None
        if self._config.get('plantbook_client_id') and self._config.get('plantbook_client_secret'):
            self.get_plantbook_data()
        else:
            self.populate_default_data()

    def get_plantbook_data(self):
        if not self._plantbook_token:
            self.get_plantbook_token()
        # url = "https://open.plantbook.io/api/v1/plant/detail/{}".format(self._species)
        # Temp as a demo, since get by name does not work yet
        url = "https://open.plantbook.io/api/v1/plant/detail/5494/"
        headers = {"Authorization": "Bearer {}".format(self._plantbook_token)}
        try:
            result = requests.get(url, headers=headers)
            result.raise_for_status()
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            _LOGGER.error("Timeout connecting to {}".format(url))
            return
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            _LOGGER.error("Too many redirects connecting to {}".format(url))
            return
        except requests.exceptions.HTTPError as err:
            _LOGGER.error(err)
            return
        except requests.exceptions.RequestException as err:
            # catastrophic error. bail.
            _LOGGER.error(err)
            return
        res = result.json()
        _LOGGER.debug("Fetched data from {}:".format(url))
        _LOGGER.debug(res)
        self._name = res['display_pid']
        self._set_conf_value('min_temperature', res['min_temp'])
        self._set_conf_value('max_temperature', res['max_temp'])
        self._set_conf_value('min_moisture', res['min_soil_moist'])
        self._set_conf_value('max_moisture', res['max_soil_moist'])
        self._set_conf_value('min_conductivity', res['min_soil_ec'])
        self._set_conf_value('max_conductivity', res['max_soil_ec'])
        self._set_conf_value('min_brightness', res['min_light_lux'])
        self._set_conf_value('max_brightness', res['max_light_lux'])

    def get_plantbook_token(self):
        url =  'https://open.plantbook.io/api/v1/token/'
        data = {
            'grant_type': 'client_credentials',
            'client_id': self._config['plantbook_client_id'],
            'client_secret': self._config['plantbook_client_secret']
        }
        try:
            result = requests.post(url, data = data)
            result.raise_for_status()
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            _LOGGER.error("Timeout connecting to {}".format(url))
            return
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            _LOGGER.error("Too many redirects connecting to {}".format(url))
            return
        except requests.exceptions.HTTPError as err:
            _LOGGER.error(err)
            return
        except requests.exceptions.RequestException as err:
            # catastrophic error. bail.
            _LOGGER.error(err)
            return
        self._plantbook_token = result.json().get('access_token')
        _LOGGER.debug("Got token {} from {}".format(self._plantbook_token, url))

    def populate_default_data(self):
        self._set_conf_value('min_temperature', DEFAULT_MIN_TEMPERATURE)
        self._set_conf_value('max_temperature', DEFAULT_MAX_TEMPERATURE)
        self._set_conf_value('min_moisture', DEFAULT_MIN_TEMPERATURE)
        self._set_conf_value('max_moisture', DEFAULT_MAX_TEMPERATURE)
        self._set_conf_value('min_conductivity', DEFAULT_MIN_CONDUCTIVITY)
        self._set_conf_value('max_conductivity', DEFAULT_MAX_CONDUCTIVITY)
        self._set_conf_value('min_brightness', DEFAULT_MIN_BRIGHTNESS)
        self._set_conf_value('max_brightness', DEFAULT_MAX_BRIGHTNESS)


    def _set_conf_value(self, var, val):
        if var not in self._config or self._config[var] is None:
            self._config[var] = val


    @property
    def name(self):
        """Return the name of the plant."""
        return self._name

    @property
    def species(self):
        """Return the species of the plant."""
        return self._species

    @property
    def config(self):
        """Return the full config of the plant."""
        return self._config




with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

plants = {}
for plant_name, plant_config in config.items():
    plants[plant_name] = Plant(plant_name, plant_config)

    print(plants[plant_name].name)
    print(plants[plant_name].config)

import urllib.request
import re
from datetime import datetime
import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = "remiks_renovasjon"
DATA_REMIKS_RENOVASJON = "data_remiks_renovasjon"

CONF_STREETS = "streets"
CONF_FOLLOWING = "following"
CONF_DAYS_NOTICE = "days_notice"
CONF_TURNOVER_HOUR = "turnover_hour"

# When to load next day
DEFAULT_TURNOVER_HOUR = 18

DEFAULT_ICONS = {
    'Optisk sortert avfall': 'mdi:delete-empty',
    'Glass og metallemballasje': 'mdi:bottle-soda-classic',
    'Posesupplering': 'mdi:sack',
}


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_STREETS): cv.ensure_list,
                vol.Required(CONF_FOLLOWING): cv.ensure_list,
                vol.Required(CONF_DAYS_NOTICE): cv.positive_int,
                vol.Optional(CONF_TURNOVER_HOUR, default=DEFAULT_TURNOVER_HOUR): cv.positive_int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """Set up component."""
    streets = config[DOMAIN][CONF_STREETS]
    following = config[DOMAIN][CONF_FOLLOWING]
    days_notice = config[DOMAIN][CONF_DAYS_NOTICE]

    remiks_renovasjon = RemiksRenovasjon(
        streets, following, days_notice
    )
    hass.data[DATA_REMIKS_RENOVASJON] = remiks_renovasjon

    return True


class RemiksRenovasjon:
    def __init__(self, streets, following, days_notice):
        self.streets = streets
        self.following = following
        self.days_notice = days_notice
        self._parsed_data = self._fetch_parsed_data()

    def update_parsed_data(self):
        needed = self._parsed_data_needs_update(self._parsed_data)
        if needed:
            self._parsed_data = self._fetch_parsed_data()

    def get_parsed_data(self, entity_code=None):
        if entity_code is None:
            return self._parsed_data
        else:
            for item in self._parsed_data:
                if item[0] == entity_code:
                    return item
        return None
        

    def _fetch_parsed_data(self):

        _LOGGER.info("Fetching from remiks.no.")
        for street in self.streets:
            _LOGGER.debug("Fetching for " + street)
            req = urllib.request.Request(
                'https://www.remiks.no/min-side/' + street, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            page = urllib.request.urlopen(req).read().decode('utf-8')
        
            _LOGGER.debug("Loaded page content: " + page)
            parsed_data = []
            for event in self.following:
                _LOGGER.debug("Looking up " + event)
                results = re.findall(r'(\d{2}.{6}\d{4}) - ' + event, page)
                dato = results[0]
                for word, initial in {"mai":"may", "okt":"oct", "des":"dec" }.items():
                    dato = dato.replace(word.lower(), initial)
                event_date = datetime.strptime(dato, '%d. %b %Y')
                entity_code = event.replace(' ','_').lower() + "_" + street
                parsed_data.append( (entity_code, event, street, street.replace("-", " ").title(), event_date, DEFAULT_ICONS.get(event, '')))

        _LOGGER.info("Compiled a list of events to follow from remiks.no")
        return parsed_data

    @staticmethod
    def _parsed_data_needs_update(parsed_data):
        
        for item in parsed_data:
            entity_code, _, _, _, next_date, _ = item

            if next_date is None:
                _LOGGER.info("No data for " + entity_code + ". Refreshing data.")
                return True
            if next_date.date() < datetime.today().date() or (next_date.date() == datetime.today().date() and datetime.today().time().hour >= CONF_TURNOVER_HOUR):
                _LOGGER.info("Data for " + entity_code + " has expired. Refreshing data.")
                return True

        return False

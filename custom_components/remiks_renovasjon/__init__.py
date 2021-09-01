import urllib.request
import re
from datetime import datetime
import logging
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = "remiks_renovasjon"
DATA_REMIKS_RENOVASJON = "data_remiks_renovasjon"

CONF_STREET = "street"
CONF_STREET_NUMBER = "street_number"
CONF_TRACK = "track"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_STREET): cv.string,
                vol.Required(CONF_STREET_NUMBER): cv.string,
                vol.Required(CONF_TRACK): cv.ensure_list,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """Set up component."""
    street = config[DOMAIN][CONF_STREET]
    street_number = config[DOMAIN][CONF_STREET_NUMBER]
    track = config[DOMAIN][CONF_TRACK]

    remiks_renovasjon = RemiksRenovasjon(
        street, street_number, street_number
    )
    hass.data[DATA_REMIKS_RENOVASJON] = remiks_renovasjon

    return True


class RemiksRenovasjon:
    def __init__(self, street, street_number, track):
        self.street = self._url_encode(street)
        self.street_number = self._url_encode(street_number)
        self.track = track
        self._tracked = self._fetch_tracked()

    @staticmethod
    def _url_encode(string):
        string_decoded_encoded = urllib.parse.quote(urllib.parse.unquote(string))
        if string_decoded_encoded != string:
            string = string_decoded_encoded
        return string

    def update_tracked(self):
        update = self._tracked_needs_update(self._tracked)
        if update:
            self._tracked = self._fetch_tracked()

    def _fetch_tracked(self):

        _LOGGER.info("Fetching from remiks.no.")
        req = urllib.request.Request(
            'https://www.remiks.no/min-side/' + self.street + '-' + self.street_number, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        page = urllib.request.urlopen(req).read().decode('utf-8')
       
        _LOGGER.debug("Loaded page: " + page)
        tracked = []
        for event in self.track:
            _LOGGER.debug("Looking up " + event)
            results = re.findall(r'(\d{2}.{6}\d{4}) - ' + event, page)
            event_date = datetime.strptime(results[0], '%d. %b %Y')
            event_code = event.replace(' ','_').lower()
            tracked.append( (event_code, event, event_date) )

        _LOGGER.info("Compiled a list of tracked events from remiks.no")
        return tracked

    @staticmethod
    def _tracked_needs_update(tracked):
        for item in tracked:
            event_code, _, next_date = entry

            if next_date is None:
                _LOGGER.info("No data for " + event_code + ", so refreshing track list.")
                return True
            if next_date.date() < date.today():
                _LOGGER.info("Data for " + event_code + " expired, so refreshing track list.")
                return True

        return False

from datetime import timedelta
from datetime import datetime
import logging

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
#from homeassistant.helpers.entity import Entity
from ..remiks_renovasjon import DATA_REMIKS_RENOVASJON

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)

def setup_platform(hass, config, add_entities, discovery_info=None):

    remiks_renovasjon = hass.data[DATA_REMIKS_RENOVASJON]

    add_entities(
        RemiksRenovasjonBinarySensor(remiks_renovasjon, item[0]) for item in remiks_renovasjon.get_parsed_data()
    )

class RemiksRenovasjonBinarySensor(BinarySensorEntity):
    def __init__(self, remiks_renovasjon, entity_code):
        """Initialize with API object, device id."""
        _LOGGER.debug("Adding entity code: " + entity_code)
        self._remiks_renovasjon = remiks_renovasjon
        self._entity_code = entity_code

    @property
    def name(self):
        """Return the full name associated with the entity_code, if any."""
        item = self._remiks_renovasjon.get_parsed_data(self._entity_code)
        if item is not None:
            _LOGGER.debug("Name of entity code: Remiks boolean " + self._entity_code + ": " + item[1] + " " + item[3])
            return "Remiks boolean " + item[1] + " " + item[3]
        else:
            _LOGGER.debug("No name for entity code: Remiks boolean " + self._entity_code)

    @property
    def is_on(self):
        """Return the boolean state of the entity."""
        item = self._remiks_renovasjon.get_parsed_data(self._entity_code)
        if item is not None:
            # If date is not set
            if item[4] is None:
                return False
            state = True
            days_until_next = (item[4].date() - datetime.now().date()).days
            if days_until_next == 0 and datetime.today().time().hour >= int(self._remiks_renovasjon.turnover_hour):
                state = False
            elif  days_until_next > int(self._remiks_renovasjon.days_notice):
                state = False
            _LOGGER.debug("State of entity code: Remiks boolean " + self._entity_code + ": " + str(state))
            return state
        else:
            _LOGGER.debug("No state for entity code: Remiks boolean " + self._entity_code)

    @property
    def icon(self):
        """Icon of the entity."""
        item = self._remiks_renovasjon.get_parsed_data(self._entity_code)
        if item is not None and item[5] != "":
            _LOGGER.debug("Icon of entity code: Remiks boolean " + self._entity_code + ": " + item[5])
            return item[5]
        else:
            _LOGGER.debug("No icon for entity code: Remiks boolean " + self._entity_code)

    def update(self):
        """Update list of parsed data."""
        self._remiks_renovasjon.update_parsed_data()

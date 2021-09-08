from datetime import timedelta
import logging

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from ..remiks_renovasjon import DATA_REMIKS_RENOVASJON

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)


def setup_platform(hass, config, add_entities, discovery_info=None):

    remiks_renovasjon = hass.data[DATA_REMIKS_RENOVASJON]

    add_entities(
        RemiksRenovasjonSensor(remiks_renovasjon, item[0]) for item in remiks_renovasjon.get_parsed_data()
    )

class RemiksRenovasjonSensor(Entity):
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
            name = "Remiks " + item[1] + " " + item[3]
            _LOGGER.debug("Name of entity code " + self._entity_code + ": " + name)
            return name
        else:
            _LOGGER.debug("No name for entity code: " + self._entity_code)

    @property
    def state(self):
        """Return the state/date of the entity."""
        item = self._remiks_renovasjon.get_parsed_data(self._entity_code)
        if item is not None:
            entity_state = item[4].strftime('%d. %b %Y')
            _LOGGER.debug("State of entity code: " + self._entity_code + ": " + entity_state)
            return entity_state
        else:
            _LOGGER.debug("No state for entity code: " + self._entity_code)

    @property
    def icon(self):
        """Icon of the entity."""
        item = self._remiks_renovasjon.get_parsed_data(self._entity_code)
        if item is not None and item[5] != "":
            _LOGGER.debug("Icon of entity code: " + self._entity_code + ": " + item[5])
            return item[5]
        else:
            _LOGGER.debug("No icon for entity code: " + self._entity_code)

    def update(self):
        """Update list of parsed data."""
        self._remiks_renovasjon.update_parsed_data()

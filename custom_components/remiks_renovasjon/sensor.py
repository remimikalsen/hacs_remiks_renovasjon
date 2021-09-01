from datetime import timedelta
import logging

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from ..remiks_renovasjon import DATA_REMIKS_RENOVASJON

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=6)

def setup_platform(hass, config, add_entities, discovery_info=None):

    remiks_renovasjon = hass.data[DATA_REMIKS_RENOVASJON]

    add_entities(
        RemiksRenovasjonSensor(remiks_renovasjon, event[0]) for event in remiks_renovasjon.get_tracked_event()
    )

class RemiksRenovasjonSensor(Entity):
    def __init__(self, remiks_renovasjon, event_code):
        """Initialize with API object, device id."""
        _LOGGER.debug("Adding event code: " + event_code)
        self._remiks_renovasjon = remiks_renovasjon
        self._event_code = event_code

    @property
    def name(self):
        """Return the name of the event_code if any."""
        event = self._remiks_renovasjon.get_tracked_event(self._event_code)
        if event is not None:
            _LOGGER.debug("Name of event code: " + self._event_code + ": " + event[1])
            return event[1]
        else:
            _LOGGER.debug("No name for event code: " + self._event_code)

    @property
    def state(self):
        """Return the state/date of the event."""
        event = self._remiks_renovasjon.get_tracked_event(self._event_code)
        if event is not None:
            _LOGGER.debug("State of event code: " + self._event_code + ": " + event[2].strftime('%d. %b %Y'))
            return event[2].strftime('%d. %b %Y')
        else:
            _LOGGER.debug("No state for event code: " + self._event_code)

    @property
    def entity_picture(self):
        """Return the symbol of the event (not implemented)"""
        return None
        event = self._remiks_renovasjon.get_tracked_event(self._event_code)
        if event is not None:
            _LOGGER.debug("Symbol of event code: " + self._event_code + ": " + event[3])
            return event[3]
        else:
            _LOGGER.debug("No symbol for event code: " + self._event_code)

    def update(self):
        """Update list of tracked events."""
        self._remiks_renovasjon.update_tracked()

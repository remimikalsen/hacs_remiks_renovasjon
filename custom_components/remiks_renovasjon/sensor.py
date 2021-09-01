from datetime import timedelta
import logging

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from ..remiks_renovasjon import DATA_REMIKS_RENOVASJON

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)

def setup_platform(hass, config, add_entities, discovery_info=None):

    remiks_renovasjon = hass.data[DATA_REMIKS_RENOVASJON]

    add_entities(
        RemiksRenovasjonSensor(remiks_renovasjon, event[0]) for event in remiks_renovasjon.get_tracked_event()
    )


class RemiksRenovasjonSensor(Entity):
    def __init__(self, remiks_renovasjon, event_code):
        """Initialize with API object, device id."""
        self._remiks_renovasjon = remiks_renovasjon
        self._event_code = event_code

    @property
    def name(self):
        """Return the name of the event_code if any."""
        event = self._remiks_renovasjon.get_tracked_event(self._event_code)
        if event is not None:
            return event[1]

    @property
    def state(self):
        """Return the state/date of the event."""
        event = self._remiks_renovasjon.get_tracked_event(self._event_code)
        if event is not None:
            return event[2].strftime('%d. %b %Y')

    @property
    def entity_picture(self):
        """Return the symbol of the event (not implemented)"""
        return None
        event = self._remiks_renovasjon.get_tracked_event(self._event_code)
        if event is not None:
            return event[3]

    def update(self):
        """Update list of tracked events."""
        self._remiks_renovasjon.update_tracked()

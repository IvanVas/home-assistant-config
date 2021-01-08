"""Alexa entity adapters."""
import logging
from typing import TYPE_CHECKING, List

from homeassistant.components import (
    alarm_control_panel,
    alert,
    automation,
    binary_sensor,
    camera,
    cover,
    fan,
    group,
    image_processing,
    input_boolean,
    input_number,
    light,
    lock,
    media_player,
    scene,
    script,
    sensor,
    switch,
    timer,
    vacuum,
)
from homeassistant.components.climate import const as climate
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_SUPPORTED_FEATURES,
    ATTR_UNIT_OF_MEASUREMENT,
    CLOUD_NEVER_EXPOSED_ENTITIES,
    CONF_NAME,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    __version__,
)
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers import network
from homeassistant.util.decorator import Registry

from .capabilities import (
    Alexa,
    AlexaBrightnessController,
    AlexaCameraStreamController,
    AlexaCapability,
    AlexaChannelController,
    AlexaColorController,
    AlexaColorTemperatureController,
    AlexaContactSensor,
    AlexaDoorbellEventSource,
    AlexaEndpointHealth,
    AlexaEqualizerController,
    AlexaEventDetectionSensor,
    AlexaInputController,
    AlexaLauncher,
    AlexaLockController,
    AlexaModeController,
    AlexaMotionSensor,
    AlexaPercentageController,
    AlexaPlaybackController,
    AlexaPlaybackStateReporter,
    AlexaPowerController,
    AlexaPowerLevelController,
    AlexaRangeController,
    AlexaRemoteVideoPlayer,
    AlexaSceneController,
    AlexaSecurityPanelController,
    AlexaSeekController,
    AlexaSpeaker,
    AlexaStepSpeaker,
    AlexaTemperatureSensor,
    AlexaThermostatController,
    AlexaTimeHoldController,
    AlexaToggleController,
)
from .const import CONF_DESCRIPTION, CONF_DISPLAY_CATEGORIES

if TYPE_CHECKING:
    from .config import AbstractConfig

_LOGGER = logging.getLogger(__name__)

ENTITY_ADAPTERS = Registry()

TRANSLATION_TABLE = dict.fromkeys(map(ord, r"}{\/|\"()[]+~!><*%"), None)


class DisplayCategory:
    """Possible display categories for Discovery response.

    https://developer.amazon.com/docs/device-apis/alexa-discovery.html#display-categories
    """

    # Indicates the endpoint is a speaker or speaker system.
    SPEAKER = "SPEAKER"

    # Indicates the endpoint is a television.
    TV = "TV"


def generate_alexa_id(entity_id: str) -> str:
    """Return the alexa ID for an entity ID."""
    return entity_id.replace(".", "#").translate(TRANSLATION_TABLE)


class AlexaEntity:
    """An adaptation of an entity, expressed in Alexa's terms.

    The API handlers should manipulate entities only through this interface.
    """

    def __init__(self, hass: HomeAssistant, config: "AbstractConfig", entity: State):
        """Initialize Alexa Entity."""
        self.hass = hass
        self.config = config
        self.entity = entity
        self.entity_conf = config.entity_config.get(entity.entity_id, {})

    @property
    def entity_id(self):
        """Return the Entity ID."""
        return self.entity.entity_id

    def friendly_name(self):
        """Return the Alexa API friendly name."""
        return self.entity_conf.get(CONF_NAME, self.entity.name).translate(
            TRANSLATION_TABLE
        )

    def description(self):
        """Return the Alexa API description."""
        description = self.entity_conf.get(CONF_DESCRIPTION) or self.entity_id
        return f"{description} via Home Assistant".translate(TRANSLATION_TABLE)

    def alexa_id(self):
        """Return the Alexa API entity id."""
        return generate_alexa_id(self.entity.entity_id)

    def display_categories(self):
        """Return a list of display categories."""
        entity_conf = self.config.entity_config.get(self.entity.entity_id, {})
        if CONF_DISPLAY_CATEGORIES in entity_conf:
            return [entity_conf[CONF_DISPLAY_CATEGORIES]]
        return self.default_display_categories()

    def default_display_categories(self):
        """Return a list of default display categories.

        This can be overridden by the user in the Home Assistant configuration.

        See also DisplayCategory.
        """
        raise NotImplementedError

    def get_interface(self, capability) -> AlexaCapability:
        """Return the given AlexaInterface.

        Raises _UnsupportedInterface.
        """

    def interfaces(self) -> List[AlexaCapability]:
        """Return a list of supported interfaces.

        Used for discovery. The list should contain AlexaInterface instances.
        If the list is empty, this entity will not be discovered.
        """
        raise NotImplementedError

    def serialize_properties(self):
        """Yield each supported property in API format."""
        for interface in self.interfaces():
            if not interface.properties_proactively_reported():
                continue

            yield from interface.serialize_properties()

    def serialize_discovery(self):
        """Serialize the entity for discovery."""
        result = {
            "displayCategories": self.display_categories(),
            "cookie": {},
            "endpointId": self.alexa_id(),
            "friendlyName": self.friendly_name(),
            "description": self.description(),
            "manufacturerName": "Home Assistant",
            "additionalAttributes": {
                "manufacturer": "Home Assistant",
                "model": self.entity.domain,
                "softwareVersion": __version__,
                "customIdentifier": self.entity_id,
            },
        }

        locale = self.config.locale
        capabilities = []

        for i in self.interfaces():
            if locale not in i.supported_locales:
                continue

            try:
                capabilities.append(i.serialize_discovery())
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(
                    "Error serializing %s discovery for %s", i.name(), self.entity
                )

        result["capabilities"] = capabilities

        return result


@callback
def async_get_entities(hass, config) -> List[AlexaEntity]:
    """Return all entities that are supported by Alexa."""
    entities = []
    for state in hass.states.async_all():
        if state.entity_id in CLOUD_NEVER_EXPOSED_ENTITIES:
            continue

        if state.domain not in ENTITY_ADAPTERS:
            continue

        alexa_entity = ENTITY_ADAPTERS[state.domain](hass, config, state)

        if not list(alexa_entity.interfaces()):
            continue

        entities.append(alexa_entity)

    return entities


@ENTITY_ADAPTERS.register(media_player.const.DOMAIN)
class MediaPlayerCapabilities(AlexaEntity):
    """Class to represent MediaPlayer capabilities."""

    def default_display_categories(self):
        """Return the display categories for this entity."""
        device_class = self.entity.attributes.get(ATTR_DEVICE_CLASS)
        if device_class == media_player.DEVICE_CLASS_SPEAKER:
            return [DisplayCategory.SPEAKER]

        return [DisplayCategory.TV]

    def interfaces(self):
        """Yield the supported interfaces."""
        yield AlexaPowerController(self.entity)

        supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
        if supported & media_player.const.SUPPORT_VOLUME_SET:
            yield AlexaSpeaker(self.entity)
        elif supported & media_player.const.SUPPORT_VOLUME_STEP:
            yield AlexaStepSpeaker(self.entity)

        playback_features = (
            media_player.const.SUPPORT_PLAY
            | media_player.const.SUPPORT_PAUSE
            | media_player.const.SUPPORT_STOP
            | media_player.const.SUPPORT_NEXT_TRACK
            | media_player.const.SUPPORT_PREVIOUS_TRACK
        )
        if supported & playback_features:
            yield AlexaPlaybackController(self.entity)
            yield AlexaPlaybackStateReporter(self.entity)

        if supported & media_player.const.SUPPORT_SEEK:
            yield AlexaSeekController(self.entity)

        if supported & media_player.SUPPORT_SELECT_SOURCE:
            inputs = AlexaInputController.get_valid_inputs(
                self.entity.attributes.get(
                    media_player.const.ATTR_INPUT_SOURCE_LIST, []
                )
            )
            if len(inputs) > 0:
                yield AlexaInputController(self.entity)

        if supported & media_player.const.SUPPORT_PLAY_MEDIA:
            yield AlexaChannelController(self.entity)
            yield AlexaRemoteVideoPlayer(self.entity)

        if supported & media_player.const.SUPPORT_SELECT_SOUND_MODE:
            inputs = AlexaInputController.get_valid_inputs(
                self.entity.attributes.get(media_player.const.ATTR_SOUND_MODE_LIST, [])
            )
            if len(inputs) > 0:
                yield AlexaEqualizerController(self.entity)

        yield AlexaLauncher(self.entity)

        yield AlexaEndpointHealth(self.hass, self.entity)
        yield Alexa(self.hass)

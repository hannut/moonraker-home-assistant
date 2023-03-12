"""Button platform for Moonraker integration."""
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from .const import DOMAIN, METHOD
from .entity import BaseMoonrakerEntity


@dataclass
class MoonrakerButtonDescription(ButtonEntityDescription):
    """Class describing Mookraker button entities."""

    press_fn: Callable | None = None
    button_name: str | None = None
    icon: str | None = None
    unit: str | None = None
    device_class: str | None = None


BUTTONS: tuple[MoonrakerButtonDescription, ...] = [
    MoonrakerButtonDescription(
        key="emergency_stop",
        name="Emergency Stop",
        press_fn=lambda button: button.coordinator.async_send_data(
            METHOD.PRINTER_EMERGENCY_STOP
        ),
        icon="mdi:alert-octagon-outline",
    ),
]


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MoonrakerButton(coordinator, entry, desc) for desc in BUTTONS])


class MoonrakerButton(BaseMoonrakerEntity, ButtonEntity):
    """MoonrakerSensor Sensor class."""

    def __init__(self, coordinator, entry, description):
        super().__init__(coordinator, entry)
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_name = description.name
        self._attr_has_entity_name = True
        self.entity_description = description
        self._attr_icon = description.icon
        self.press_fn = description.press_fn

    async def async_press(self) -> None:
        """Press the button."""
        await self.press_fn(self)

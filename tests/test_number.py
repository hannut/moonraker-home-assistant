"""Number Tests."""

from unittest.mock import patch

import pytest
from homeassistant.components.number import DOMAIN as NUMBER_DOMAIN
from homeassistant.components.number import SERVICE_SET_VALUE
from homeassistant.const import ATTR_ENTITY_ID
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.moonraker.const import DOMAIN, METHODS

from .const import MOCK_CONFIG


@pytest.fixture(name="bypass_connect_client", autouse=True)
def bypass_connect_client_fixture():
    """Skip calls to get data from API."""
    with patch("custom_components.moonraker.MoonrakerApiClient.start"):
        yield


# test number
@pytest.mark.parametrize(
    "number",
    [("mainsail_output_pin_pwm"), ("mainsail_output_pin_CAPITALIZED")],
)
async def test_number_set_value(hass, number, get_default_api_response):
    """Test."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    with patch(
        "moonraker_api.MoonrakerClient.call_method",
        return_value={**get_default_api_response},
    ) as mock_api:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            SERVICE_SET_VALUE,
            {
                ATTR_ENTITY_ID: f"number.{number}",
                "value": 50,
            },
            blocking=True,
        )

        mock_api.assert_any_call(
            METHODS.PRINTER_GCODE_SCRIPT.value,
            script=f"SET_PIN PIN={number.split('_')[3]} VALUE=0.5",
        )

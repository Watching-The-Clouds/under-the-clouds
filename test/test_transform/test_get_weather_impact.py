import pytest
from transform_utils import get_weather_impact


def test_light_rain_codes():
    light_rain_codes = [200, 201, 230, 231, 232, 300, 301, 302, 310, 311, 500, 501, 520]
    for code in light_rain_codes:
        assert get_weather_impact(code) == "light_rain"


def test_heavy_rain_codes():
    heavy_rain_codes = [202, 312, 313, 314, 321, 502, 503, 504, 511, 521, 522, 531]
    for code in heavy_rain_codes:
        assert get_weather_impact(code) == "heavy_rain"


def test_snow_codes():
    snow_codes = [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622]
    for code in snow_codes:
        assert get_weather_impact(code) == "snow"


def test_clear_codes():
    clear_codes = [
        800,
        801,
        802,
        803,
        804,
        701,
        711,
        721,
        731,
        741,
        751,
        761,
        762,
        771,
        781,
    ]
    for code in clear_codes:
        assert get_weather_impact(code) == "clear"


def test_unknown_weather_codes():
    unknown_codes = [-1, 0, 999, 1000]
    for code in unknown_codes:
        assert get_weather_impact(code) == "Unknown weather code"

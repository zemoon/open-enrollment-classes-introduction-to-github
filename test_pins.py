import geojson
from path import path

def test_geojson():
    try:
        s = path("class-pins.topojson").bytes()
        rawJson = geojson.loads(s)
        assert True
    except:
        assert False

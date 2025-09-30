from kivy_garden.mapview import MapView, MapMarker
from kivy.app import MDapp


class Map(MDapp):
    def __init__(self):
        self.map_view = MapView(zoom=10, lat=0, lon=0)
    

    def build(self):
        return self.map_view

    def get_map_view(self):
        return self.map_view

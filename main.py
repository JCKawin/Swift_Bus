from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView, MapMarker
from plyer import gps
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from math import radians, sin, cos, sqrt, atan2
import requests
from kivy.uix.button import Button
from functools import partial
from kivy.utils import platform

SERVER_URL = "http://172.20.163.95:5000"

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    return R*c

class UserScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markers = []
        self.user_location = None
        self.mapview = None  # will be assigned from kv

    def on_enter(self):
        if platform == "android" or platform == "ios":
            gps.configure(on_location=self.update_user_location)
            gps.start()
        else:
            # Mock location for desktop testing
            self.user_location = (12.9716, 77.5946)  # Example coordinates (Bangalore)
            if self.mapview:
                self.mapview.center_on(*self.user_location)
            self.update_map()
    def update_user_location(self, **kwargs):
        lat, lon = kwargs['lat'], kwargs['lon']
        self.user_location = (lat, lon)
        if self.mapview:
            self.mapview.center_on(lat, lon)
        self.update_map()

    def update_map(self):
        if not self.mapview:
            return

        for marker in self.markers:
            self.mapview.remove_widget(marker)
        self.markers.clear()

        try:
            res = requests.get(f"{SERVER_URL}/buses").json()
            buses = res.get('buses', [])
            nearest_dist = float('inf')
            nearest_bus = None

            for bus in buses:
                marker = MapMarker(lat=bus['lat'], lon=bus['lon'], source="bus-icon.png")
                self.mapview.add_widget(marker)
                self.markers.append(marker)

                if self.user_location:
                    dist = haversine(self.user_location[0], self.user_location[1], bus['lat'], bus['lon'])
                    if dist < nearest_dist:
                        nearest_dist = dist
                        nearest_bus = bus

            if nearest_bus:
                print(f"Nearest bus: {nearest_bus['lat']}, {nearest_bus['lon']}, distance: {nearest_dist:.2f} km")

            if self.ids.broadcast_label:
                self.ids.broadcast_label.text = res.get('broadcast', '')

        except Exception as e:
            print(f"Error updating map: {e}")

class DriverScreen(Screen):
    bus_id = "default_bus_id"

    def on_enter(self):
        gps.configure(on_location=self.update_location, on_status=self.on_gps_status)
        gps.start()

    def update_location(self, **kwargs):
        lat, lon = kwargs['lat'], kwargs['lon']
        try:
            requests.post(f"{SERVER_URL}/update_location", json={
                "bus_id": self.bus_id, "lat": lat, "lon": lon})
        except Exception as e:
            print(f"Failed to update location: {e}")

    def send_broadcast(self, message):
        try:
            requests.post(f"{SERVER_URL}/broadcast", json={
                "bus_id": self.bus_id, "message": message})
        except Exception as e:
            print(f"Failed to send broadcast: {e}")

    def on_gps_status(self, status, provider):
        print(f"GPS status: {status} provider: {provider}")

class AccountScreen(Screen):
    pass

class BroadcastScreen(Screen):
    pass




class MainApp(App):
    def build(self):
        sm = ScreenManager()
        self.user_screen = UserScreen(name="user")
        self.driver_screen = DriverScreen(name="driver")
        self.account_screen = AccountScreen(name="account")
        self.broadcast_screen = BroadcastScreen(name="broadcast")

        sm.add_widget(self.user_screen)
        sm.add_widget(self.driver_screen)
        sm.add_widget(self.account_screen)
        sm.add_widget(self.broadcast_screen)

        root = BoxLayout(orientation='vertical')
        root.add_widget(sm)

        dock = BoxLayout(size_hint_y=None, height=dp(50))

        def set_screen(screen_name, *args):
            sm.current = screen_name
        
        # Define set_screen BEFORE using it in partial
        dock.add_widget(Button(text='Account', on_press=partial(set_screen, 'account')))
        dock.add_widget(Button(text='Map', on_press=partial(set_screen, 'user')))
        dock.add_widget(Button(text='Broadcast', on_press=partial(set_screen, 'broadcast')))

        root.add_widget(dock)

        return root


if __name__ == "__main__":
    MainApp().run()

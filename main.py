import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
import map
class MainScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.main_screen = MainScreen(name='main')
        self.sm.add_widget(self.main_screen)

        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Welcome to the Swift Bus App", size_hint_y=None, height=50)
        layout.add_widget(self.label)

        self.map_box = BoxLayout(size_hint_y=None, height=400)
        self.map_box.add_widget(self.map_view())

        get_bus_location_btn = Button(text="Get Bus Location", size_hint_y=None, height=50)
        layout.add_widget(get_bus_location_btn)

        self.file_path_input = TextInput(text="", size_hint_y=None, height=50, readonly=True)
        layout.add_widget(self.file_path_input)

        self.image_display = Image(size_hint_y=None, height=300)
        layout.add_widget(self.image_display)

        self.main_screen.add_widget(layout)
        return self.sm
    
    def map_view(self):
        m = map.Map()
        return m.get_map_view()


if __name__ == '__main__':
    MyApp().run()
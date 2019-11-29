from functools import partial

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from specialbuttons import ImageButton, LabelButton
from kivy.graphics import Color, Rectangle
import kivy.utils
from kivy.app import App


# Add a available drivers banner on mainpassenger of firebase database
class DriversBanner(GridLayout):
    def __init__(self, **kwargs):
        super(DriversBanner, self).__init__()
        self.rows = 1
        app = App.get_running_app()
        with self.canvas.before:
            # Setting background of banner in a scroll screen
            Color(rgb=(kivy.utils.get_color_from_hex("f4f4f4")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        # Make refresh and eliminate trip <-------------*****

        # Layout banner
        available_driver = FloatLayout()
        # Add avatar drivers
        image = Image(source=f"resources/avatars/{kwargs['avatar']}", size_hint=(0.2, 1),
                      pos_hint={"x": 0.05, "top": 1})
        # Add info trip
        label = LabelButton(text=f'{kwargs["name"]} {kwargs["last_name"]}\n'
                                 f'Salida a las {kwargs["leave_hour"]}\n'
                                 f'De {kwargs["desde"]} para {kwargs["to"]}\n'
                                 f'Cel: {kwargs["cel"]}, Patente: {kwargs["plate"]}',
                            size_hint=(0.8, 1), pos_hint={"x": 0.2, "top": 1}, markup=True,
                            color=kivy.utils.get_color_from_hex("#000000"),
                            on_release=partial(App.get_running_app().load_info_driver_available))

        available_driver.add_widget(image)
        available_driver.add_widget(label)

        self.add_widget(available_driver)

    # Setting background banner
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class PassengerBanner(GridLayout):
    def __init__(self, **kwargs):
        super(PassengerBanner, self).__init__()
        self.rows = 1
        app = App.get_running_app()
        with self.canvas.before:
            # Setting background of banner in a scroll screen
            Color(rgb=(kivy.utils.get_color_from_hex("f4f4f4")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        # Layout banner
        available_passenger = FloatLayout()
        # Add avatar drivers
        image = Image(source=f"resources/avatars/{kwargs['avatar']}", size_hint=(0.2, 1),
                      pos_hint={"x": 0.05, "top": 1})
        # Add info trip
        label = Label(text=f'{kwargs["name"]} {kwargs["last_name"]}\n'
                           f'Salida a las {kwargs["leave_hour"]}\n'
                           f'De {kwargs["desde"]} para {kwargs["to"]}\n'
                           f'Cel: {kwargs["cel"]}',
                      size_hint=(0.8, 1), pos_hint={"x": 0.2, "top": 1}, halign="center",
                      color=kivy.utils.get_color_from_hex("#000000"))

        available_passenger.add_widget(image)
        available_passenger.add_widget(label)

        self.add_widget(available_passenger)

    # Setting background banner
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class InfoDriversBanner(GridLayout):
    def __init__(self, **kwargs):
        super(InfoDriversBanner, self).__init__()
        self.rows = 1
        app = App.get_running_app()
        with self.canvas.before:
            # Setting background of banner in a scroll screen
            Color(rgb=(kivy.utils.get_color_from_hex("f4f4f4")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        # Make refresh and eliminate trip <-------------*****

        # Layout banner
        available_driver = FloatLayout()
        # Add avatar drivers
        image = Image(source=f"resources/avatars/{kwargs['avatar']}", size_hint=(0.2, 1),
                      pos_hint={"x": 0.05, "top": 1})
        # Add info trip
        label = LabelButton(text=f'{kwargs["name"]} {kwargs["last_name"]}\n'
                                 f'Salida a las {kwargs["leave_hour"]}\n'
                                 f'De {kwargs["desde"]} para {kwargs["to"]}\n'
                                 f'Cel: {kwargs["cel"]}, Patente: {kwargs["plate"]}',
                            size_hint=(0.8, 1), pos_hint={"x": 0.2, "top": 1}, markup=True,
                            color=kivy.utils.get_color_from_hex("#000000"))

        available_driver.add_widget(image)
        available_driver.add_widget(label)

        self.add_widget(available_driver)

    # Setting background banner
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

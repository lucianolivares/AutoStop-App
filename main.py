from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from available_banners import DriversBanner, PassengerBanner, InfoDriversBanner
from kivy.config import Config
from kivy.uix.label import Label
from os import walk
from functools import partial
from myfirebase import MyFirebase
import requests
import json

# Screen size settings
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '720')


# Login Screen <- Inside login
class LoginScreen(Screen):
    pass


# Register Screen <- Inside login
class CreateScreen(Screen):
    pass


# AddCar Screen <- Inside login
class AddCar(Screen):
    pass


# Principal Screen Driver <- Inside driver
class DriverScreen(Screen):
    pass


# Principal Screen Passenger <- Inside passenger
class MainPassenger(Screen):
    pass


# Add to Queue Passenger  <- Inside passenger
class AddRequest(Screen):
    pass


# Trip selected Screen <- Inside passenger
class InfoTrip(Screen):
    pass


# Settings Users Screen <- Inside passenger
class AccountSettings(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = "passenger"

    def change_mode(self, m):
        self.mode = m


class AddAvailableDriver(Screen):
    pass


# Settings Change Avatar <- Inside passenger
class ChangeAvatarScreen(Screen):
    pass


# Button + Image
class ImageButton(ButtonBehavior, Image):
    pass


# Button + Label
class LabelButton(ButtonBehavior, Label):
    pass


# Import Design
GUI = Builder.load_file("main.kv")


class MainApp(App):
    refresh_token_file = "refresh_token.txt"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.my_firebase = MyFirebase()
        return GUI

    def on_start(self):
        # Populate change avatar grid
        avatar_grid = self.root.ids['change_avatar_screen'].ids['avatar_grid']
        for root_dir, folders, png in walk("resources/avatars"):
            for p in png:
                img = ImageButton(source="resources/avatars/" + p, on_release=partial(self.change_avatar, p))
                avatar_grid.add_widget(img)

        # Get available drivers database
        all_data_request = requests.get(f'https://sube-y-baja-app.firebaseio.com/available_drivers.json')
        drivers = json.loads(all_data_request.content.decode())
        # Available Drivers
        # Get and update available drivers banner
        available_driver_banner = self.root.ids["main_passenger"].ids["banner_grid"]
        for driver in drivers:
            current = drivers[driver]
            banner = DriversBanner(name=current['name'], last_name=current['last_name'],
                                   leave_hour=current['leave_hour'],
                                   desde=current['from'], to=current['to'],
                                   cel=current['cel'], plate=current['plate'],
                                   avatar=current['avatar'])
            available_driver_banner.add_widget(banner)

        # Get available passenger database
        available_passenger_request = requests.get(f'https://sube-y-baja-app.firebaseio.com/available_passenger.json')
        passengers = json.loads(available_passenger_request.content.decode())
        # Available Passenger
        # Get and update available passenger banner
        available_passenger_banner = self.root.ids["driver_screen"].ids["passenger_available_grid"]
        for passenger in passengers:
            current = passengers[passenger]
            banner = PassengerBanner(name=current['name'], last_name=current['last_name'],
                                     leave_hour=current['hour'],
                                     desde=current['from'], to=current['to'],
                                     cel=current['cel'],
                                     avatar=current['avatar'])
            available_passenger_banner.add_widget(banner)

        try:
            # Try to read the persisten signing credentials (refresh token)
            with open("refresh_token.txt", 'r') as f:
                refresh_token = f.read()
            # Use refresh token to get a new idToken
            self.id_token, self.local_id = self.my_firebase.exchange_refresh_token(refresh_token)

            # Get database data
            result = requests.get(
                f'https://sube-y-baja-app.firebaseio.com/Users/{self.local_id}.json?auth={self.id_token}')
            data = json.loads(result.content.decode())
            # Feature of User
            self.user_name = data["name"]
            self.last_name = data["last_name"]
            self.email = data["email"]
            self.cel = data["cel"]
            self.avatar = data["avatar"]
            self.plate = data["plate"]
            # Get and update account settings
            account_settings_id = self.root.ids["account_settings"].ids
            avatar_setting = account_settings_id["avatar_setting"]
            avatar_setting.source = f'resources/avatars/{self.avatar}'
            name_setting = account_settings_id["name"]
            name_setting.text = f'{self.user_name} {self.last_name}\n' \
                                f'{self.email}'
            cel_settings = account_settings_id["cel"]
            cel_settings.text = str(self.cel)
            # pass_settings = self.root.ids["account_settings"].ids["password"]

            self.root.ids["screen_manager"].transition = NoTransition()
            self.change_screen("main_passenger")
            self.root.ids["screen_manager"].transition = CardTransition()

        except:
            pass

    def change_avatar(self, image, widget_id):
        # Change avatar in the app
        avatar_setting = self.root.ids["account_settings"].ids["avatar_setting"]
        avatar_setting.source = f'resources/avatars/{image}'
        # Change avatar in firebase database
        my_data = '{"avatar": "%s" }' % image
        requests.patch(f'https://sube-y-baja-app.firebaseio.com/Users/{self.local_id}.json?auth={self.id_token}',
                       data=my_data)
        self.change_screen("account_settings")

    def add_request(self):
        # Get all data of fields of add_request Screen
        requests_ids = self.root.ids["add_request"].ids
        desde_input = requests_ids["desde"].text
        para_input = requests_ids["para"].text
        hora_input = requests_ids["hora"].text
        n_passenger_input = requests_ids["n_passenger"].text
        # Make sure fields aren't garbage
        if desde_input == "":
            requests_ids["desde"].background_color = (1, 0, 0, 1)
            return
        if para_input == "":
            requests_ids["para"].background_color = (1, 0, 0, 1)
            return
        if hora_input == "":
            requests_ids["hora"].background_color = (1, 0, 0, 1)
            return
        try:
            int_n_passenger = int(n_passenger_input)
        except:
            requests_ids["n_passenger"].background_color = (1, 0, 0, 1)
            return

        # If all data is ok, send data to firebase real-time database
        request_payload = {
            "n_pasajeros": n_passenger_input,
            "avatar": self.avatar,
            "cel": self.cel,
            "from": desde_input,
            "last_name": self.last_name,
            "hour": hora_input,
            "name": self.user_name,
            "to": para_input
        }
        request_request = requests.post("https://sube-y-baja-app.firebaseio.com/available_passenger.json",
                                        data=json.dumps(request_payload))

    def add_available_driver(self):
        # Get all data of fields of add_request Screen
        requests_ids = self.root.ids["add_available_driver"].ids
        desde_input = requests_ids["desde"].text
        para_input = requests_ids["para"].text
        hora_input = requests_ids["hora"].text
        available_seats = requests_ids["available_seats"].text
        # Make sure fields aren't garbage
        if desde_input == "":
            requests_ids["desde"].background_color = (1, 0, 0, 1)
            return
        if para_input == "":
            requests_ids["para"].background_color = (1, 0, 0, 1)
            return
        if hora_input == "":
            requests_ids["hora"].background_color = (1, 0, 0, 1)
            return
        try:
            int_available_seats = int(available_seats)
        except:
            requests_ids["available_seats"].background_color = (1, 0, 0, 1)
            return

        # If all data is ok, send data to firebase real-time database
        request_payload = {
            "available_seats": available_seats,
            "avatar": self.avatar,
            "cel": self.cel,
            "from": desde_input,
            "last_name": self.last_name,
            "leave_hour": hora_input,
            "name": self.user_name,
            "to": para_input,
            "plate": self.plate
        }
        request_request = requests.post("https://sube-y-baja-app.firebaseio.com/available_drivers.json",
                                        data=json.dumps(request_payload))

    def sign_out_user(self):
        # User wants to log out
        with open(self.refresh_token_file, "w") as f:
            f.write("")
        self.change_screen("login_screen", direction='down', mode='push')
        # Need to set the avatar to the default image
        avatar_setting = self.root.ids["account_settings"].ids["avatar_setting"]
        avatar_setting.source = "resources/avatars/man.png"

        # Need to clear widgets from previous user's drivers available
        driver_available_banner = self.root.ids['main_passenger'].ids['banner_grid']
        passenger_available_banner = self.root.ids['driver_screen'].ids['passenger_available_grid']
        for w in driver_available_banner.walk():
            if w.__class__ == DriversBanner:
                driver_available_banner.remove_widget(w)

        # Need to clear widgets from previous user's friend's passenger available
        passenger_available_banner = self.root.ids['driver_screen'].ids['passenger_available_grid']
        for w in passenger_available_banner.walk():
            if w.__class__ == PassengerBanner:
                passenger_available_banner.remove_widget(w)

    def load_info_driver_available(self, widget):
        # Get available drivers database
        info_driver_request = requests.get(f'https://sube-y-baja-app.firebaseio.com/available_drivers/shano.json')
        info_driver = json.loads(info_driver_request.content.decode())
        # Available Drivers
        # Get and update available drivers banner
        available_driver_banner = self.root.ids["info_trip"].ids["driver_banner"]
        banner = InfoDriversBanner(name=info_driver['name'], last_name=info_driver['last_name'],
                                   leave_hour=info_driver['leave_hour'],
                                   desde=info_driver['from'], to=info_driver['to'],
                                   cel=info_driver['cel'], plate=info_driver['plate'],
                                   avatar=info_driver['avatar'])
        available_driver_banner.add_widget(banner)

        self.change_screen("info_trip")

    def change_screen(self, screen_name, direction='forward', mode=""):
        # Get the screen manager from the kv file
        screen_manager = self.root.ids['screen_manager']
        # print(direction, mode)
        # If going backward, change the transition. Else make it the default
        # Forward/backward between pages made more sense to me than left/right
        if direction == 'forward':
            mode = "push"
            direction = 'left'
        elif direction == 'backwards':
            direction = 'right'
            mode = 'pop'
        elif direction == "None":
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return

        screen_manager.transition = CardTransition(direction=direction, mode=mode)

        screen_manager.current = screen_name


MainApp().run()

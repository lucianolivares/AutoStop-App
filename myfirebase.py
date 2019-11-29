import requests
import json
from kivy.app import App


class MyFirebase():
    wak = ""  # Web Api Key

    def sign_up(self, email, password, user_name, last_name, alias, cel, address, comuna):
        app = App.get_running_app()
        # Send email and password to Firebase
        # Firebase will return localId, authToken (idToken), refreshToken
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        signup_payload = {"email": email, "password": password, "returnSecureToken": True}
        sign_up_request = requests.post(signup_url, data=signup_payload)
        sign_up_data = json.loads(sign_up_request.content.decode())
        if sign_up_request.ok:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            # Save refreshToken to a file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            # Save localId to a variable in main app class
            # Save idToken to a variable in main app class
            app.local_id = localId
            app.id_token = idToken

            # Create new key in database from localId
            # Empty features
            my_data = '{"address": "%s", "avatar": "man.png", "capacity": "N/A", "cel": "%s",' \
                      '"city": "%s", "color": "azul", "email": "%s", "alias": "%s", "last_name": "%s",' \
                      '"name": "%s", "password": "%s", "plate": "N/A", "rut": "N/A"}' % (address, cel, comuna, email,
                                                                                         alias, last_name, user_name,
                                                                                         password)
            post_request = requests.patch(f'https://sube-y-baja-app.firebaseio.com/Users/{localId}.json?auth={idToken}',
                                          data=my_data)
            print(post_request.ok)
            print(json.loads(post_request.content.decode()))

            app.change_screen("main_passenger")

        elif not sign_up_request.ok:
            error_data = json.loads(sign_up_request.content.decode())
            error_message = error_data["error"]["message"]
            app.root.ids["login_screen"].ids["login_message"].text = error_message

        pass

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        id_token = refresh_req.json()['id_token']
        local_id = refresh_req.json()['user_id']
        return id_token, local_id

    def sign_in_existing_user(self, email, password):
        """Called if a user tried to sign up and their email already existed."""
        signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.wak
        signin_payload = {"email": email, "password": password, "returnSecureToken": True}
        signin_request = requests.post(signin_url, data=signin_payload)
        sign_up_data = json.loads(signin_request.content.decode())
        app = App.get_running_app()

        if signin_request.ok:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            # Save refreshToken to a file
            with open(app.refresh_token_file, "w") as f:
                f.write(refresh_token)

            # Save localId to a variable in main app class
            # Save idToken to a variable in main app class
            app.local_id = localId
            app.id_token = idToken

            # Create new key in database from localId Get friend ID Get request on firebase to get the next friend id
            # --- User exists so i don't need to get a friend id self.friend_get_req = UrlRequest(
            # "https://friendly-fitness.firebaseio.com/next_friend_id.json?auth=" + idToken,
            # on_success=self.on_friend_get_req_ok)
            app.root.ids['login_screen'].ids['email'].text = ""
            app.root.ids['login_screen'].ids['password'].text = ""
            app.change_screen("main_passenger")
            app.on_start()

        elif not signin_request.ok:
            error_data = json.loads(signin_request.content.decode())
            error_message = error_data["error"]['message']
            app.root.ids['login_screen'].ids['login_message'].text = "EMAIL EXISTS - " + error_message.replace("_", " ")


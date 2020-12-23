from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import certifi
import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from json import dumps
import os.path
import progressspinner

# Load the kv files
folder = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(folder + "/themedwidgets.kv")
Builder.load_file(folder + "/signinscreen.kv")
Builder.load_file(folder + "/loadingpopup.kv")

# Import the screens used to log the user in
from signinscreen import SignInScreen
from facerec_from_webcam_faster import recog_procedure 

Builder.load_string('''
<CustomPopup>:
    size_hint: .5, .5
    auto_dismiss: False
    background_color: [0, 0, 0, 0.3]
    opacity: 0.7
    title: 'Login Error'
    Button:
        text: 'Could not log-in'
        on_press: root.dismiss()
''')


class CustomPopup(Popup):
    pass




class Login(Screen, EventDispatcher):
  students_codes = []
  login_success = BooleanProperty(False)  # Called upon successful sign in
  code_exists = BooleanProperty(False)
  code_not_found = BooleanProperty(False)

  #debug = True
  popup = Factory.LoadingPopup()
  popup.background = folder + "/transparent_image.png"
  
  def on_login_success(self, *args):
    print("Logged in successfully", args)

  def sign_in(self, code):
    stored_path = os.listdir("./stored/")
    code_dir = { person for person in stored_path }

    validated = False
    if code in code_dir:
      validated = recog_procedure(code)
    
    if validated:
      self.login_success = True
    else:
      p = CustomPopup()
      p.open()
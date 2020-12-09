from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
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
    if code == "201912345":
      self.login_success = True
    else:
      print("Cannot log in")

import kivy

kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.clock import Clock
from subprocess import *

Builder.load_file("pigui.kv")

controller_server = "yutao@192.168.1.149"
controller_path = "/home/yutao/PycharmProjects/archhack/VendingMachine_Control"
base_path = "/home/pi/script/"
image_file = "image.jpg"


screen_manager = ScreenManager()

class ScreenPickUp(Screen):
    # function that handles a pickup request
    def start_pick_up(self):
        screen_manager.transition.direction = "up"
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_ready_take_photo"

class ScreenReadyTakePhoto(Screen):
    def start_veri(self):
        screen_manager.transition.direction = "up"
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_take_photo"
        Clock.schedule_once(self.delayed_job, 0.8)

    def delayed_job(self, dt):
        self.manager.get_screen("screen_take_photo").call_take_photo()

class ScreenTakePhoto(Screen):

    def call_take_photo(self):
        check_call(["python", base_path + "capture.py"])
        check_call(["scp", image_file, controller_server + ":" + controller_path])
        self.photo_finish()

    def photo_finish(self):
        result = check_output(["ssh", controller_server, "cd " + controller_path + ";" + "python Verify.py"])

        if (result.strip() == "1"):
            print("Passed")
            screen_manager.transition.direction = "up"
            screen_manager.transition.duration = 1
            screen_manager.current = "screen_pass"
            #Clock.schedule_once(self.delayed_restart, 15)
        else:
            screen_manager.transition.direction = "up"
            screen_manager.transition.duration = 1
            screen_manager.current = "screen_no_pass"


    def delayed_restart(self, dt):
        self.re_start()

    def re_start(self):
        screen_manager.transition.direction = "down"
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_pick_up"


class ScreenPass(Screen):
    #deliver_checkbox = ObjectProperty()

    def deliver(self):
        #print("start deliver")
        check_call(["python", "/home/pi/script/send_out.py"])
        #print("finish deliver")

    def restart(self):
        screen_manager.transition.direction = "down"
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_pick_up"

class ScreenNoPass(Screen):
    def restart(self):
        screen_manager.transition.direction = "down"
        screen_manager.transition.duration = 1
        screen_manager.current = "screen_pick_up"


screen_manager.add_widget(ScreenPickUp(name="screen_pick_up"))
screen_manager.add_widget(ScreenReadyTakePhoto(name="screen_ready_take_photo"))
screen_manager.add_widget(ScreenTakePhoto(name="screen_take_photo"))
screen_manager.add_widget(ScreenPass(name="screen_pass"))
screen_manager.add_widget(ScreenNoPass(name="screen_no_pass"))


class PiGuiApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return screen_manager



pi_app = PiGuiApp()
pi_app.run()

# from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty,NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock, mainthread
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.dialog import MDDialog
import plyer
import time
import schedule

# global time_text


class MainScreen(Screen, FloatLayout):
    mantra_text = ObjectProperty(None)  # this is the text input id

    def printMantra(self):
        print(self.ids.mantra_text.text)

    def icon_popup(self):  # creates the popup window with the icons in it
        popup = Popup(title="Profile Icon", content=Popup_Content(), size_hint=(0.8, 0.3))
        popup.open()

    def hour_pop(self):
        popup = Popup(title="Hour", content=Hour_Time(), size_hint=(0.2, 0.5))
        popup.open()


# This contains the content of the popup window for the profile icons
class Popup_Content(RelativeLayout):
    pass


# This contains the content of the popup window that will display the user's text input
class Mantra_Message_Popup(RelativeLayout):
    pass


class Hour_Time(RelativeLayout):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Mantra App"
        #theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Lime"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        super().__init__(**kwargs)

    # variables for kv file to interact with(the displayed user set time)
    hour = NumericProperty()
    minute = NumericProperty()

    def build(self):
        # calling the service
        if platform == "android":
            from android import AndroidService
            service = AndroidService("my pong service", "running")
            service.start("service started")
            self.service = service

        return MainScreen()

    # displays the clock for the user to choose the time
    def show_timepicker(self):
        picker = MDTimePicker()
        picker.bind(time=self.got_time)
        picker.open()

    def got_time(self, picker_widget, time):
        # check if it is am or pm so as to add the prefix 0
        self.hour = time.hour
        self.minute = time.minute
        if self.hour >= 10 and self.minute >= 10:
            schedule.every().day.at(f'{int(self.hour)}:{int(self.minute)}').do(self.show_MDDialogue)
        elif self.hour < 10 and self.minute < 10:
            schedule.every().day.at(str(0)+str(self.hour) + ":" + str(0) + str(self.minute)).do(self.mantraPop_message)
        Clock.schedule_interval(lambda dt: schedule.run_pending(), 1)
        print(f'{int(self.hour)}:{int(self.minute)}')

    # sets the profile icon
    def set_profile_icon(self, image):
        self.root.ids.profile_icon.source = image.source
        print(image)
        # print(self.root.ids.popup_content.ids)

    # @mainthread Notification setup
    def show_notification(self, *args):
        plyer.notification.notify(title='Gentle Reminder', message=self.root.ids.mantra_text.text, timeout=86400, toast=True)
        print("Yahs")

    # displays user input in the message popup window
    def mantraPop_message(self):
        pop = Popup(title="Message", content=Mantra_Message_Popup(), size_hint=(0.8, 0.3))
        pop.open()
        print("We out here!")

    # Popup Window that displays the user's written word
    def show_MDDialogue(self):
        my_dialogue = MDDialog(title="Gentle reminder", text=self.root.ids.mantra_text.text, size_hint=[0.5, 0.5],
                               buttons=[
                                   MDRaisedButton(text=self.root.ids.mantra_text.text,
                                                  text_color=self.theme_cls.primary_color)
                               ])
        my_dialogue.open()

    def my_callback(self, *args):
        from kivymd.toast.kivytoast import toast
        toast(args[0])


if __name__ == "__main__":
    MainApp().run()

# make user able to input time to schedule the mantra text --> COMPLETE
# make app able to run in the background
# database: login and staying logged in
# exportation of file into apk
# wrap the text in the popup window

# 2.0
# splash screen
# change popup theme
# add ads

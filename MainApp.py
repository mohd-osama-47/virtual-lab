#!/usr/bin/python3

# Kivy related imports for the GUI
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.behaviors import DragBehavior

SCREEN_RES = [960, 540]    # Set your desired screen size here please
Window.size = (SCREEN_RES[0],SCREEN_RES[1])

# KivyMD related imports for Material Design look
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFillRoundFlatButton

import os

#! Install these packages using pip please!
# They are used for correct arabic text viewing
from bidi import algorithm as bidiAlgorithm # Responsible for text direction fixing
import arabic_reshaper

def get_media_path(file):
    """
    Gets path for media file

    @param file: name of the media file
    @type file: str
    """
    media_path = os.path.join(os.getcwd(),file)
    return media_path

Config.set('kivy', 'default_font', get_media_path('font/Shoroq-Font.ttf'))

class ItemDrawer(OneLineListItem):
    '''
    Class for the side buttons of the side rail
    '''
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

class DrawerList(ThemableBehavior, MDList):
    '''
    Side rail container for navigation buttons.
    '''
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class BasicToggleButton(MDFillRoundFlatButton, MDToggleButton):
    '''
    Class allowing for a button to be toggled ON or OFF and stay in that state.
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_text_color = "Custom"

class Experiment1(MDScreen):
    '''
    Class for the first screen in the GUI
    '''
    def __init__(self, **kw):
        super().__init__(**kw)

class Experiment2(MDScreen):
    '''
    Class for the second screen in the GUI
    '''
    def __init__(self, **kw):
        super().__init__(**kw)

class CopperExperiment(Widget):
    '''
    Class representing the copper extraction experiment through the 
    application of a direct heat source
    '''
    #* Colors are represented in the RGBA format in a list
    brown = [0.72, 0.45, 0.2, 0.9] 
    blue = [0.12, 0.72, 0.60, 0.9]
    oxide_color = ListProperty(brown)   # Color of the material within the test tube
    flame_color = ListProperty(blue)    # color of the flame from the burner
    burner_on = BooleanProperty(False)  # Flag representing state of the burner (ON/OFF)
    start_animation = BooleanProperty(False)    # Flag to start or stop the color change animation
    
    def __init__(self, **kwargs):
        '''
        Constructor of the widget class
        '''
        super().__init__(**kwargs)
        # Bind the start_animnation flag to a function 
        # so that the function gets called whenever 
        # the varibale changes.
        self.bind(start_animation=self.anim_reaction)
        self.bind(burner_on=self.anim_heating)
        # Helper function that gets called 20 times a second to check for collision between the flame and the test tube.
        #! You can change the rate from 1/20 to something lower if performance is important for you
        Clock.schedule_interval(self.check_flame_collision, 1/20.)
    
    def anim_heating(self, *args):
        '''
        Creates an animation for the flame to come into view smoothly
        '''
        if self.burner_on:
            # means that the burner is now ON
            # start animation that changes color to blue
            Animation(opacity=1, step = 1/60, duration = 0.1).start(self.parent.ids.flame_object)
        else:
            # means burner is now OFF
            # start animation that changes color BACK to brown
            Animation(opacity=0, step = 1/60, duration = 0.1).start(self.parent.ids.flame_object)
            
    def anim_reaction(self, *args):
        '''
        Creates an animation for heating and desplaying the chemical reaction
        '''
        if self.start_animation:
            # means that the burner is now ON
            # start animation that changes color to blue
            Animation(oxide_color=self.blue, step = 1/10).start(self)
        else:
            # means burner is now OFF
            # start animation that changes color BACK to brown
            Animation(oxide_color=self.brown, step = 1/10).start(self)
    
    def check_flame_collision(self, *args):
        if not self.burner_on:
            # Means the button for the burner is not 
            # enabled, so do not trigger any animation
            self.start_animation = False
            return

        # Check if the tube object defined in the KV file is colliding with the flame object of the bunsen burner.
        collision = self.parent.ids.test_tube.collide_widget(self.parent.ids.flame_object)

        if collision:
            # self.oxide_color = self.blue
            self.start_animation = True
        else:
            # self.oxide_color = self.brown
            self.start_animation = False

class DragImage(DragBehavior, Image):
    pass

class GUIApp(MDApp):
    '''
    Main GUI app to create the chemistry lab environment.
    '''

    # Dict that contains all the screen names and their instances
    screen_dict = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.title = "Virtual Chemsitry Lab"
        self.title = 'مختبر الكيمياء اﻹفتراضي'
    
    def build(self):
        self.icon = get_media_path('media/icon.png')
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"  # use "Dark" for dark mode
        self.theme_cls.primary_hue = "100"  # "500"

        # Load each kv file for styles
        for file_name in os.listdir(get_media_path('include')):
            if '.kv' not in file_name:
                continue
            if 'main' in file_name:
                self.screen = Builder.load_file(get_media_path('include/main.kv'))
                continue
            Builder.load_file(get_media_path('include/')+ file_name)
        
        self.sm = self.screen.ids.sm
        self.sm.add_widget(Experiment1())
        self.sm.add_widget(Experiment2())

        self.experiment1 = self.screen.ids.sm.get_screen('experiment1')
        self.screen_dict["experiment1"] = self.experiment1
        self.experiment2 = self.screen.ids.sm.get_screen('experiment2')
        self.screen_dict["experiment2"] = self.experiment2

        return self.screen
    
    def switch_screen(self, instance_navigation_rail_item, screen_name):
        '''
        Called when tapping on rail menu items. Switches application screens.
        '''
        
        self.sm.switch_to(self.screen_dict[screen_name.lower()])
    
    def get_corrected_text(self, text_to_correct):
        '''
        Reverses text to support arabic writing
        '''
        text_to_correct = arabic_reshaper.reshape(text_to_correct)
        return bidiAlgorithm.get_display(text_to_correct)
    



if __name__ == '__main__':
    app = GUIApp()
    app.run()
    print("DONE EXECUTING THE APP. THANK YOU FOR USING IT!")
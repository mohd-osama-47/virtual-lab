#!/usr/bin/python3

# Kivy related imports for the GUI
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.behaviors import DragBehavior
from kivy.utils import get_color_from_hex

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
from random import randint
from math import sin, cos

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

class IonsExperiment(Widget):
    '''
    Class representing the Ion extraction experiment by 
    supplying a current source between two rods
    '''
    #* Colors are represented in the RGBA format in a list
    cu2_color  = get_color_from_hex("#6699FF")
    mno4_color = get_color_from_hex("#B319FF")
    def_color  = get_color_from_hex("#6C8387")
    cu_ions_color = ListProperty(def_color)   # Color of the Copper ions.
    mno_ions_color = ListProperty(def_color)   # Color of the Permanganate ions.
    current_on = BooleanProperty(False)  # Flag representing state of the burner (ON/OFF)
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
        self.bind(current_on=self.anime_current)
        # Helper function that gets called 20 times a second to check for collision between the flame and the test tube.
        #! You can change the rate from 1/20 to something lower if performance is important for you
        # Clock.schedule_interval(self.check_flame_collision, 1/20.)
    
    def anime_current(self, *args):
        '''
        Creates an animation for the current flow to come in view smoothly
        '''
        if self.current_on:
            # means that the burner is now ON
            # start animation that changes color to blue
            # Animation(opacity=1, step = 1/60, duration = 0.1).start(self.parent.ids.flame_object)
            self.start_animation = True
        else:
            # means burner is now OFF
            # start animation that changes color BACK to brown
            # Animation(opacity=0, step = 1/60, duration = 0.1).start(self.parent.ids.flame_object)
            self.start_animation = False
            
    def anim_reaction(self, *args):
        '''
        Creates an animation for displaying the chemical reaction
        '''
        if self.start_animation:
            # means that the current flow is now ON
            # start animation that changes colors
            Animation(cu_ions_color=self.cu2_color, step = 1/10).start(self)
            Animation(mno_ions_color=self.mno4_color, step = 1/10).start(self)
        else:
            # means current is now OFF
            # start animation that changes color BACK to default
            Animation(cu_ions_color=self.def_color, step = 1/10).start(self)
            Animation(mno_ions_color=self.def_color, step = 1/10).start(self)
    
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

class ParticleMesh(Widget):
    '''
    Class definition responsible for generating the animated particle effect in the background

    Attributes:
        - points (kivy ListProperty): list of all points that are moving in the background
        - color (kivy ListProperty): list of colors for each line connecting the points
        - line_color (kivy ListProperty): color of the generated line between points
        - point_count (kivy NumericProperty): amount of generated points

    Methods:
        - plot_points: generates all the points and initializes them with random directions, also starts a Clock function call that updates their position
        - draw_lines: draws lines between points based on their proximity
        - update_positions: update the position of points by moving them in increments, also checks if they went out of the bounds of the display
        - distance_between_points (static method): checks the euclidean distance between the points
        - off_screen (static method): returns a boolean to signify if a point is off bounds
    '''
    points = ListProperty()
    color = ListProperty(get_color_from_hex("#eeeeee88"))
    line_color = ListProperty([1,1,1])
    point_count = NumericProperty(30)
    move_to_pos = BooleanProperty(False)
    home_pos = NumericProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = []
        self.point_number = self.point_count
        # print(f'1:{self.width}, {self.height}')
        Clock.schedule_once(lambda dt: self.plot_points(), 0)

    def plot_points(self):
        '''
        Generates all the points in the background and starts a Clock event for updating their positions.
        '''
        for _ in range(self.point_number):
            #! Issue with getting screen size if you have other 
            #! Fixed with putting the screenmanager in a floatlayout
            # x = randint(0, self.width)
            # y = randint(0, self.height)
            x = randint(0, SCREEN_RES[0])
            y = randint(0, SCREEN_RES[1])
            self.points.extend([x, y])
            self.direction.append(randint(0, 359))
        # print('THE PARTICLE EFFECT LIST IS:', self.points)
        Clock.schedule_interval(self.update_positions, 1/30)
        

    def draw_lines(self):
        '''
        Draws all the lines and colours them according to how close the points at the tail ends of the line are.
        '''
        self.canvas.after.clear()
        with self.canvas.after:
            for i in range(0, len(self.points), 2):
                for j in range(i + 2, len(self.points), 2):

                    d = self.distance_between_points(self.points[i], self.points[i + 1], self.points[j],
                                                     self.points[j + 1])
                    if d > 200:
                        continue
                    color = 1 - d / 200
                    Color(rgba=[self.line_color[0]*color, self.line_color[1]*color, self.line_color[2]*color, 0.2])
                    Line(points=[self.points[i], self.points[i + 1], self.points[j], self.points[j + 1]], width = 3 * color)
    
    def update_positions(self, *args):
        '''
        Updates the points in increaments, also checks if a point went out of bounds
        '''
        step = 0.6
        for i, j in zip(range(0, len(self.points), 2), range(len(self.direction))):
            if not self.move_to_pos:
                theta = self.direction[j]
                self.points[i] += step * cos(theta)
                self.points[i + 1] += step * sin(theta)
                if self.off_screen(self.points[i], self.points[i + 1]):
                    self.direction[j] = 90 + self.direction[j]
            else:
                theta = self.home_pos
                self.points[i] += 2 * step * cos(theta)
                self.points[i + 1] += 2 * step * sin(theta)
                if self.off_screen(self.points[i], self.points[i + 1]):
                    self.direction[j] = 90 + self.direction[j]

        self.draw_lines()

    @staticmethod
    def distance_between_points(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def off_screen(self, x, y):
        return x < -5 or x > self.width + 5 or y < -5 or y > self.height + 5
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
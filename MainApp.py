#!/usr/bin/python3

# Kivy related imports for the GUI
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, ColorProperty
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex

# from kivy.core.window import Window
# SCREEN_RES = [960, 540]    # Set your desired screen size here please
# Window.size = (SCREEN_RES[0],SCREEN_RES[1])

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

class LineRectangle(Widget):
    animated_color = ColorProperty([0.80,0.97,1.00, 0.5]) # the color property to be animated
    pulse_interval = 1 # the interval for pulsing
    stop_pulse = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(stop_pulse=self.blink_trigger)

    def blink_trigger(self, *args):
        if (not self.stop_pulse):
            Clock.schedule_once(self.start_pulsing,0)
        else:
            Animation.cancel_all(self)
            Animation(animated_color=[0.80,0.97,1.00, 0.5]).start(self)
       
    
    def start_pulsing(self,*args):
       d = self.pulse_interval /2
       anim = Animation(animated_color=[0.80,0.97,1.00, 0.5], duration=d) + \
              Animation(animated_color=[1.00,0.98,0.76, 0.6], duration=d)
       anim.repeat = True
       anim.start(self)


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

class MainScreen(MDScreen):
    '''
    Class for the first screen in the GUI
    '''
    def __init__(self, **kw):
        super().__init__(**kw)

class Experiment1(MDScreen):
    '''
    Class for the first experiment in the GUI
    '''
    def __init__(self, **kw):
        super().__init__(**kw)

class Experiment2(MDScreen):
    '''
    Class for the second experiment in the GUI
    '''
    def __init__(self, **kw):
        super().__init__(**kw)

class Experiment3(MDScreen):
    '''
    Class for the third experiment in the GUI
    '''
    def __init__(self, **kw):
        super().__init__(**kw)

class CopperExperiment(Widget):
    '''
    Class representing the copper extraction experiment through the 
    application of a direct heat source
    '''
    #* Colors are represented in the RGBA format in a list
    brown = [0, 0, 0, 0.9]
    blue = [0.12, 0.72, 0.60, 0.9]
    oxide_color = ListProperty(brown)   # Color of the material within the test tube
    flame_color = ListProperty(blue)    # color of the flame from the burner
    burner_on = BooleanProperty(False)  # Flag representing state of the burner (ON/OFF)
    start_animation = BooleanProperty(False)    # Flag to start or stop the color change animation

    smoke_opacity = NumericProperty(0)    # controls opacity of smoke effect
    smoke_offset = NumericProperty(0)   # controls how the smoke moves when heating
    
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
            Animation.cancel_all(self)
            Animation(oxide_color=self.blue, step = 1/10, duration=1).start(self)
            Animation(smoke_opacity=0, duration=0).start(self)
            smoke = Animation(smoke_offset=200, smoke_opacity=0.8, step = 1/60)
            smoke += Animation(smoke_offset=0, smoke_opacity=0, duration=0)
            # smoke &= Animation(smoke_opacity=1, duration=0)
            smoke.repeat = True
            smoke.start(self)
        else:
            # means burner is now OFF
            # start animation that changes color BACK to brown
            Animation.cancel_all(self)
            Animation(oxide_color=self.brown, step = 1/10).start(self)
            # Animation(smoke_opacity=0, step = 1/10).start(self)
            smoke = Animation(smoke_opacity=0, duration=0)
            smoke &= Animation(smoke_offset=0, duration=0)
            smoke.start(self)
    
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
            Animation(cu_ions_color=self.def_color, step = 1/30).start(self)
            Animation(mno_ions_color=self.def_color, step = 1/30).start(self)
    

class ChlorineExperiment(Widget):
    '''
    Class representing the extraction of Chlorine gas by dripping HCl into a flask containing Potassium Permanganate
    '''
    #* Colors are represented in the RGBA format in a list
    dropping_on = BooleanProperty(False)  # Flag representing state of the dripper (ON/OFF)
    animation_on = BooleanProperty(False)

    droplet_opacity = NumericProperty(0)    # controls opacity of droplet effect
    droplet_offset = NumericProperty(0)   # controls how the droplet moves when dripping

    smoke_opacity = NumericProperty(0)    # controls opacity of smoke effect
    smoke_offset = NumericProperty(0)   # controls how the smoke moves when reaction starts
    
    def __init__(self, **kwargs):
        '''
        Constructor of the widget class
        '''
        super().__init__(**kwargs)
        # Bind the start_animnation flag to a function 
        # so that the function gets called whenever 
        # the varibale changes.
        self.bind(dropping_on=self.anim_droplet)
        self.bind(animation_on=self.anim_reaction)
        
    def _change_flag_state(self, flag: bool, *args):
        '''
        Helper function to change the state of a boolean flag using kivy clock commands
        '''
        # Animation(droplet_opacity=0, droplet_offset=0, duration=0).start(self)
        if not flag:
            Animation(droplet_opacity=0, droplet_offset=0, duration=0).start(self)
        smoke = Animation(smoke_opacity=0, duration=0)
        smoke &= Animation(smoke_offset=0, duration=0)
        smoke.start(self)
        self.animation_on = flag

    def anim_droplet(self, *args):
        '''
        Creates an animation for droplets falling into the flask
        '''
        if self.dropping_on:
            # means that the dripper is now ON
            # start animation that drops a droplet to the flask
            Animation(droplet_opacity=0, duration=0).start(self)
            Animation(smoke_opacity=0, duration=0).start(self)
            drop = Animation(droplet_offset=-160, droplet_opacity=1, step = 1/60, duration=0.7)
            drop += Animation(droplet_offset=5, droplet_opacity=0, duration=0)
            # drop &= Animation(droplet_opacity=1, duration=0)
            drop.repeat = True
            drop.start(self)
            # Call the gas emitter function after 3 seconds have passed (3 drops essentially)
            Clock.schedule_once(lambda dt: self._change_flag_state(True), 3)
        else:
            Animation.cancel_all(self)
            self._change_flag_state(False)
    def anim_reaction(self, *args):
        '''
        Creates an animation for displaying the chemical reaction
        '''
        if self.animation_on:
            # means that the smoke is now ON
            # start animation that generates chlorine gas
            # Animation.cancel_all(self)
            Animation(smoke_opacity=0, duration=0).start(self)
            smoke = Animation(smoke_offset=300, smoke_opacity=0.8, step = 1/60)
            smoke += Animation(smoke_offset=0, smoke_opacity=0, duration=0)
            # smoke &= Animation(smoke_opacity=1, duration=0)
            smoke.repeat = True
            smoke.start(self)
    
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
        self.bind(move_to_pos=self.anime_particles)
        # print(f'1:{self.width}, {self.height}')
        # print(f'2:{self.pos}, {self.y}')

    def plot_points(self):
        '''
        Generates all the points in the background and starts a Clock event for updating their positions.
        '''
        self.points = []
        self.direction = []
        # print(f'1:{self.width}, {self.height}')
        # print(f'2:{self.x}, {self.y}')
        for _ in range(self.point_number):
            #! Issue with getting screen size if you have other 
            #! Fixed with putting the screenmanager in a floatlayout
            x = randint(self.x+35, self.width+self.x - 35)
            y = randint(self.y+35, self.height+self.y - 35)
            # x = randint(0, SCREEN_RES[0])
            # y = randint(0, SCREEN_RES[1])
            self.points.extend([x, y])
            self.direction.append(randint(0, 359))
        # print('THE PARTICLE EFFECT LIST IS:', self.points)
        self.move_event = Clock.schedule_interval(self.update_positions, 1/30)
    
    def anime_particles(self, *args):
        if self.move_to_pos:
            self.move_event.cancel()
            self.move_event = Clock.schedule_interval(self.update_positions2, 1/30)
        else:
            self.move_event.cancel()
            Clock.schedule_once(lambda dt: self.plot_points(), 0)
            # self.move_event = Clock.schedule_interval(self.update_positions, 1/30)
    
    def update_positions(self, *args):
        '''
        Updates the points in increaments, also checks if a point went out of bounds
        '''
        step = 0.6
        for i, j in zip(range(0, len(self.points), 2), range(len(self.direction))):
            theta = self.direction[j]
            self.points[i] += 3 * step * cos(theta)
            self.points[i + 1] += 3 * step * sin(theta)
            if self.off_screen(self.points[i], self.points[i + 1]):
                self.direction[j] = -90 + self.direction[j]

    def update_positions2(self, *args):
        step = 0.6
        for i, j in zip(range(0, len(self.points), 2), range(len(self.direction))):
            if not self.off_screen2(self.points[i], self.points[i + 1]):
                theta = self.home_pos
                # theta = self.direction[j] + 180
                self.points[i] += 5 * step * cos(theta)
                self.points[i + 1] += randint(-1, 0) * 0.5
                # self.direction[j] = 90 + self.direction[j]
            if self.off_screen2(self.points[i], self.points[i + 1]):
                self.direction[j] = 90 * cos(self.home_pos) + self.home_pos

    def off_screen(self, x, y):
        return x < self.x + 25 or x > self.width + self.x - 25 or y < self.y + 25 or y > self.height + self.y - 25

    def off_screen2(self, x, y):
        return x < self.x + 30 or x > self.width + self.x - 30 or y < self.y + 30 or y > self.height + self.y
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
        self.sm.add_widget(MainScreen())
        self.sm.add_widget(Experiment1())
        exp2 = Experiment2()
        Clock.schedule_once(lambda dt: exp2.ids.cu_ions.plot_points(), 0)
        Clock.schedule_once(lambda dt: exp2.ids.mno_ions.plot_points(), 0)
        self.sm.add_widget(exp2)
        self.sm.add_widget(Experiment3())

        self.main_screen = self.sm.get_screen('main')
        self.screen_dict["main"] = self.main_screen
        self.experiment1 = self.sm.get_screen('experiment1')
        self.screen_dict["experiment1"] = self.experiment1
        self.experiment2 = self.sm.get_screen('experiment2')
        self.screen_dict["experiment2"] = self.experiment2
        self.experiment3 = self.sm.get_screen('experiment3')
        self.screen_dict["experiment3"] = self.experiment3

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
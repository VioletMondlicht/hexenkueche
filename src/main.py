import json
import os

from kivy.core.text.text_layout import LayoutLine
from kivy.metrics import dp
from kivy.properties import StringProperty

from kivymd.uix.screen import MDScreen 
from kivymd.uix.screenmanager import MDScreenManager 
from kivymd.uix.button import MDButton, MDButtonIcon 
from kivymd.uix.textfield import MDTextField 
from kivy.uix.checkbox import CheckBox 
from kivymd.uix.boxlayout import MDBoxLayout 
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemLabel,
    MDNavigationItemIcon,
) 
from kivymd.app import MDApp
from kivy.uix.image import Image 

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView 
from kivy.uix.screenmanager import NoTransition
from kivy.core.window import Window
from kivy.animation import Animation 


# Savefile for the list
DATA_FILE_savedlist = "saved_eklist.json"

class EinkaufslisteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        main_layout = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
        )

        header_image = Image(
        source="HeaderNeu.png",
        allow_stretch=True ,  
        keep_ratio=True,   
        fit_mode="cover",  
        size_hint=(1, None),
        height=dp(150),
            )

        main_layout.add_widget(header_image)

        content_layout = FloatLayout(size_hint=(1, 1))

        self.content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            padding=[10, 10, 10, 10],
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.content_layout)

        content_layout.add_widget(scroll_view)

        plus_button = MDButton(
           MDButtonIcon(
                icon="plus",
            ),
            pos_hint={"center_x": 0.85, "center_y": 0.08},
            on_release=self.add_textfield_with_checkbox,
        )
        content_layout.add_widget(plus_button)

        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

        self.load_data()

    def add_textfield_with_checkbox(self, instance, text="", checked=False):
        
        item_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            spacing=2,
        )

        text_field = MDTextField(
            hint_text="Zutat eingeben",
            theme_bg_color="Custom",
            fill_color_normal=(0, 1, 0, .1),  # Schwarz
            fill_color_focus=(165, 42, 42, .2),  # blueviolet
            text_color_normal="blueviolet",
            text_color_focus="blueviolet",
            mode="filled",
            size_hint_x=0.8,
            size_hint_y=None,
            max_height="35dp",
            text=text,
        )
        item_layout.add_widget(text_field)

        checkbox = CheckBox(
            size_hint_x=0.2,
            active=checked,
        )
        item_layout.add_widget(checkbox)

        self.content_layout.add_widget(item_layout)

        text_field.bind(text=self.save_data)
        checkbox.bind(active=self.save_data)

    def save_data(self, *args):
        data = []
        for item in reversed(self.content_layout.children):
            text_field = item.children[1]
            checkbox = item.children[0]
            if text_field.text.strip():
                data.append({"text": text_field.text, "checked": checkbox.active})
        with open(DATA_FILE_savedlist, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(DATA_FILE_savedlist):
            with open(DATA_FILE_savedlist, 'r') as f:
                data = json.load(f)
            for entry in reversed(data):
                self.add_textfield_with_checkbox(
                    None, text=entry["text"], checked=entry["checked"]
                )


class RezepteScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
        )

        header_image = Image(
        source="HeaderNeu.png",
        allow_stretch=True,
        keep_ratio=True,
        fit_mode="cover",
        size_hint=(1, None),
        height=dp(150),
            )

        main_layout.add_widget(header_image)

        content_layout = FloatLayout(size_hint=(1, 1))

        self.content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            padding=[10, 10, 10, 10],
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.content_layout)

        content_layout.add_widget(scroll_view)

        main_layout.add_widget(content_layout)

        self.add_widget(main_layout)

    def add_textfield_with_checkbox(self, instance, text="", checked=False):
        item_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(35),
            spacing=2,
        )

        text_field = MDTextField(
            hint_text="Zutat eingeben",
            theme_bg_color="Custom",
            fill_color_normal=(0, 1, 0, .1),  # Schwarz
            fill_color_focus=(165, 42, 42, .2),  # blueviolet
            text_color_normal="blueviolet",
            text_color_focus="blueviolet",
            mode="filled",
            size_hint_x=0.8,
            size_hint_y=None,
            max_height="35dp",
            text=text,
        )
        item_layout.add_widget(text_field)

        checkbox = CheckBox(
            size_hint_x=0.2,
            active=checked,
        )
        item_layout.add_widget(checkbox)

        self.content_layout.add_widget(item_layout)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))


class Hexenkueche(MDApp):
    def build(self):
        self.icon = "HKIcon.png"

        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"

        self.screen_manager = MDScreenManager(id="screen_manager")

        self.screen_manager.add_widget(EinkaufslisteScreen(name="Einkaufsliste"))
        self.screen_manager.add_widget(RezepteScreen(name="Rezepte"))

        nav_bar = MDNavigationBar(
            BaseMDNavigationItem(
                icon="receipt-text",
                text="Einkaufsliste",
                active=True,
            ),
            BaseMDNavigationItem(
                icon="notebook",
                text="Rezepte",
            ),
            on_switch_tabs=self.on_switch_tabs,
        )

        main_layout = FloatLayout()

        background_image = Image(
            source="BackgroundDM.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )

        main_layout.add_widget(background_image)

        main_box = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
        )
        main_box.add_widget(self.screen_manager)
        main_box.add_widget(nav_bar)

        main_layout.add_widget(main_box)

        self.overlay_image2 = Image(
            source="CatScroll.png",
            size_hint=(0.15, 0.2),
            pos_hint={"x": 0.01, "y": 0.03},
            opacity=1
        )
        self.overlay_image3 = Image(
            source="CatBook.png",
            size_hint=(0.15, 0.2),
            pos_hint={"x": 0.01, "y": 0.03},
            opacity=0
        )

        main_layout.add_widget(self.overlay_image2)
        main_layout.add_widget(self.overlay_image3)

        return main_layout

    def on_switch_tabs(
        self,
        bar,
        item,
        item_icon: str,
        item_text: str,
    ):
        self.screen_manager.transition = NoTransition()
        self.screen_manager.current = item_text


        if item_text == "Einkaufsliste":
            self.animate_fade(self.overlay_image3, 0)
            self.animate_fade(self.overlay_image2, 1)
        elif item_text == "Rezepte":
            self.animate_fade(self.overlay_image2, 0)
            self.animate_fade(self.overlay_image3, 1)

    def animate_fade(self, widget, target_opacity):
        Animation(opacity=target_opacity, duration=0.5).start(widget)



Hexenkueche().run()

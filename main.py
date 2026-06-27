import random
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatIconButton
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Set modern mobile window size
Window.size = (400, 650)

KV = """
<MainLayout>:
    orientation: 'vertical'
    md_bg_color: self.theme_cls.bg_normal
    padding: dp(24)
    spacing: dp(24)

    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: dp(120)
        spacing: dp(8)
        
        # Center alignment layout for the top icon
        MDIcon:
            icon: "controller-classic"
            font_size: "36sp"
            halign: "center"
            theme_text_color: "Primary"

        MDLabel:
            text: "GUESS-O-MATIC"
            font_style: "H4"
            bold: True
            halign: 'center'
            theme_text_color: "Primary"

        MDLabel:
            text: "Pick a secret number between 1 and 100"
            font_style: "Body1"
            halign: 'center'
            theme_text_color: "Secondary"

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(32)
        adaptive_height: True
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

        MDTextField:
            id: guess_input
            mode: "rectangle"
            hint_text: "Enter your guess"
            helper_text: "Numbers only"
            helper_text_mode: "on_focus"
            input_filter: 'int'
            font_size: 32
            halign: 'center'
            size_hint_x: 0.8
            pos_hint: {"center_x": 0.5}
            on_text_validate: root.check_guess()

        # Swapped to an Icon Button component to natively support the icon
        MDFillRoundFlatIconButton:
            text: "SEND IT!"
            icon: "rocket-launch"
            size_hint_x: 0.8
            height: dp(52)
            pos_hint: {"center_x": 0.5}
            on_release: root.check_guess()

    MDBoxLayout:
        orientation: 'vertical'
        padding: [0, dp(20), 0, 0]

        MDLabel:
            id: feedback_label
            text: root.feedback_text
            font_style: "H6"
            halign: 'center'
            theme_text_color: "Custom"
            text_color: root.feedback_color
            bold: True

    MDWidget:
"""

class MainLayout(MDBoxLayout):
    feedback_text = StringProperty("READY PLAYER ONE...")
    feedback_color = ObjectProperty(get_color_from_hex("#6750A4")) 
    dialog = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.com = random.randint(1, 100)
        self.tries = 0

    def check_guess(self):
        input_widget = self.ids.guess_input
        val = input_widget.text
        
        if not val:
            input_widget.error = True
            self.flash_feedback("ENTER A NUMBER!", "#BA1A1A") 
            return
            
        try:
            hum = int(val)
        except ValueError:
            return

        self.tries += 1
        input_widget.text = ""
        input_widget.error = False

        if hum == self.com:
            self.show_win_dialog()
        elif hum > self.com:
            self.flash_feedback("TOO HIGH! GO LOWER!", "#0288D1") 
        else:
            self.flash_feedback("TOO LOW! GO HIGHER!", "#E65100") 

    def flash_feedback(self, text, color_hex):
        self.feedback_text = text
        self.feedback_color = get_color_from_hex(color_hex)
        
        label = self.ids.feedback_label
        anim = (Animation(font_size=24, duration=0.08) + 
                Animation(font_size=18, duration=0.08))
        anim.start(label)

    def show_win_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="VICTORY!",
                text=f"You smashed it in {self.tries} tries!",
                buttons=[
                    MDRaisedButton(
                        text="PLAY AGAIN",
                        on_release=self.reset_game
                    ),
                ],
            )
        else:
            self.dialog.text = f"You smashed it in {self.tries} tries!"
        self.dialog.open()

    def reset_game(self, *args):
        if self.dialog:
            self.dialog.dismiss()
        self.com = random.randint(1, 100)
        self.tries = 0
        self.feedback_text = "NEW GAME STARTED! GO!"
        self.feedback_color = get_color_from_hex("#388E3C") 

class FunkyGuessApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        Builder.load_string(KV)
        return MainLayout()

if __name__ == "__main__":
    FunkyGuessApp().run()
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class CheckOut(Popup):
    def __init__(self, **kwargs):
        super(CheckOut, self).__init__(**kwargs)
        self.title = 'Checkout'
        self.size_hint = (None, None)
        self.size = (min(Window.width * 0.8, 600),
                     min(Window.height * 0.8, 400))

        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text='Enter Card Details'))

        # Card Details Input
        card_number = TextInput(multiline=False, hint_text='Card Number')
        layout.add_widget(card_number)
        card_expiry = TextInput(multiline=False, hint_text='Card Expiry')
        layout.add_widget(card_expiry)
        cvv = TextInput(multiline=False, hint_text='CVV')
        layout.add_widget(cvv)

        # Purhcase 
        purchase_button = Button(text='Confirm Purchase')
        purchase_button.bind(on_press=lambda x: self.purchase(
            card_number.text, card_expiry.text, cvv.text))
        layout.add_widget(purchase_button)

        self.content = layout

    def purchase(self, card_number, card_expiry, cvv):
        # Check card details are entered
        if card_number.strip() == '' or not card_number.isdigit() or card_expiry.strip() == '' or cvv.strip() == ''or not cvv.isdigit():
            error_popup = Popup(title='Error', content=Label(
                text='Please provide valid card details.'), size_hint=(None, None), size=(600, 400))
            error_popup.open()
        else:
            self.dismiss()
            App.get_running_app().purchase(card_number, card_expiry, cvv)
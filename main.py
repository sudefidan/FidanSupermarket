from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class Product:
    def __init__(self, name, price, image_source):
        self.name = name
        self.price = price
        self.image_source = image_source

class CloseButton(Button):
    def __init__(self, **kwargs):
        super(CloseButton, self).__init__(**kwargs)
        self.text = "Close"
        self.background_color = (1, 0, 0, 1)  # Red background (RGBA format)

class SelectItemPopup(Popup):
    def __init__(self, catalog, **kwargs):
        super(SelectItemPopup, self).__init__(**kwargs)
        self.title = 'Select Item'
        self.size_hint = (None, None)
        self.size = (min(Window.width * 0.8, 1000), min(Window.height * 0.8, 600))
        self.auto_dismiss = False

        layout = BoxLayout(orientation='vertical', padding=10)

        for product in catalog:
            item_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=200, spacing=10)

            item_image = Image(
                source=product.image_source,
                size_hint=(None, None),
                size=(min(Window.width * 0.8, 200), min(Window.height * 0.8, 200)),
                allow_stretch=True,
                keep_ratio=True
            )

            item_label = Label(text='{} - £{}'.format(product.name, product.price))
            select_button = Button(text='Select')
            select_button.bind(on_press=lambda x: self.add_item_to_cart(product))

            item_layout.add_widget(item_image)
            item_layout.add_widget(item_label)
            item_layout.add_widget(select_button)

            layout.add_widget(item_layout)

        close_button = CloseButton(size_hint=(1, 0.1))
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)

        self.content = layout

    def add_item_to_cart(self, product):
        self.dismiss()
        App.get_running_app().add_item_to_cart(product)

class CheckoutPopup(Popup):
    def __init__(self, **kwargs):
        super(CheckoutPopup, self).__init__(**kwargs)
        self.title = 'Checkout'
        self.size_hint = (None, None)
        self.size = (min(Window.width * 0.8, 600), min(Window.height * 0.8, 400))

        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text='Enter Card Details'))

        card_number_input = TextInput(multiline=False, hint_text='Card Number')
        layout.add_widget(card_number_input)

        card_expiry_input = TextInput(multiline=False, hint_text='Card Expiry')
        layout.add_widget(card_expiry_input)

        cvv_input = TextInput(multiline=False, hint_text='CVV')
        layout.add_widget(cvv_input)

        confirm_button = Button(text='Confirm Purchase')
        confirm_button.bind(on_press=lambda x: self.process_purchase(card_number_input.text, card_expiry_input.text, cvv_input.text))
        layout.add_widget(confirm_button)

        self.content = layout

    def process_purchase(self, card_number, card_expiry, cvv):
        if card_number.strip() == '' or card_expiry.strip() == '' or cvv.strip() == '':
            error_popup = Popup(title='Error', content=Label(text='Please provide all card details.'), size_hint=(None, None), size=(600, 400))
            error_popup.open()
        else:
            self.dismiss()
            App.get_running_app().process_purchase(card_number, card_expiry, cvv)

class ShoppingApp(App):
    def build(self):
        Window.size = (800, 600)  # Set an initial window size

        layout = BoxLayout(orientation='vertical')

        title = Label(text='FIDAN ONLINE MARKET', size_hint=(1, 0.1), bold=True)
        layout.add_widget(title)

        content_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        layout.add_widget(content_layout)

        select_button = Button(text='Item List', size_hint=(0.2, 1), bold=True)
        select_button.bind(on_press=self.show_item_list)
        content_layout.add_widget(select_button)

        self.selected_items_box = ScrollView(size_hint=(0.8, 1))
        content_layout.add_widget(self.selected_items_box)

        purchase_button = Button(text='Purchase', size_hint=(1, 0.1), bold=True)
        purchase_button.bind(on_press=self.show_checkout_page)
        layout.add_widget(purchase_button)

        self.selected_items = []
        self.catalog = [
            Product('Bread', 1.99, 'images/bread.jpeg'),
            Product('Cheese', 4.99, 'images/bread.jpeg'),
            # Product('Lemon', 0.30, 'images/lemon.png'),
            # Product('Carrot', 2.50, 'images/carrot.png'),
            # Product('Onion', 0.90, 'images/onion.png'),
        ]

        self.checkout_popup = None

        return layout

    def show_item_list(self, instance):
        popup = SelectItemPopup(catalog=self.catalog)
        popup.open()

    def add_item_to_cart(self, product):
        self.selected_items.append(product)
        self.display_selected_items()

    def display_selected_items(self):
        self.selected_items_box.clear_widgets()

        total_price = 0.0

        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for item in self.selected_items:
            item_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100, spacing=10)

            item_image = Image(
                source=item.image_source,
                size_hint=(None, None),
                size=(100, 100),
                allow_stretch=True,
                keep_ratio=True
            )

            item_label = Label(text='{} - £{}'.format(item.name, item.price))
            item_layout.add_widget(item_image)
            item_layout.add_widget(item_label)

            total_price += item.price

            grid_layout.add_widget(item_layout)

        total_price_label = Label(text='Total Price: £{}'.format(total_price), size_hint=(1, None), height=30)
        grid_layout.add_widget(total_price_label)

        self.selected_items_box.add_widget(grid_layout)

    def show_checkout_page(self, instance):
        if len(self.selected_items) > 0:
            popup = CheckoutPopup()
            popup.open()
        else:
            popup = Popup(title='Purchase Error', content=Label(text='No items selected!'), size_hint=(None, None), size=(600, 300))
            popup.open()

    def process_purchase(self, card_number, card_expiry, cvv):
        self.selected_items = []
        self.display_selected_items()

        success_popup = Popup(title='Purchase Successful', content=Label(text='Thank you for your purchase!'), size_hint=(None, None), size=(600, 400))
        success_popup.open()

if __name__ == '__main__':
    ShoppingApp().run()

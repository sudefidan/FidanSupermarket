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

class ShoppingApp(App):
    def build(self):
        self.window_width, self.window_height = Window.size

        layout = BoxLayout(orientation='vertical')

        title = Label(text='FIDAN ONLINE MARKET', size_hint=(1, 0.1), bold=True)
        layout.add_widget(title)

        content_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        layout.add_widget(content_layout)

        select_button = Button(text='Item List', size_hint=(0.2, 1), bold=True)
        select_button.bind(on_press=self.select_item)
        content_layout.add_widget(select_button)

        self.selected_items_box = ScrollView(size_hint=(0.8, 1))
        content_layout.add_widget(self.selected_items_box)

        purchase_button = Button(text='Purchase', size_hint=(1, 0.1), bold=True)
        purchase_button.bind(on_press=self.show_checkout_page)
        layout.add_widget(purchase_button)

        self.selected_items = []
        self.catalog = [
            Product('Bread', 1.99, 'images/bread.jpeg'),
            Product('Cheese', 4.99, 'images/cheese.jpeg'),
            Product('Lemon', 0.30, 'images/lemon.png'),
            Product('Carrot', 2.50, 'images/carrot.png'),
            # Product('Onion', 0.90, 'images/onion.png'),
        ]

        self.checkout_popup = None
        self.checkout_page = None

        return layout

    def select_item(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_width = min(self.window_width * 0.8, 1000)
        popup_height = min(self.window_height * 0.8, 600)
        popup = Popup(title='Select Item', content=popup_layout, size_hint=(None, None), size=(popup_width, popup_height))

        for product in self.catalog:
            layout_height = min(self.window_height * 0.8, 200)
            item_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=layout_height, spacing=10)

            # Create the image widget
            image_width = min(self.window_width * 0.8, 200)
            image_height = min(self.window_height * 0.8, 200)
            item_image = Image(
                source=product.image_source,
                size_hint=(None, None),
                size=(image_width, image_height),
                allow_stretch=True,  # Allow the image to stretch to fit the widget
                keep_ratio=True  # Maintain the aspect ratio of the image
            )

            item_label = Label(text='{} - £{}'.format(product.name, product.price))
            select_button = Button(text='Select')
            select_button.bind(on_press=lambda x, product=product: self.add_item_to_cart(x, product, popup))

            item_layout.add_widget(item_image)
            item_layout.add_widget(item_label)
            item_layout.add_widget(select_button)

            popup_layout.add_widget(item_layout)

        # Create the close button
        close_button = CloseButton(size_hint=(1, 0.1))
        close_button.bind(on_press=popup.dismiss)
        popup_layout.add_widget(close_button)

        # Don't auto-dismiss the popup when the user clicks outside it
        popup.auto_dismiss = False

        popup.open()

    def add_item_to_cart(self, instance, product, popup):
        self.selected_items.append(product)
        self.display_selected_items()
        # Do not dismiss the popup after adding an item

    def display_selected_items(self):
        self.selected_items_box.clear_widgets()

        total_price = 0.0

        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for item in self.selected_items:
            item_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100, spacing=10)

            # Create the image widget for each item
            image_width = 100
            image_height = 100
            item_image = Image(
                source=item.image_source,
                size_hint=(None, None),
                size=(image_width, image_height),
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
            self.checkout_page = BoxLayout(orientation='vertical', padding=10)
            self.checkout_page.add_widget(Label(text='Enter Card Details'))

            card_number_input = TextInput(multiline=False, hint_text='Card Number')
            self.checkout_page.add_widget(card_number_input)

            card_expiry_input = TextInput(multiline=False, hint_text='Card Expiry')
            self.checkout_page.add_widget(card_expiry_input)

            cvv_input = TextInput(multiline=False, hint_text='CVV')
            self.checkout_page.add_widget(cvv_input)

            confirm_button = Button(text='Confirm Purchase')
            confirm_button.bind(on_press=lambda x: self.process_purchase(x, card_number_input.text, card_expiry_input.text, cvv_input.text))
            self.checkout_page.add_widget(confirm_button)

            popup_width = min(self.window_width * 0.8, 600)
            popup_height = min(self.window_height * 0.8, 400)

            self.checkout_popup = Popup(title='Checkout', content=self.checkout_page, size_hint=(None, None), size=(popup_width, popup_height))
            self.checkout_popup.open()
        else:
            popup = Popup(title='Purchase Error', content=Label(text='No items selected!'), size_hint=(None, None), size=(600, 300))
            popup.open()

    def process_purchase(self, instance, card_number, card_expiry, cvv):
        if card_number.strip() == '' or card_expiry.strip() == '' or cvv.strip() == '':
            error_popup = Popup(title='Error', content=Label(text='Please provide all card details.'), size_hint=(None, None), size=(600, 400))
            error_popup.open()
        else:
            self.checkout_popup.dismiss()

            receipt_content = self.generate_receipt()
            popup_width = min(self.window_width * 0.8, 1000)
            popup_height = min(self.window_height * 0.8, 600)
            receipt_popup = Popup(title='Receipt', content=Label(text=receipt_content), size_hint=(None, None), size=(popup_width, popup_height))
            receipt_popup.open()

            self.reset_app()

    def generate_receipt(self):
        receipt = 'Thank you for your purchase!\n\n'
        for item in self.selected_items:
            receipt += '{} - £{}\n'.format(item.name, item.price)
        total_price = sum(item.price for item in self.selected_items)
        receipt += '\nTotal Price: £{}'.format(total_price)
        return receipt

    def reset_app(self):
        self.selected_items = []
        self.selected_items_box.clear_widgets()
        self.checkout_popup = None
        self.checkout_page = None

class Product:
    def __init__(self, name, price, image_source):
        self.name = name
        self.price = price
        self.image_source = image_source

if __name__ == '__main__':
    ShoppingApp().run()

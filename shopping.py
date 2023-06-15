from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

# Product Class
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.quantity = 0

# Item List Class
class ItemListPopup(Popup):
    def __init__(self, catalog, **kwargs):
        super(ItemListPopup, self).__init__(**kwargs)
        self.title = 'Select Item'
        self.size_hint = (None, None)
        self.size = (min(Window.width * 0.8, 800),
                     min(Window.height * 0.8, 600))

        layout = BoxLayout(orientation='vertical', padding=10)

        # Product Details
        for product in catalog:
            item_layout = BoxLayout(orientation='vertical', padding=10)

            item_label = Label(
                text='{} - £{}'.format(product.name, product.price))
            item_layout.add_widget(item_label)

            select_button = Button(text='Select')
            select_button.bind(
                on_press=lambda _,product=product: self.add_item_to_cart(product))
            item_layout.add_widget(select_button)

            layout.add_widget(item_layout)

        self.content = layout

    def add_item_to_cart(self, product):
        self.dismiss()
        App.get_running_app().add_item_to_cart(product)
    


class CheckoutPopup(Popup):
    def __init__(self, **kwargs):
        super(CheckoutPopup, self).__init__(**kwargs)
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

class ShoppingApp(App):
    def build(self):
        Window.size = (700, 600)

        layout = BoxLayout(orientation='vertical')

        title = Label(text='FIDAN ONLINE MARKET',
                      size_hint=(1, 0.1),color = "red", bold=True)
        layout.add_widget(title)

        content_layout = BoxLayout(
            orientation='horizontal', size_hint=(1, 0.8))
        layout.add_widget(content_layout)

        select_button = Button(text='Item List', size_hint=(0.2, 1), bold=True)
        select_button.bind(on_press=self.show_item_list)
        content_layout.add_widget(select_button)

        self.shopping_basket = ScrollView(size_hint=(0.8, 1))
        content_layout.add_widget(self.shopping_basket)

        purchase_button = Button(
            text='Purchase', size_hint=(1, 0.1), bold=True)
        purchase_button.bind(on_press=self.show_checkout_page)
        layout.add_widget(purchase_button)

        self.basket_items = []
        self.catalog = [
            Product('Bread', 1.99, ),
            Product('Cheese', 4.99),
            Product('Lemon', 0.30),
            Product('Carrot', 2.50),
            Product('Onion', 0.90),
            Product('Garlic', 0.90),

        ]

        self.checkout_popup = None

        return layout

    def show_item_list(self, instance):
        popup = ItemListPopup(catalog=self.catalog)
        popup.open()

    def add_item_to_cart(self, product):
        for item in self.basket_items:
            if item.name == product.name:
                item.quantity += 1
                self.display_basket_items()
                return
        product.quantity = 1
        self.basket_items.append(product)
        self.display_basket_items()

    def display_basket_items(self):
        self.shopping_basket.clear_widgets()

        total_price = 0.0

        grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for item in self.basket_items:
            item_layout = BoxLayout(orientation='horizontal', size_hint=(
                1, None), height=100, spacing=10)

            item_label = Label(text='{} - £{} x{} '.format(item.name, item.price,item.quantity))
            item_layout.add_widget(item_label)

            total_price += item.price * item.quantity

            grid_layout.add_widget(item_layout)


        total_price_label = Label(text='Total Price: £{}'.format(
            total_price), size_hint=(1, None), height=30)
        grid_layout.add_widget(total_price_label)

        self.shopping_basket.add_widget(grid_layout)

    def show_checkout_page(self, instance):
        if len(self.basket_items) > 0:
            popup = CheckoutPopup()
            popup.open()
        else:
            popup = Popup(title='Purchase Error', content=Label(
                text='No items selected!'), size_hint=(None, None), size=(600, 300))
            popup.open()

    def purchase(self, card_number, card_expiry, cvv):
        self.basket_items = []
        self.display_basket_items()

        success_popup = Popup(title='Purchase Successful', content=Label(
            text='Thank you for your purchase!'), size_hint=(None, None), size=(600, 400))
        success_popup.open()


if __name__ == '__main__':
    ShoppingApp().run()

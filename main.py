from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from Entities.Product import Product
from PopUps.ItemListPopup import ItemList
from PopUps.CheckOutPopup import CheckOut

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
        popup = ItemList(catalog=self.catalog)
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
    
    def remove_item_from_cart(self, product):
        # Find the item in the cart
        for item in self.basket_items:
            if item.name == product.name:
                # Decrease the quantity
                item.quantity -= 1
                if item.quantity == 0:
                    # Remove the item from the cart if the quantity becomes zero
                    self.basket_items.remove(item)
                break

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

            remove_button = Button(text='Remove')
            remove_button.bind(
                on_press=lambda _, product=item: self.remove_item_from_cart(product))
            item_layout.add_widget(remove_button)

            grid_layout.add_widget(item_layout)


        total_price_label = Label(text='Total Price: £{}'.format(
            total_price), size_hint=(1, None), height=30)
        grid_layout.add_widget(total_price_label)

        self.shopping_basket.add_widget(grid_layout)

    def show_checkout_page(self, instance):
        if len(self.basket_items) > 0:
            popup = CheckOut()
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

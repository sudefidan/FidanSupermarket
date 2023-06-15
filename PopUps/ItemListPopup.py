from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# Item List Class
class ItemList(Popup):
    def __init__(self, catalog, **kwargs):
        super(ItemList, self).__init__(**kwargs)
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
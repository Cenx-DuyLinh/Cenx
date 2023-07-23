from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.metrics import dp
class MainWidget(Widget):
    pass
class StackLayoutExample(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(0,10):
            b=Button(text=str(i+1),size_hint=(None,None),size=(dp(100)+20,dp(100)))
            self.add_widget(b)
class GridLayoutExample(GridLayout):
    pass
class BoxLayoutExample(BoxLayout):
    pass
    '''def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        b1 = Button(text='TestBoxLayout')
        b2 = Button(text='TestBoxLayout2')
        b3 = Button(text='TestBoxLayout3')
        self.add_widget(b1)
        self.add_widget(b2)
        self.add_widget(b3)'''

class TheLabApp(App):
    pass

TheLabApp().run()
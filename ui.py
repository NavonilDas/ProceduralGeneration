from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import PIL
import uuid

from grass_2d import create_2d_grass_tileset

class GrassDisplayApp(BoxLayout):
    def __init__(self, **kwargs):
        super(GrassDisplayApp, self).__init__(**kwargs)
        
        self.generate_btn = Button(text="Generate new Image", height=50)
        self.add_widget(self.generate_btn)
        self.generate_btn.bind(on_press=self.on_image_generate)

        self.save_btn = Button(text="Save Image", height=50)
        self.add_widget(self.save_btn)
        self.save_btn.bind(on_press=self.on_image_save)

        
        self.img1=Image(size=(200,200))
        self.img = create_2d_grass_tileset()
        self.add_widget(self.img1)
        Clock.schedule_interval(self.update, 1.0/33.0)

    def on_image_generate(self, _):
        self.img = create_2d_grass_tileset()

    def on_image_save(self, _):
        pil_img = PIL.Image.fromarray(self.img, mode='RGBA')
        pil_img.save(str(uuid.uuid4()) + ".png")


    def update(self, *args):
        buf = self.img.tobytes()
        texture = Texture.create(size=self.img.shape[:2], colorfmt="rgba")
        texture.blit_buffer(buf, colorfmt="rgba", bufferfmt="ubyte")
        self.img1.texture = texture

class MainApp(App):
   def build(self):
         return GrassDisplayApp()

if __name__ == "__main__":
   MainApp().run()
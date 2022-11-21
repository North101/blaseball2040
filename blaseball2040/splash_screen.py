import badger2040
from badger_ui import App, Offset, Size, Widget
from badger_ui.util import Image

import blaseball2040
from blaseball2040.select_screen import SelectScreen


class SplashScreen(Widget):
  def __init__(self) -> None:
    self.logo = Image(f'{blaseball2040.root_dir}/assets/logo.bin', 296, 128)
    self.logo.load()

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_B]:
      app.child = SelectScreen()
      return True

    return super().on_button(app, pressed)

  def render(self, app: 'App', size: Size, offset: Offset):
    app.display.invert(False)
    self.logo.draw(app.display, offset=offset)

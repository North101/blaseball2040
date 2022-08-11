import badger2040
from badger_ui import App
from blaseball2040.splash_screen import SplashScreen


class MyApp(App):
  def __init__(self):
    super().__init__()

    self.child = SplashScreen()

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_USER]:
      app.child = SplashScreen()
      return True

    return super().on_button(app, pressed)

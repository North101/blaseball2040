import badger2040
from badger_ui import App, Offset, Size, Widget
from badger_ui.align import Center
from badger_ui.column import Column
from badger_ui.sized import SizedBox
from badger_ui.stack import Stack
from badger_ui.text import TextWidget

from blaseball2040.stat_screen import Game
from blaseball2040.team_score import TeamScore


class ScoreScreen(Widget):
  def __init__(self, game: Game):
    self.game = game

    self.child: Widget | None = None

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    from blaseball2040.splash_screen import SplashScreen
    if pressed[badger2040.BUTTON_B]:
      app.child = SplashScreen()
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    if self.child:
      return
    self.child = Stack(children=[
        SizedBox(
            child=Center(child=TextWidget(
                text='GAME OVER',
                line_height=30,
                thickness=2,
            )),
            size=Size(size.width, 30),
        ),
        Center(child=Column(children=[
            TeamScore(
                self.game.team1,
                self.game.score1,
                self.game.score1 > self.game.score2,
            ),
            TeamScore(
                self.game.team2,
                self.game.score2,
                self.game.score2 > self.game.score1,
            ),
        ])),
    ])

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)

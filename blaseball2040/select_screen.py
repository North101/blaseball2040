import badger2040
from badger_ui import App, Offset, Size, Widget
from badger_ui.align import Center
from badger_ui.column import Column
from badger_ui.image import ImageWidget
from badger_ui.positioned import Positioned
from badger_ui.sized import SizedBox
from badger_ui.stack import Stack
from badger_ui.text import TextWidget
from badger_ui.util import Image

import blaseball2040
from blaseball2040.stat_screen import Game, StatScreen

teams = [
    'THE CANIS UNDERDOGS',
    'THE AURIC ALLSTARS',
]


class SelectScreen(Widget):
  def __init__(self) -> None:
    self.vs_image = Image(f'{blaseball2040.assets_dir}/vs.bin', 296, 128)
    self.vs_image.load()

    self.player_index = 0
    self.player_team_index = [
        0,
        1,
    ]

    self.team1: Column | None = None
    self.team2: Column | None = None
    self.child: Widget | None = None

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_A]:
      self.player_index = (self.player_index - 1) % 2
      return True

    elif pressed[badger2040.BUTTON_B]:
      app.display.invert(False)
      app.child = StatScreen(
          game=Game(
              team1=teams[self.player_team_index[0]],
              team2=teams[self.player_team_index[1]],
          ),
      )
      return True

    elif pressed[badger2040.BUTTON_C]:
      self.player_index = (self.player_index + 1) % 2
      return True

    elif pressed[badger2040.BUTTON_UP]:
      self.player_team_index[self.player_index] = (self.player_team_index[self.player_index] + 1) % len(teams)
      return True

    elif pressed[badger2040.BUTTON_DOWN]:
      self.player_team_index[self.player_index] = (self.player_team_index[self.player_index] - 1) % len(teams)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    team1 = [
        TextWidget(
            text=line,
            line_height=15,
            thickness=2,
            color=15,
            scale=0.5,
        )
        for line in teams[self.player_team_index[0]].split(' ')
    ]
    if self.team1:
      self.team1.children = team1
    else:
      self.team1 = Column(children=team1)

    team2 = [
        TextWidget(
            text=line,
            line_height=15,
            thickness=2,
            color=0,
            scale=0.5,
        )
        for line in teams[self.player_team_index[1]].split(' ')
    ]
    if self.team2:
      self.team2.children = team2
    else:
      self.team2 = Column(children=team2)

    if self.child:
      return
    self.child = Stack(children=[
        ImageWidget(self.vs_image),
        SizedBox(
            child=Center(child=self.team1),
            size=Size(size.width // 2, size.height),
        ),
        SizedBox(
            child=Positioned(
                child=Center(child=self.team2),
                offset=Offset(size.width // 2, 0),
            ),
            size=Size(size.width // 2, size.height),
        )
    ])

  def render(self, app: 'App', size: Size, offset: Offset):
    app.display.invert(self.player_index == 1)

    self.build(app, size, offset)
    self.child.render(app, size, offset)

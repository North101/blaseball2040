import badger2040
from badger_ui import App, Offset, Size, Widget
from badger_ui.align import Center
from badger_ui.column import Column
from badger_ui.icon import IconWidget
from badger_ui.positioned import Positioned
from badger_ui.row import Row
from badger_ui.sized import SizedBox
from badger_ui.stack import Stack
from badger_ui.text import TextWidget
from badger_ui.util import IconSheet

import blaseball2040
from blaseball2040.team_score import TeamScore


class Inning:
  TOP = 0
  BOTTOM = 1
  OVER = 2


class Selection:
  BALLS = 0
  STRIKES = 1
  OUTS = 2


class Game:
  def __init__(
      self,
      team1: str,
      team2: str,
      inning: int = Inning.TOP,
      score1: int = 0,
      score2: int = 0,
      outs: int = 0,
      strikes: int = 0,
      balls: int = 0,
  ):
    self.team1 = team1
    self.team2 = team2
    self.inning = inning
    self.score1 = score1
    self.score2 = score2
    self.outs = outs
    self.strikes = strikes
    self.balls = balls


class StatScreen(Widget):
  stat_offsets = [
      Offset(badger2040.WIDTH // 4 * 1, 96) - Offset(32, 16),
      Offset(badger2040.WIDTH // 4 * 2, 96) - Offset(32, 16),
      Offset(badger2040.WIDTH // 4 * 3, 96) - Offset(32, 16),
  ]

  def __init__(self, game: Game):
    self.icons = IconSheet(f'{blaseball2040.assets_dir}/stats.bin', 32, 3)
    self.icons.load()

    self.game = game
    self.selected_index = 0

    self.team1: TeamScore | None = None
    self.team2: TeamScore | None = None
    self.balls: StatWidget | None = None
    self.strikes: StatWidget | None = None
    self.outs: StatWidget | None = None
    self.child: Widget | None = None

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    from blaseball2040.pitch_screen import (BallScreen, OutScreen, PitchScreen,
                                            StrikeScreen)

    if pressed[badger2040.BUTTON_A]:
      self.selected_index = (self.selected_index - 1) % 3
      return True

    elif pressed[badger2040.BUTTON_B]:
      app.child = PitchScreen(self.game)
      return True

    elif pressed[badger2040.BUTTON_C]:
      self.selected_index = (self.selected_index + 1) % 3
      return True

    elif pressed[badger2040.BUTTON_UP]:
      if self.selected_index == Selection.OUTS:
        self.game.outs += 1
        if self.game.outs >= 3:
          app.child = OutScreen(self.game)
      elif self.selected_index == Selection.STRIKES:
        self.game.strikes += 1
        if self.game.strikes >= 3:
          app.child = StrikeScreen(self.game)
      elif self.selected_index == Selection.BALLS:
        self.game.balls += 1
        if self.game.balls >= 4:
          app.child = BallScreen(self.game)
      return True

    elif pressed[badger2040.BUTTON_DOWN]:
      if self.selected_index == Selection.OUTS:
        self.game.outs = max(self.game.outs - 1, 0)
      elif self.selected_index == Selection.STRIKES:
        self.game.strikes = max(self.game.strikes - 1, 0)
      elif self.selected_index == Selection.BALLS:
        self.game.balls = max(self.game.balls - 1, 0)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    if self.team1:
      self.team1.score = self.game.score1
      self.team1.selected = self.game.inning == Inning.TOP
    else:
      self.team1 = TeamScore(
          name=self.game.team1,
          score=self.game.score1,
          selected=self.game.inning == Inning.TOP,
      )

    if self.team2:
      self.team2.score = self.game.score2
      self.team2.selected = self.game.inning == Inning.BOTTOM
    else:
      self.team2 = TeamScore(
          name=self.game.team2,
          score=self.game.score2,
          selected=self.game.inning == Inning.BOTTOM,
      )

    if self.balls:
      self.balls.value = self.game.balls
      self.balls.selected = self.selected_index == Selection.BALLS
    else:
      self.balls = StatWidget(
          icons=self.icons,
          index=0,
          value=self.game.balls,
          selected=self.selected_index == Selection.BALLS,
      )

    if self.strikes:
      self.strikes.value = self.game.strikes
      self.strikes.selected = self.selected_index == Selection.STRIKES
    else:
      self.strikes = StatWidget(
          icons=self.icons,
          index=1,
          value=self.game.strikes,
          selected=self.selected_index == Selection.STRIKES,
      )

    if self.outs:
      self.outs.value = self.game.outs
      self.outs.selected = self.selected_index == Selection.OUTS
    else:
      self.outs = StatWidget(
          icons=self.icons,
          index=2,
          value=self.game.outs,
          selected=self.selected_index == Selection.OUTS,
      )

    if self.child:
      return
    self.child = Stack(children=[
        Column(children=[
            self.team1,
            self.team2,
        ]),
        Positioned(
            child=self.balls,
            offset=Offset(size.width // 4 * 1, 96) - Offset(32, 16),
        ),
        Positioned(
            child=self.strikes,
            offset=Offset(size.width // 4 * 2, 96) - Offset(32, 16),
        ),
        Positioned(
            child=self.outs,
            offset=Offset(size.width // 4 * 3, 96) - Offset(32, 16),
        ),
    ])

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)


class StatWidget(Widget):
  def __init__(self, icons: IconSheet, index: int, value: int, selected: bool):
    self.icons = icons
    self.index = index
    self.value = value
    self.selected = selected

    self.value_text: TextWidget | None = None
    self.child: Widget | None = None

  def measure(self, app: 'App', size: Size) -> Size:
    return Size(self.icons.size + 32, 32)

  def build(self, app: App, size: Size, offset: Offset):
    value = f'{self.value}'
    if self.value_text:
      self.value_text.text = value
    else:
      self.value_text = TextWidget(
          text=value,
          line_height=30,
          thickness=2,
      )

    if self.child:
      return
    self.child = SizedBox(
        child=Center(child=Row(children=[
            IconWidget(
                icons=self.icons,
                icon_index=self.index,
            ),
            self.value_text,
        ])),
        size=self.measure(app, size),
    )

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)
    if self.selected:
      height = offset.y + 32
      app.display.line(
          offset.x,
          height,
          offset.x + self.icons.size + 32,
          height,
      )

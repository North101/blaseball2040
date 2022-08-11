import badger2040
from badger_ui import App, Offset, Size, Widget
from badger_ui.align import Center
from badger_ui.column import Column
from badger_ui.positioned import Positioned
from badger_ui.row import Row
from badger_ui.sized import SizedBox
from badger_ui.stack import Stack
from badger_ui.text import TextWidget

from blaseball2040.score_screen import ScoreScreen
from blaseball2040.stat_screen import Game, Inning, StatScreen


class PitchScreen(Widget):
  def __init__(self, game: Game) -> None:
    self.game = game
    self.pitch = 10

    self.pitch_text: TextWidget | None = None
    self.child: Widget | None = None

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_UP]:
      self.pitch += 1
      return True

    elif pressed[badger2040.BUTTON_DOWN]:
      self.pitch = max(self.pitch - 1, 0)
      return True

    elif pressed[badger2040.BUTTON_B]:
      app.child = BatScreen(self.game, self.pitch)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    pitch = f'{self.pitch}'
    if self.pitch_text:
      self.pitch_text.text = pitch
    else:
      self.pitch_text = TextWidget(
          text=pitch,
          line_height=60,
          thickness=2,
          scale=2,
      )

    if self.child:
      return
    self.child = Stack(children=[
        SizedBox(
            child=Center(child=TextWidget(
                text='PITCH',
                line_height=30,
                thickness=2,
            )),
            size=Size(size.width, 30),
        ),
        Center(child=self.pitch_text),
    ])

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)


class BatScreen(Widget):
  def __init__(self, game: Game, pitch: int) -> None:
    self.game = game
    self.pitch = pitch
    self.bat = 10

    self.bat_text: TextWidget | None = None
    self.subtitle: TextWidget | None = None
    self.child: Widget | None = None

  @property
  def base(self):
    return self.bat - self.pitch

  @property
  def strike(self):
    return self.base < 0

  @property
  def ball(self):
    return self.base == 0

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_UP]:
      self.bat += 1
      return True

    elif pressed[badger2040.BUTTON_DOWN]:
      self.bat = max(self.bat - 1, 0)
      return True

    elif pressed[badger2040.BUTTON_B]:
      if self.ball:
        self.game.balls += 1
        app.child = BallScreen(self.game)
      elif self.strike:
        self.game.strikes += 1
        app.child = StrikeScreen(self.game)
      else:
        app.child = AskCatchScreen(self.game, self.pitch, self.bat)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    if self.bat_text:
      self.bat_text.text = f'{self.bat}'
    else:
      self.bat_text = TextWidget(
          text=f'{self.bat}',
          line_height=60,
          thickness=2,
          scale=2,
      )

    if self.strike:
      subtitle = 'Strike!'
    elif self.ball:
      subtitle = 'Ball!'
    elif self.base >= 4:
      subtitle = 'Homerun!'
    else:
      subtitle = f'Base {self.base}'

    if self.subtitle:
      self.subtitle.text = subtitle
    else:
      self.subtitle = TextWidget(
          text=subtitle,
          line_height=30,
          thickness=2,
      )

    if self.child:
      return
    self.child = Stack(children=[
        SizedBox(
            child=Center(child=TextWidget(
                text='BAT',
                line_height=30,
                thickness=2,
            )),
            size=Size(size.width, 30),
        ),
        Positioned(
            child=Center(child=TextWidget(
                text=f'{self.pitch}',
                line_height=60,
                thickness=2,
                scale=2,
            )),
            offset=Offset(-(size.width // 4), 0),
        ),
        Center(child=TextWidget(
            text='VS',
            line_height=30,
            thickness=2,
        )),
        Positioned(
            child=Center(child=self.bat_text),
            offset=Offset(size.width // 4, 0),
        ),
        SizedBox(
            child=Positioned(
                child=Center(child=self.subtitle),
                offset=Offset(0, size.height - 30),
            ),
            size=Size(size.width, 30),
        ),
    ])

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)


class AskCatchScreen(Widget):
  def __init__(self, game: Game, pitch: int, bat: int) -> None:
    self.game = game
    self.pitch = pitch
    self.bat = bat
    self.catch = True

    self.yes_text: TextWidget | None = None
    self.no_text: TextWidget | None = None
    self.child: Widget | None = None

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_A]:
      self.catch = not self.catch
      return True

    elif pressed[badger2040.BUTTON_B]:
      if self.catch:
        app.child = CatchScreen(self.game, self.pitch, self.bat + 1)
      else:
        app.child = RunsScreen(self.game)
      return True

    elif pressed[badger2040.BUTTON_C]:
      self.catch = not self.catch
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    if self.yes_text:
      self.yes_text.underline = self.catch
    else:
      self.yes_text = TextWidget(
          text='Yes',
          line_height=60,
          thickness=2,
          scale=2,
          underline=self.catch,
      )

    if self.no_text:
      self.no_text.underline = not self.catch
    else:
      self.no_text = TextWidget(
          text='No',
          line_height=60,
          thickness=2,
          scale=2,
          underline=not self.catch,
      )

    if self.child:
      return
    self.child = Stack(children=[
        SizedBox(
            child=Center(child=TextWidget(
                text='CATCH?',
                line_height=30,
                thickness=2,
            )),
            size=Size(size.width, 30),
        ),
        Center(child=Row(children=[
            SizedBox(
                child=Center(child=self.yes_text),
                size=Size(size.width // 2, 60),
            ),
            SizedBox(
                child=Center(child=self.no_text),
                size=Size(size.width // 2, 60),
            ),
        ]))
    ])

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)


class CatchScreen(Widget):
  def __init__(self, game: Game, pitch: int, bat: int) -> None:
    self.game = game
    self.pitch = pitch
    self.bat = bat
    self.catch = 10

    self.catch_text: TextWidget | None = None
    self.subtitle: TextWidget | None = None
    self.child: Widget | None = None

  @property
  def base(self):
    return self.bat - self.pitch

  @property
  def out(self):
    return self.bat - self.catch < 0

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_UP]:
      self.catch += 1
      return True

    elif pressed[badger2040.BUTTON_DOWN]:
      self.catch = max(self.catch - 1, 0)
      return True

    elif pressed[badger2040.BUTTON_B]:
      if self.out:
        self.game.outs += 1
        self.game.balls = 0
        app.child = OutScreen(self.game)
      else:
        app.child = RunsScreen(self.game)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    catch = f'{self.catch}'
    if self.catch_text:
      self.catch_text.text = catch
    else:
      self.catch_text = TextWidget(
          text=catch,
          line_height=60,
          thickness=2,
          scale=2,
      )

    if self.out:
      subtitle = 'Out!'
    elif self.base >= 4:
      subtitle = 'Homerun!'
    else:
      subtitle = f'Base {self.base}'

    if self.subtitle:
      self.subtitle.text = subtitle
    else:
      self.subtitle = TextWidget(
          text=subtitle,
          line_height=30,
          thickness=2,
      )

    if self.child:
      return
    self.child = Stack(children=[
        SizedBox(
            child=Center(child=TextWidget(
                text='CATCH',
                line_height=30,
                thickness=2,
            )),
            size=Size(size.width, 30),
        ),
        Positioned(
            child=Center(child=TextWidget(
                text=f'{self.bat}',
                line_height=60,
                thickness=2,
                scale=2,
            )),
            offset=Offset(-(size.width // 4), 0),
        ),
        Center(child=TextWidget(
            text='VS',
            line_height=30,
            thickness=2,
        )),
        Positioned(
            child=Center(child=TextWidget(
                text=f'{self.bat}',
                line_height=60,
                thickness=2,
                scale=2,
            )),
            offset=Offset(size.width // 4, 0),
        ),
        SizedBox(
            child=Positioned(
                child=Center(child=self.subtitle),
                offset=Offset(0, size.height - 30),
            ),
            size=Size(size.width, 30),
        ),
    ])

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)


class BallScreen(Widget):
  def __init__(self, game: Game) -> None:
    self.game = game
    self.child: Widget | None = None

  @property
  def walk(self):
    return self.game.balls >= 4

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_B]:
      self.game.balls %= 4
      if self.walk:
        app.child = RunsScreen(self.game)
      else:
        app.child = StatScreen(self.game)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    if self.child:
      return

    if self.walk:
      self.child = Center(child=Column(children=[
          TextWidget(
              text='Walk!',
              line_height=60,
              thickness=2,
              scale=2,
          ),
          TextWidget(
              text='4 Balls',
              line_height=30,
              thickness=2,
          ),
      ]))
    else:
      self.child = Center(child=TextWidget(
          text=f'Ball {self.game.balls}!',
          line_height=60,
          thickness=2,
          scale=2,
      ))

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)


class StrikeScreen(Widget):
  def __init__(self, game: Game) -> None:
    self.game = game
    self.child: Widget | None = None

  @property
  def switch(self):
    return self.game.outs >= 3

  @property
  def out(self):
    return self.game.strikes >= 3

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_B]:
      if self.switch:
        app.child = OutScreen(self.game)
      elif self.out:
        self.game.outs += 1
        self.game.strikes = 0
        app.child = StatScreen(self.game)
      else:
        app.child = StatScreen(self.game)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    if self.child:
      return

    if self.out:
      self.child = Center(child=Column(children=[
          TextWidget(
              text='Out!',
              line_height=60,
              thickness=2,
              scale=2,
          ),
          TextWidget(
              text='3 Strikes',
              line_height=30,
              thickness=2,
          ),
      ]))
    else:
      self.child = Center(child=TextWidget(
          text=f'Strike {self.game.strikes}!',
          line_height=60,
          thickness=2,
          scale=2,
      ))

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)


class OutScreen(Widget):
  def __init__(self, game: Game) -> None:
    self.game = game
    self.child: Widget | None = None

  @property
  def switch(self):
    return self.game.outs >= 3

  @property
  def over(self):
    return self.switch and self.game.inning == Inning.BOTTOM

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_B]:
      if self.over:
        self.game.inning += 1
        self.game.outs = 0
        self.game.strikes = 0
        self.game.balls = 0
        app.child = ScoreScreen(self.game)
      elif self.switch:
        self.game.inning += 1
        self.game.outs = 0
        self.game.strikes = 0
        self.game.balls = 0
        app.child = StatScreen(self.game)
      else:
        app.child = StatScreen(self.game)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    if self.child:
      return

    if self.over:
      self.child = Center(child=Column(children=[
          TextWidget(
              text='Game Over!',
              line_height=45,
              thickness=2,
              scale=1.5,
          ),
          TextWidget(
              text='3 Outs',
              line_height=30,
              thickness=2,
          ),
      ]))
    elif self.switch:
      self.child = Center(child=Column(children=[
          TextWidget(
              text='Switch!',
              line_height=60,
              thickness=2,
              scale=2,
          ),
          TextWidget(
              text='3 Outs',
              line_height=30,
              thickness=2,
          ),
      ]))
    else:
      self.child = Center(child=TextWidget(
          text=f'Out {self.game.outs}!',
          line_height=60,
          thickness=2,
          scale=2,
      ))

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)


class RunsScreen(Widget):
  def __init__(self, game: Game) -> None:
    self.game = game
    self.runs = 0
    self.child: Widget | None = None
    self.runs_text: TextWidget | None = None

  def on_button(self, app: 'App', pressed: dict[int, bool]) -> bool:
    if pressed[badger2040.BUTTON_B]:
      if self.game.inning == Inning.TOP:
        self.game.score1 += self.runs
      elif self.game.inning == Inning.BOTTOM:
        self.game.score2 += self.runs
      self.game.strikes = 0
      self.game.balls = 0
      app.child = StatScreen(self.game)
      return True

    elif pressed[badger2040.BUTTON_UP]:
      self.runs += 1
      return True

    elif pressed[badger2040.BUTTON_DOWN]:
      self.runs = max(self.runs - 1, 0)
      return True

    return super().on_button(app, pressed)

  def build(self, app: 'App', size: Size, offset: Offset):
    if self.runs_text:
      self.runs_text.text = f'{self.runs}'
    else:
      self.runs_text = TextWidget(
          text=f'{self.runs}',
          line_height=60,
          thickness=2,
          scale=2,
      )

    if self.child:
      return

    self.child = Stack(children=[
        SizedBox(
            child=Center(child=TextWidget(
                text='RUNS',
                line_height=30,
                thickness=2,
            )),
            size=Size(size.width, 30),
        ),
        Center(child=self.runs_text),
    ])

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)
    self.child.render(app, size, offset)

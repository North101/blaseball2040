from badger_ui import App, Offset, Size, Widget
from badger_ui.align import Left, Right
from badger_ui.padding import EdgeOffsets, Padding
from badger_ui.sized import SizedBox
from badger_ui.stack import Stack
from badger_ui.text import TextWidget


class TeamScore(Widget):
  def __init__(self, name: str, score: int, selected: bool):
    self.name = name
    self.score = score
    self.selected = selected

    self.name_text: TextWidget | None = None
    self.score_text: TextWidget | None = None
    self.child: Widget | None = None

  def measure(self, app: 'App', size: Size) -> Size:
    return Size(size.width, 25)

  def build(self, app: 'App', size: Size, offset: Offset):
    color = 15 if self.selected else 0
    if self.name_text:
      self.name_text.text = self.name
      self.name_text.color = color
    else:
      self.name_text = TextWidget(
          text=self.name,
          line_height=21,
          scale=0.7,
          thickness=2,
          color=color,
      )

    if self.score_text:
      self.score_text.text = f'{self.score}'
      self.score_text.color = color
    else:
      self.score_text = TextWidget(
          text=f'{self.score}',
          line_height=21,
          scale=0.7,
          thickness=2,
          color=color,
      )

    if self.child:
      return
    self.child = SizedBox(
        child=Stack(children=[
            Left(child=Padding(
                child=self.name_text,
                padding=EdgeOffsets.all(2),
            )),
            Right(child=Padding(
                child=self.score_text,
                padding=EdgeOffsets.all(2),
            )),
        ]),
        size=self.measure(app, size),
    )

  def render(self, app: 'App', size: Size, offset: Offset):
    self.build(app, size, offset)

    if self.selected:
      app.display.pen(0)
      app.display.rectangle(
          offset.x,
          offset.y,
          size.width,
          size.height,
      )
    self.child.render(app, size, offset)

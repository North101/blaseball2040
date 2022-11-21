from blaseball2040.app import MyApp

root_dir = '/'.join(__file__.rsplit('/')[:-1])

def start():
  app = MyApp()
  while True:
    app.update()

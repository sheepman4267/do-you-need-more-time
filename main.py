import subprocess

# An extremely simple and configurable "do you need more time?" dialog
import pyglet
from pyglet import clock
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Simple "Do you need more time?" dialog for integration into a kiosk system.')
parser.add_argument('--time', type=int, help='Integer number of seconds before timeout', default=30)
parser.add_argument('--timeout_command', type=str, help='Command to be executed on timeout')
parser.add_argument('--message', type=str, help='Message to be displayed', default='Do you need more time?')

args = parser.parse_args()

def main():
    if is_idle(args.timeout_command):
        clock.schedule_interval(countdown, 1)
        pyglet.app.run()
    else:
        print('Kiosk is not idle. Exiting.')

window = pyglet.window.Window()
announcement_label = pyglet.text.Label(
                          text=args.message,
                          font_name='Arial',
                          font_size=36,
                          x=window.width//2, y=window.height//1.2,
                          anchor_x='center', anchor_y='center',
                          )
countdown_label = pyglet.text.Label(str(args.time),
                                    font_name='Arial',
                                    font_size=30,
                                    x=window.width//2, y=window.height//2.7,
                                    anchor_x='center', anchor_y='center',
                                    )

def countdown(dt):
    if int(countdown_label.text) <= 0:
        subprocess.run(args.timeout_command.split())
        exit(0)
    countdown_label.text = str(int(countdown_label.text) - 1)

@window.event
def on_draw():
    window.clear()
    announcement_label.draw()
    countdown_label.draw()

def is_idle(timeout:int):
    idletime = int(subprocess.check_output('xprintidle')) / 1000 #Get idle time from xprintidle, convert it to seconds
    if idletime <= timeout:
        return False
    elif idletime > timeout * 2:
        return False
    else:
        return True

if __name__ == '__main__':
    main()
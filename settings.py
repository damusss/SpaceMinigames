import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# window
WIDTH = screensize[0]
HEIGHT = screensize[1]
#WIDTH = 1800
#HEIGHT = 1000
FPS = 60

# stars
STAR_COLOR = 'white'
STARS_NUM = 200
STAR_SIZES = [3,10]

# main menu
G_SCALES = [(6,6),(0.4,0.4),(1.2,1.2),(0.35,0.35)]
G_NAMES = ["Asteroids","Space Battle","Space Invaders",'Base Defender']
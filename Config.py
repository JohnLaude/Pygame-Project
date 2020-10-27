# Options and Config File

# Constants
TITLE = "BUNNY HOP"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'tempus sans itc'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
FADE = 500
SCORE_TO_BEAT = 10000000000

# Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
GRAVITY = 0.8
PLAYER_JUMP = 18
IDLE_TIME = 350
WALK_TIME = 200

# Game Properties
BOOST_POWER = 60
POWERUP_FREQ = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0
CLOUD_SCALE = 3
CLOUD_FREQ = 7

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 300),
                 (350, 200),
                 (175, 100)]

# Color Definitions
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
RED = (255, 0, 0)
BRICK = (165, 42, 42)
PINK = (255,192,203)
GREEN = (0, 255, 0)
FORESTGRN = (0, 50, 0)
LIME = (180,255,100)
BLUEGREEN = (0,255,170)
GRAY = (127,127,127)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
SKYBLUE = (0, 255, 255)
BEIGE = (255,228,196)
BGCOLOR = LIGHTBLUE
TXT_COLOR = BLACK
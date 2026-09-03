# RasPipBoy: A Pip-Boy 3000 implementation for Raspberry Pi
#	Neal D Corbett, 2013
# Configuration data

# Device options 
#  (These will be automatically be set to 'False' if unavailable)
USE_INTERNET = True		# Download map/place data via internet connection
USE_GPS = False		# Use GPS module, accessed via GPSD daemon
USE_SOUND = False		# Play sounds via RasPi's current sound-source
USE_CAMERA = False		# Use RasPi camera-module as V.A.T.S
USE_GPIO = False         # Use rpi gpio for buttons & rotary encoder

QUICKLOAD = True		# If true, commandline-startup bits aren't rendered
FORCE_DOWNLOAD = False	# Don't use cached map-data, if online

USE_CURSOR = False # show the cursor in the map screen. enable for mouse, disable for touchscreen.

# Render screen-objects at this size - smaller is faster
WIDTH = 800
HEIGHT = 480

# Brightness control
BACKLIGHT_SYSFS_PATH = ""

# Address for map's default position: 
#	(used if GPS is inactive)
defaultPlace = "Washington DC"

# Player data:
PLAYERNAME = 'Jeeeef'
PLAYERLEVEL = 33

FPS = 5

import pygame, os

# My Google-API key:
# (this is limited to only 2000 location requests a day, 
#    so please don't use this key if you're making your own project!)
gKey = 'Your_Key_Here'

# Test camera:
if USE_CAMERA:
	# Is there a camera module connected?
	def hasCamera():
		try:
			import picamera
			camera = picamera.PiCamera()
			camera.close()
			return True
		except:
			return False
	
	USE_CAMERA = hasCamera()
print("CAMERA: %s" %(USE_CAMERA))

# Downloaded/auto-generated data will be put here:
CACHEPATH = 'cache'
if not os.path.exists(CACHEPATH):
	os.makedirs(CACHEPATH)

DRAWCOLOUR = pygame.Color (255, 255, 255)
TINTCOLOUR = pygame.Color (242, 117, 21)
SELBOXGREY = 50

EVENTS = {
	'SONG_END': pygame.USEREVENT + 1
}

print("Loading images...")
IMAGES = {
	"background":pygame.image.load('images/pipboy_back.png'),
	"scanline":pygame.image.load('images/pipboyscanlines.png'),
	"distort":pygame.image.load('images/pipboydistorteffectmap.png'),
	"statusboy":pygame.image.load('images/pipboy_statusboy.png'),
}

print("(done)")

# Test internet connection:
if USE_INTERNET:
	import urllib.request, urllib.error
	
	def internet_on():
		try:
			# Can we access this Google address?
			response=urllib.request.urlopen('https://www.google.com',timeout=5)
			return True
		except urllib.error.URLError as err: pass
		return False
	
	USE_INTERNET = internet_on()
print("INTERNET: %s" %(USE_INTERNET))

# Test and set up sounds::
MINHUMVOL = 0.7
MAXHUMVOL = 1.0
if USE_SOUND:
	try:
		print("Loading sounds...")
		pygame.mixer.init(44100, -16, 2, 2048)

		SOUNDS = {
			"start":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_access_up.wav'),
			"end":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_access_down.wav'),
			"hum":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_hum_lp.wav'),
			"scroll":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_scroll.wav'),
			"changetab":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_tab.wav'),
			"changemode":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_mode.wav'),
			"static":		pygame.mixer.Sound('sounds/radio/ui_radio_static_lp.wav'),
			"tapestart":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_holotape_start.wav'),
			"tapestop":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_holotape_stop.wav'),
			"lighton":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_light_on.wav'),
			"lightoff":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_light_off.wav'),
			"beacon":		pygame.mixer.Sound('sounds/radio/beacon/ui_radio_beacon_header.wav'),
			"camerastart":	pygame.mixer.Sound('sounds/vats/ui_vats_enter.wav'),
			#"cameraexit":	pygame.mixer.Sound('sounds/vats/ui_vats_exit.wav'),
		}
		SOUNDS["hum"].set_volume(MINHUMVOL)
		print("(done)")
	except:
		USE_SOUND = False
print("SOUND: %s" %(USE_SOUND))

# Set up fonts:
pygame.font.init()
kernedFontName = 'fonts/monofonto-kerned.ttf'
monoFontName = 'fonts/monofonto.ttf'

# Scale font-sizes to chosen resolution:
FONT_SML = pygame.font.Font(kernedFontName, int (HEIGHT * (12.0 / 360)))
FONT_MED = pygame.font.Font(kernedFontName, int (HEIGHT * (16.0 / 360.0)))
FONT_LRG = pygame.font.Font(kernedFontName, int (HEIGHT * (18.0 / 360.0)))
MONOFONT = pygame.font.Font(monoFontName, int (HEIGHT * (16.0 / 360.0)))

# Find monofont's character-size:
tempImg = MONOFONT.render("X", True, DRAWCOLOUR, (0, 0, 0))
charHeight = tempImg.get_height()
charWidth = tempImg.get_width()
del tempImg

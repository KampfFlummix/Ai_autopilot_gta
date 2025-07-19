# Bildschirmeinstellungen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_REGION = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Steuerungstasten
KEY_TOGGLE_AUTOPILOT = 'f1'
KEY_SWITCH_MODE = 'f2'
KEY_TOGGLE_SPEED = 'f3'
KEY_EMERGENCY_STOP = 'f4'

# Geschwindigkeitsmodi
SPEED_MODES = {
    'SLOW': 0.6,    # 60% der Maximalgeschwindigkeit
    'NORMAL': 0.85, # 85% der Maximalgeschwindigkeit
    'FAST': 1.0      # Volle Geschwindigkeit
}

# Verkehrsregeln
ALLOW_RIGHT_TURN_ON_RED = True
MIN_SAFETY_DISTANCE = 3.0  # Meter

# Pfade
DATA_LOG_PATH = "data_logs/"
MODEL_PATH = "models/driving_model.h5"

# Lernparameter
LEARNING_RATE = 0.001
BATCH_SIZE = 32
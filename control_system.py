import pydirectinput
import time
from config import SPEED_MODES

class ControlSystem:
    def __init__(self):
        self.speed_mode = 'NORMAL'
        self.current_steering = 0
        self.current_speed = 0
        
    def toggle_speed_mode(self):
        modes = list(SPEED_MODES.keys())
        current_index = modes.index(self.speed_mode)
        next_index = (current_index + 1) % len(modes)
        self.speed_mode = modes[next_index]
        
    def apply_controls(self, steering, speed):
        self.current_steering = steering
        self.current_speed = speed * SPEED_MODES[self.speed_mode]
        
        # Tastatureingaben simulieren
        if steering < -0.1:
            pydirectinput.keyDown('a')
            pydirectinput.keyUp('d')
        elif steering > 0.1:
            pydirectinput.keyDown('d')
            pydirectinput.keyUp('a')
        else:
            pydirectinput.keyUp('a')
            pydirectinput.keyUp('d')
            
        if self.current_speed > 0:
            pydirectinput.keyDown('w')
        else:
            pydirectinput.keyUp('w')
            
    def release_controls(self):
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('a')
        pydirectinput.keyUp('d')
        self.current_steering = 0
        self.current_speed = 0
        
    def get_current_controls(self):
        return {
            'steering': self.current_steering,
            'speed': self.current_speed
        }
import numpy as np
import random

class NPCMode:
    def calculate_behavior(self, current_pos):
        # Simuliertes NPC-Verhalten
        steering = np.random.uniform(-0.3, 0.3)
        
        # Gelegentlich Geschwindigkeit ändern
        if random.random() < 0.1:
            speed = random.choice([30, 50, 70])
        else:
            speed = 50
            
        return steering, speed
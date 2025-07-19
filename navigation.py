import numpy as np

class Navigation:
    def __init__(self):
        self.waypoints = []
        self.current_waypoint_index = 0
        
    def load_route(self, route_name):
        # Hier sollten Wegpunkte geladen werden
        self.waypoints = [
            {'x': 10, 'y': 20},
            {'x': 30, 'y': 40},
            {'x': 50, 'y': 60}
        ]
        self.current_waypoint_index = 0
    
    def calculate_path(self, current_pos):
        if not self.waypoints:
            return 0, 0, "STRAIGHT"
            
        target = self.waypoints[self.current_waypoint_index]
        dx = target['x'] - current_pos['x']
        dy = target['y'] - current_pos['y']
        
        # Distanz berechnen
        distance = np.sqrt(dx**2 + dy**2)
        
        # Zum nächsten Wegpunkt wechseln
        if distance < 5:
            self.current_waypoint_index = (self.current_waypoint_index + 1) % len(self.waypoints)
            target = self.waypoints[self.current_waypoint_index]
            dx = target['x'] - current_pos['x']
            dy = target['y'] - current_pos['y']
            distance = np.sqrt(dx**2 + dy**2)
        
        # Richtung berechnen
        angle = np.arctan2(dy, dx)
        steering = np.sin(angle - current_pos['heading'] * np.pi/180)
        
        # Abbiegerichtung bestimmen
        angle_diff = angle - current_pos['heading'] * np.pi/180
        if angle_diff > 0.5:
            next_action = "RIGHT"
        elif angle_diff < -0.5:
            next_action = "LEFT"
        else:
            next_action = "STRAIGHT"
        
        # Geschwindigkeit basierend auf Distanz
        speed = min(80, distance * 2)
        
        return steering, speed, next_action
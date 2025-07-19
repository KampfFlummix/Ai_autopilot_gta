from config import ALLOW_RIGHT_TURN_ON_RED

class TrafficRules:
    def apply_rules(self, traffic_light, turning_direction):
        if traffic_light == "RED":
            if turning_direction == "RIGHT" and ALLOW_RIGHT_TURN_ON_RED:
                return "CAUTIOUS"  # Vorsichtig rechts abbiegen
            return "STOP"  # Anhalten bei Rot
        
        elif traffic_light == "GREEN":
            return "PROCEED"  # Weiterfahren
        
        else:  # UNKNOWN oder kein Licht
            return "CAUTIOUS"  # Vorsichtig weiterfahren
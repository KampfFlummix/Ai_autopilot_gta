import keyboard
import time
import threading
import numpy as np
from modules.vision_processor import VisionProcessor
from modules.navigation import Navigation
from modules.npc_mode import NPCMode
from modules.control_system import ControlSystem
from modules.learning_module import LearningModule
from modules.safety_system import SafetySystem
from modules.traffic_rules import TrafficRules
import config

class Autopilot:
    def __init__(self):
        self.running = False
        self.mode = "GPS"  # "GPS" oder "NPC"
        self.vision = VisionProcessor()
        self.navigation = Navigation()
        self.npc = NPCMode()
        self.control = ControlSystem()
        self.learning = LearningModule()
        self.safety = SafetySystem()
        self.traffic_rules = TrafficRules()
        self.current_speed = 0
        self.emergency_stop = False
        
        # Threads
        self.vision_thread = threading.Thread(target=self.update_vision)
        self.control_thread = threading.Thread(target=self.update_controls)
        
    def start(self):
        self.running = True
        self.vision_thread.daemon = True
        self.control_thread.daemon = True
        self.vision_thread.start()
        self.control_thread.start()
        print("Autopilot gestartet")
        
    def stop(self):
        self.running = False
        self.control.release_controls()
        print("Autopilot gestoppt")
        
    def toggle_autopilot(self):
        if self.running:
            self.stop()
        else:
            self.start()
            
    def switch_mode(self):
        self.mode = "NPC" if self.mode == "GPS" else "GPS"
        print(f"Modus gewechselt zu: {self.mode}")
        
    def toggle_speed(self):
        self.control.toggle_speed_mode()
        
    def emergency_stop(self):
        self.emergency_stop = True
        self.control.release_controls()
        self.learning.save_data()
        print("NOTSTOP aktiviert")
        
    def update_vision(self):
        while self.running:
            try:
                # Bildschirm erfassen und verarbeiten
                frame = self.vision.capture_screen()
                traffic_light = self.vision.detect_traffic_light(frame)
                obstacles = self.vision.detect_obstacles(frame)
                
                # Daten für Lernmodul speichern
                self.learning.record_data(frame, {
                    'traffic_light': traffic_light,
                    'obstacles': obstacles,
                    'controls': self.control.get_current_controls()
                })
                
                time.sleep(0.05)
            except Exception as e:
                print(f"Vision-Fehler: {str(e)}")
                time.sleep(1)
                
    def update_controls(self):
        while self.running:
            try:
                if self.emergency_stop:
                    time.sleep(0.1)
                    continue
                    
                # Aktuelle Position (simuliert - muss mit Spiel-API verbunden werden)
                current_pos = self.get_game_position()
                
                if self.mode == "GPS":
                    target_steering, target_speed, next_action = self.navigation.calculate_path(current_pos)
                else:
                    target_steering, target_speed = self.npc.calculate_behavior(current_pos)
                
                # Verkehrsregeln anwenden
                action = self.traffic_rules.apply_rules(
                    traffic_light=self.vision.current_traffic_light,
                    turning_direction=next_action
                )
                
                if action == "STOP":
                    target_speed = 0
                elif action == "CAUTIOUS":
                    target_speed *= 0.5
                
                # Sicherheitsüberprüfung
                if self.safety.check_collision(self.vision.current_obstacles):
                    target_speed = 0
                
                # Steuerung anwenden
                self.control.apply_controls(target_steering, target_speed)
                
                time.sleep(0.05)
            except Exception as e:
                print(f"Steuerungsfehler: {str(e)}")
                self.control.release_controls()
                time.sleep(1)
    
    def get_game_position(self):
        """Simulierte Position - Muss mit Spiel-API verbunden werden"""
        return {
            'x': np.random.uniform(0, 100),
            'y': np.random.uniform(0, 100),
            'z': 0,
            'speed': self.current_speed,
            'heading': np.random.uniform(0, 360)
        }

def main():
    autopilot = Autopilot()
    
    # Tastatur-Hotkeys
    keyboard.add_hotkey(config.KEY_TOGGLE_AUTOPILOT, autopilot.toggle_autopilot)
    keyboard.add_hotkey(config.KEY_SWITCH_MODE, autopilot.switch_mode)
    keyboard.add_hotkey(config.KEY_TOGGLE_SPEED, autopilot.toggle_speed)
    keyboard.add_hotkey(config.KEY_EMERGENCY_STOP, autopilot.emergency_stop)
    
    print("Autopilot-System bereit. Drücke F1 zum Starten.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        autopilot.stop()
        print("System beendet")

if __name__ == "__main__":
    main()
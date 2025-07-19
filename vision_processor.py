import cv2
import numpy as np
import mss
from config import SCREEN_REGION

class VisionProcessor:
    def __init__(self):
        self.sct = mss.mss()
        self.current_traffic_light = "UNKNOWN"
        self.current_obstacles = []
        
    def capture_screen(self):
        img = self.sct.grab(SCREEN_REGION)
        return np.array(img)
    
    def detect_traffic_light(self, frame):
        # ROI für Ampel definieren
        roi = frame[50:200, SCREEN_REGION[2]//2-50:SCREEN_REGION[2]//2+50]
        
        # Farberkennung
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Rot erkennen
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        
        # Grün erkennen
        lower_green = np.array([40, 50, 50])
        upper_green = np.array([90, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        
        # Entscheidung
        if np.sum(mask_red) > 10000:
            self.current_traffic_light = "RED"
        elif np.sum(mask_green) > 10000:
            self.current_traffic_light = "GREEN"
        else:
            self.current_traffic_light = "UNKNOWN"
            
        return self.current_traffic_light
    
    def detect_obstacles(self, frame):
        # Vereinfachte Hinderniserkennung
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        # Konturen finden
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        obstacles = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(contour)
                obstacles.append({
                    'x': x + w//2,
                    'y': y + h//2,
                    'width': w,
                    'height': h,
                    'distance': self.estimate_distance(w)
                })
        
        self.current_obstacles = obstacles
        return obstacles
    
    def estimate_distance(self, width):
        # Vereinfachte Distanzschätzung
        return 5000 / width if width > 0 else 100
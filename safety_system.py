from config import MIN_SAFETY_DISTANCE

class SafetySystem:
    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if obstacle['distance'] < MIN_SAFETY_DISTANCE:
                return True
        return False
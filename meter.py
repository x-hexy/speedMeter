import time
from geopy.distance import geodesic

class TrainSpeedCalculator:
    def __init__(self):
        self.locations = []  # Stores tuples of (latitude, longitude, timestamp)
    
    def record_location(self, latitude, longitude):
        timestamp = time.time()
        self.locations.append((latitude, longitude, timestamp))
        
        # Maintain only the last two points for speed calculation
        if len(self.locations) > 2:
            self.locations.pop(0)
    
    def calculate_speed(self):
        if len(self.locations) < 2:
            return None  # Need at least two points
        
        (lat1, lon1, time1), (lat2, lon2, time2) = self.locations
        distance = geodesic((lat1, lon1), (lat2, lon2)).meters  # Distance in meters
        time_elapsed = time2 - time1  # Time in seconds
        
        if time_elapsed == 0:
            return None  # Avoid division by zero
        
        speed = distance / time_elapsed  # Speed in meters/second
        return speed * 3.6  # Convert to km/h

# Usage
train_speed_calculator = TrainSpeedCalculator()

# Simulated data: replace with actual GPS data
train_speed_calculator.record_location(35.681236, 139.767125)  # Location 1
time.sleep(4)  # Wait 2 seconds
train_speed_calculator.record_location(35.689487, 139.691711)  # Location 2

speed = train_speed_calculator.calculate_speed()
if speed:
    print(f"Train Speed: {speed:.2f} km/h")
else:
    print("Insufficient data to calculate speed.")

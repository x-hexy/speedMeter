from flask import Flask, render_template, request, redirect, url_for
from geopy.distance import geodesic
import time

app = Flask(__name__)

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

# Initialize the speed calculator
train_speed_calculator = TrainSpeedCalculator()

@app.route('/', methods=['GET', 'POST'])
def index():
    speed = None
    if request.method == 'POST':
        try:
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])
            
            # Record the location
            train_speed_calculator.record_location(latitude, longitude)
            
            # Calculate speed
            speed = train_speed_calculator.calculate_speed()
        except ValueError:
            speed = "Invalid input, please enter numeric coordinates."

    return render_template('index.html', speed=speed)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.spatial.transform import Rotation
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class CrashDetector:
    def __init__(self, gyro_file='gyro_processed.csv', accel_file='accel_processed.csv'):
        self.gyro_data = pd.read_csv(gyro_file)
        self.accel_data = pd.read_csv(accel_file)
        self.sync_data()
        self.calculate_features()
        
    def sync_data(self):
        self.data = pd.merge(self.gyro_data, self.accel_data, 
                           on='time_combined', how='inner')
        self.data = self.data.sort_values('time_combined').reset_index(drop=True)
        
    def calculate_features(self):
        dt = np.diff(self.data['time_combined'])
        dt = np.insert(dt, 0, dt[0] if len(dt) > 0 else 0.01)
        
        # Basic magnitudes
        self.data['accel_magnitude'] = np.sqrt(
            self.data['accel_x']**2 + self.data['accel_y']**2 + self.data['accel_z']**2)
        self.data['gyro_magnitude'] = np.sqrt(
            self.data['gyro_x']**2 + self.data['gyro_y']**2 + self.data['gyro_z']**2)
        
        # Jerk (rate of acceleration change)
        self.data['jerk_x'] = np.gradient(self.data['accel_x'], dt)
        self.data['jerk_y'] = np.gradient(self.data['accel_y'], dt)
        self.data['jerk_z'] = np.gradient(self.data['accel_z'], dt)
        self.data['jerk_magnitude'] = np.sqrt(
            self.data['jerk_x']**2 + self.data['jerk_y']**2 + self.data['jerk_z']**2)
        
        # Orientation
        self.data['roll'] = np.cumsum(self.data['gyro_x'] * dt)
        self.data['pitch'] = np.cumsum(self.data['gyro_y'] * dt)
        self.data['yaw'] = np.cumsum(self.data['gyro_z'] * dt)
        
    def detect_crashes(self):
        events = []
        
        # Threshold-based detection
        accel_threshold = 15.0
        gyro_threshold = 2.0
        jerk_threshold = 50.0
        
        for i, row in self.data.iterrows():
            if row['accel_magnitude'] > accel_threshold:
                events.append({
                    'time': row['time_combined'],
                    'type': 'high_acceleration',
                    'magnitude': row['accel_magnitude'],
                    'confidence': min(row['accel_magnitude'] / accel_threshold, 1.0)
                })
            
            if row['gyro_magnitude'] > gyro_threshold:
                events.append({
                    'time': row['time_combined'],
                    'type': 'high_rotation',
                    'magnitude': row['gyro_magnitude'],
                    'confidence': min(row['gyro_magnitude'] / gyro_threshold, 1.0)
                })
            
            if row['jerk_magnitude'] > jerk_threshold:
                events.append({
                    'time': row['time_combined'],
                    'type': 'high_jerk',
                    'magnitude': row['jerk_magnitude'],
                    'confidence': min(row['jerk_magnitude'] / jerk_threshold, 1.0)
                })
        
        return events
    
    def generate_blackbox_trigger(self, events):
        triggers = []
        for event in events:
            if event['confidence'] > 0.7:
                triggers.append({
                    'time': event['time'],
                    'action': 'start_recording',
                    'duration': 30,
                    'priority': 'high' if event['confidence'] > 0.8 else 'medium'
                })
        return triggers

def main():
    detector = CrashDetector()
    events = detector.detect_crashes()
    triggers = detector.generate_blackbox_trigger(events)
    
    print(f"Detected {len(events)} crash events")
    print(f"Generated {len(triggers)} blackbox triggers")
    
    for event in events[:5]:
        print(f"Event: {event['type']} at {event['time']:.2f}s (confidence: {event['confidence']:.2f})")

if __name__ == "__main__":
    main()

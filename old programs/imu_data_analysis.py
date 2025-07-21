import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def analyze_imu_data():
    """
    Analyze and interpret IMU (Inertial Measurement Unit) data from camera sensors.
    This script provides detailed labeling and interpretation of accelerometer and gyroscope data.
    """
    
    print("="*80)
    print("IMU DATA ANALYSIS & INTERPRETATION")
    print("="*80)
    
    # Create a large figure for all plots
    fig = plt.figure(figsize=(20, 16))
    
    # ===== ACCELEROMETER DATA ANALYSIS =====
    print("\n📊 ACCELEROMETER DATA ANALYSIS:")
    print("-" * 50)
    
    try:
        # Read accelerometer data
        accel_data = pd.read_csv('accel.csv', header=None)
        
        # Define column labels based on ROS IMU message structure
        accel_columns = [
            'timestamp_sec',           # Unix timestamp (seconds)
            'timestamp_nsec',          # Unix timestamp (nanoseconds)
            'frame_id',                # Reference frame (camera_accel_optical_frame)
            'orientation_x',           # Quaternion orientation X
            'orientation_y',           # Quaternion orientation Y
            'orientation_z',           # Quaternion orientation Z
            'orientation_w',           # Quaternion orientation W
            'orientation_covariance_0', # Orientation covariance matrix (3x3)
            'orientation_covariance_1',
            'orientation_covariance_2',
            'orientation_covariance_3',
            'orientation_covariance_4',
            'orientation_covariance_5',
            'orientation_covariance_6',
            'orientation_covariance_7',
            'orientation_covariance_8',
            'angular_velocity_x',      # Angular velocity X (rad/s)
            'angular_velocity_y',      # Angular velocity Y (rad/s)
            'angular_velocity_z',      # Angular velocity Z (rad/s)
            'angular_velocity_covariance_0', # Angular velocity covariance
            'angular_velocity_covariance_1',
            'angular_velocity_covariance_2',
            'angular_velocity_covariance_3',
            'angular_velocity_covariance_4',
            'angular_velocity_covariance_5',
            'angular_velocity_covariance_6',
            'angular_velocity_covariance_7',
            'angular_velocity_covariance_8',
            'linear_acceleration_x',   # Linear acceleration X (m/s²)
            'linear_acceleration_y',   # Linear acceleration Y (m/s²)
            'linear_acceleration_z',   # Linear acceleration Z (m/s²)
            'linear_acceleration_covariance_0', # Linear acceleration covariance
            'linear_acceleration_covariance_1',
            'linear_acceleration_covariance_2',
            'linear_acceleration_covariance_3',
            'linear_acceleration_covariance_4',
            'linear_acceleration_covariance_5',
            'linear_acceleration_covariance_6',
            'linear_acceleration_covariance_7',
            'linear_acceleration_covariance_8'
        ]
        
        # Assign column names
        accel_data.columns = accel_columns
        
        print(f"📈 Accelerometer Data Summary:")
        print(f"   - Total data points: {len(accel_data)}")
        print(f"   - Time range: {accel_data['timestamp_sec'].min()} to {accel_data['timestamp_sec'].max()}")
        print(f"   - Duration: {accel_data['timestamp_sec'].max() - accel_data['timestamp_sec'].min():.2f} seconds")
        print(f"   - Sampling rate: ~{len(accel_data) / (accel_data['timestamp_sec'].max() - accel_data['timestamp_sec'].min()):.1f} Hz")
        
        # Convert timestamp to datetime for better interpretation
        accel_data['datetime'] = pd.to_datetime(accel_data['timestamp_sec'], unit='s')
        
        print(f"\n📊 Linear Acceleration Analysis:")
        print(f"   - X-axis range: {accel_data['linear_acceleration_x'].min():.3f} to {accel_data['linear_acceleration_x'].max():.3f} m/s²")
        print(f"   - Y-axis range: {accel_data['linear_acceleration_y'].min():.3f} to {accel_data['linear_acceleration_y'].max():.3f} m/s²")
        print(f"   - Z-axis range: {accel_data['linear_acceleration_z'].min():.3f} to {accel_data['linear_acceleration_z'].max():.3f} m/s²")
        print(f"   - Gravity component (Z-axis): ~{accel_data['linear_acceleration_z'].mean():.3f} m/s² (expected ~9.81 m/s²)")
        
        print(f"\n🔄 Angular Velocity Analysis:")
        print(f"   - X-axis range: {accel_data['angular_velocity_x'].min():.3f} to {accel_data['angular_velocity_x'].max():.3f} rad/s")
        print(f"   - Y-axis range: {accel_data['angular_velocity_y'].min():.3f} to {accel_data['angular_velocity_y'].max():.3f} rad/s")
        print(f"   - Z-axis range: {accel_data['angular_velocity_z'].min():.3f} to {accel_data['angular_velocity_z'].max():.3f} rad/s")
        
        # Plot accelerometer data
        plt.subplot(3, 3, 1)
        plt.plot(accel_data.index, accel_data['linear_acceleration_x'], 'r-', label='X-axis', linewidth=1.5)
        plt.plot(accel_data.index, accel_data['linear_acceleration_y'], 'g-', label='Y-axis', linewidth=1.5)
        plt.plot(accel_data.index, accel_data['linear_acceleration_z'], 'b-', label='Z-axis', linewidth=1.5)
        plt.title('Linear Acceleration (m/s²)')
        plt.xlabel('Sample Index')
        plt.ylabel('Acceleration (m/s²)')
        plt.legend()
        plt.grid(True)
        
        plt.subplot(3, 3, 2)
        plt.plot(accel_data.index, accel_data['angular_velocity_x'], 'r-', label='X-axis', linewidth=1.5)
        plt.plot(accel_data.index, accel_data['angular_velocity_y'], 'g-', label='Y-axis', linewidth=1.5)
        plt.plot(accel_data.index, accel_data['angular_velocity_z'], 'b-', label='Z-axis', linewidth=1.5)
        plt.title('Angular Velocity (rad/s)')
        plt.xlabel('Sample Index')
        plt.ylabel('Angular Velocity (rad/s)')
        plt.legend()
        plt.grid(True)
        
        # Calculate magnitude of acceleration
        accel_data['acceleration_magnitude'] = np.sqrt(
            accel_data['linear_acceleration_x']**2 + 
            accel_data['linear_acceleration_y']**2 + 
            accel_data['linear_acceleration_z']**2
        )
        
        plt.subplot(3, 3, 3)
        plt.plot(accel_data.index, accel_data['acceleration_magnitude'], 'purple', linewidth=1.5)
        plt.title('Acceleration Magnitude')
        plt.xlabel('Sample Index')
        plt.ylabel('Magnitude (m/s²)')
        plt.grid(True)
        
        # Histogram of acceleration values
        plt.subplot(3, 3, 4)
        plt.hist(accel_data['linear_acceleration_x'], bins=50, alpha=0.7, label='X-axis', color='red')
        plt.hist(accel_data['linear_acceleration_y'], bins=50, alpha=0.7, label='Y-axis', color='green')
        plt.hist(accel_data['linear_acceleration_z'], bins=50, alpha=0.7, label='Z-axis', color='blue')
        plt.title('Acceleration Distribution')
        plt.xlabel('Acceleration (m/s²)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        
    except Exception as e:
        print(f"   ❌ Error reading accelerometer data: {e}")
    
    # ===== GYROSCOPE DATA ANALYSIS =====
    print("\n\n🔄 GYROSCOPE DATA ANALYSIS:")
    print("-" * 50)
    
    try:
        # Read gyroscope data
        gyro_data = pd.read_csv('camera_camera_gyro_sample.csv', header=None)
        
        # Define column labels for gyroscope data (40 columns)
        gyro_columns = [
            'timestamp_sec',           # Unix timestamp (seconds)
            'timestamp_nsec',          # Unix timestamp (nanoseconds)
            'frame_id',                # Reference frame (camera_gyro_optical_frame)
            'orientation_x',           # Quaternion orientation X
            'orientation_y',           # Quaternion orientation Y
            'orientation_z',           # Quaternion orientation Z
            'orientation_w',           # Quaternion orientation W
            'orientation_covariance_0', # Orientation covariance matrix (3x3)
            'orientation_covariance_1',
            'orientation_covariance_2',
            'orientation_covariance_3',
            'orientation_covariance_4',
            'orientation_covariance_5',
            'orientation_covariance_6',
            'orientation_covariance_7',
            'orientation_covariance_8',
            'angular_velocity_x',      # Angular velocity X (rad/s)
            'angular_velocity_y',      # Angular velocity Y (rad/s)
            'angular_velocity_z',      # Angular velocity Z (rad/s)
            'angular_velocity_covariance_0', # Angular velocity covariance
            'angular_velocity_covariance_1',
            'angular_velocity_covariance_2',
            'angular_velocity_covariance_3',
            'angular_velocity_covariance_4',
            'angular_velocity_covariance_5',
            'angular_velocity_covariance_6',
            'angular_velocity_covariance_7',
            'angular_velocity_covariance_8',
            'linear_acceleration_x',   # Linear acceleration X (m/s²)
            'linear_acceleration_y',   # Linear acceleration Y (m/s²)
            'linear_acceleration_z',   # Linear acceleration Z (m/s²)
            'linear_acceleration_covariance_0', # Linear acceleration covariance
            'linear_acceleration_covariance_1',
            'linear_acceleration_covariance_2',
            'linear_acceleration_covariance_3',
            'linear_acceleration_covariance_4',
            'linear_acceleration_covariance_5',
            'linear_acceleration_covariance_6',
            'linear_acceleration_covariance_7',
            'linear_acceleration_covariance_8'
        ]
        
        # Assign column names
        gyro_data.columns = gyro_columns
        
        print(f"📈 Gyroscope Data Summary:")
        print(f"   - Total data points: {len(gyro_data)}")
        print(f"   - Time range: {gyro_data['timestamp_sec'].min()} to {gyro_data['timestamp_sec'].max()}")
        print(f"   - Duration: {gyro_data['timestamp_sec'].max() - gyro_data['timestamp_sec'].min():.2f} seconds")
        print(f"   - Sampling rate: ~{len(gyro_data) / (gyro_data['timestamp_sec'].max() - gyro_data['timestamp_sec'].min()):.1f} Hz")
        
        print(f"\n🔄 Angular Velocity Analysis:")
        print(f"   - X-axis range: {gyro_data['angular_velocity_x'].min():.3f} to {gyro_data['angular_velocity_x'].max():.3f} rad/s")
        print(f"   - Y-axis range: {gyro_data['angular_velocity_y'].min():.3f} to {gyro_data['angular_velocity_y'].max():.3f} rad/s")
        print(f"   - Z-axis range: {gyro_data['angular_velocity_z'].min():.3f} to {gyro_data['angular_velocity_z'].max():.3f} rad/s")
        print(f"   - X-axis mean: {gyro_data['angular_velocity_x'].mean():.3f} rad/s")
        print(f"   - Y-axis mean: {gyro_data['angular_velocity_y'].mean():.3f} rad/s")
        print(f"   - Z-axis mean: {gyro_data['angular_velocity_z'].mean():.3f} rad/s")
        
        print(f"\n📊 Linear Acceleration Analysis (from gyro sensor):")
        print(f"   - X-axis range: {gyro_data['linear_acceleration_x'].min():.3f} to {gyro_data['linear_acceleration_x'].max():.3f} m/s²")
        print(f"   - Y-axis range: {gyro_data['linear_acceleration_y'].min():.3f} to {gyro_data['linear_acceleration_y'].max():.3f} m/s²")
        print(f"   - Z-axis range: {gyro_data['linear_acceleration_z'].min():.3f} to {gyro_data['linear_acceleration_z'].max():.3f} m/s²")
        
        # Plot gyroscope data
        plt.subplot(3, 3, 5)
        plt.plot(gyro_data.index, gyro_data['angular_velocity_x'], 'r-', label='X-axis', linewidth=1.5)
        plt.plot(gyro_data.index, gyro_data['angular_velocity_y'], 'g-', label='Y-axis', linewidth=1.5)
        plt.plot(gyro_data.index, gyro_data['angular_velocity_z'], 'b-', label='Z-axis', linewidth=1.5)
        plt.title('Gyroscope Angular Velocity (rad/s)')
        plt.xlabel('Sample Index')
        plt.ylabel('Angular Velocity (rad/s)')
        plt.legend()
        plt.grid(True)
        
        # Calculate magnitude of angular velocity
        gyro_data['angular_velocity_magnitude'] = np.sqrt(
            gyro_data['angular_velocity_x']**2 + 
            gyro_data['angular_velocity_y']**2 + 
            gyro_data['angular_velocity_z']**2
        )
        
        plt.subplot(3, 3, 6)
        plt.plot(gyro_data.index, gyro_data['angular_velocity_magnitude'], 'orange', linewidth=1.5)
        plt.title('Angular Velocity Magnitude')
        plt.xlabel('Sample Index')
        plt.ylabel('Magnitude (rad/s)')
        plt.grid(True)
        
        # Histogram of angular velocity values
        plt.subplot(3, 3, 7)
        plt.hist(gyro_data['angular_velocity_x'], bins=50, alpha=0.7, label='X-axis', color='red')
        plt.hist(gyro_data['angular_velocity_y'], bins=50, alpha=0.7, label='Y-axis', color='green')
        plt.hist(gyro_data['angular_velocity_z'], bins=50, alpha=0.7, label='Z-axis', color='blue')
        plt.title('Angular Velocity Distribution')
        plt.xlabel('Angular Velocity (rad/s)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        
    except Exception as e:
        print(f"   ❌ Error reading gyroscope data: {e}")
    
    # ===== SAMPLE ACCELEROMETER DATA ANALYSIS =====
    print("\n\n📊 SAMPLE ACCELEROMETER DATA ANALYSIS:")
    print("-" * 50)
    
    try:
        # Read sample accelerometer data
        sample_accel_data = pd.read_csv('camera_camera_accel_sample.csv', header=None)
        
        # Use same column structure as main accelerometer data
        sample_accel_data.columns = accel_columns
        
        print(f"📈 Sample Accelerometer Data Summary:")
        print(f"   - Total data points: {len(sample_accel_data)}")
        print(f"   - Time range: {sample_accel_data['timestamp_sec'].min()} to {sample_accel_data['timestamp_sec'].max()}")
        print(f"   - Duration: {sample_accel_data['timestamp_sec'].max() - sample_accel_data['timestamp_sec'].min():.2f} seconds")
        
        print(f"\n📊 Sample Linear Acceleration Analysis:")
        print(f"   - X-axis range: {sample_accel_data['linear_acceleration_x'].min():.3f} to {sample_accel_data['linear_acceleration_x'].max():.3f} m/s²")
        print(f"   - Y-axis range: {sample_accel_data['linear_acceleration_y'].min():.3f} to {sample_accel_data['linear_acceleration_y'].max():.3f} m/s²")
        print(f"   - Z-axis range: {sample_accel_data['linear_acceleration_z'].min():.3f} to {sample_accel_data['linear_acceleration_z'].max():.3f} m/s²")
        
        # Plot sample accelerometer data
        plt.subplot(3, 3, 8)
        plt.plot(sample_accel_data.index, sample_accel_data['linear_acceleration_x'], 'r-', label='X-axis', linewidth=1.5)
        plt.plot(sample_accel_data.index, sample_accel_data['linear_acceleration_y'], 'g-', label='Y-axis', linewidth=1.5)
        plt.plot(sample_accel_data.index, sample_accel_data['linear_acceleration_z'], 'b-', label='Z-axis', linewidth=1.5)
        plt.title('Sample: Linear Acceleration (m/s²)')
        plt.xlabel('Sample Index')
        plt.ylabel('Acceleration (m/s²)')
        plt.legend()
        plt.grid(True)
        
        # Calculate and plot acceleration magnitude for sample
        sample_accel_data['acceleration_magnitude'] = np.sqrt(
            sample_accel_data['linear_acceleration_x']**2 + 
            sample_accel_data['linear_acceleration_y']**2 + 
            sample_accel_data['linear_acceleration_z']**2
        )
        
        plt.subplot(3, 3, 9)
        plt.plot(sample_accel_data.index, sample_accel_data['acceleration_magnitude'], 'purple', linewidth=1.5)
        plt.title('Sample: Acceleration Magnitude')
        plt.xlabel('Sample Index')
        plt.ylabel('Magnitude (m/s²)')
        plt.grid(True)
        
    except Exception as e:
        print(f"   ❌ Error reading sample accelerometer data: {e}")
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('imu_data_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 Plots saved as 'imu_data_analysis.png'")
    
    # ===== DATA INTERPRETATION GUIDE =====
    print("\n\n📖 DATA INTERPRETATION GUIDE:")
    print("="*50)
    
    print("\n🎯 WHAT EACH COLUMN REPRESENTS:")
    print("-" * 30)
    print("• timestamp_sec: Unix timestamp in seconds (when measurement was taken)")
    print("• timestamp_nsec: Nanosecond precision for timestamp")
    print("• frame_id: Reference coordinate frame (camera_accel_optical_frame)")
    print("• orientation_x/y/z/w: Quaternion representing sensor orientation")
    print("• orientation_covariance_0-8: 3x3 covariance matrix for orientation uncertainty")
    print("• angular_velocity_x/y/z: Angular velocity in rad/s (rotation around each axis)")
    print("• angular_velocity_covariance_0-8: 3x3 covariance matrix for angular velocity uncertainty")
    print("• linear_acceleration_x/y/z: Linear acceleration in m/s² (movement along each axis)")
    print("• linear_acceleration_covariance_0-8: 3x3 covariance matrix for acceleration uncertainty")
    
    print("\n🧭 COORDINATE SYSTEM:")
    print("-" * 20)
    print("• X-axis: Forward direction (positive = forward acceleration)")
    print("• Y-axis: Left direction (positive = leftward acceleration)")
    print("• Z-axis: Up direction (positive = upward acceleration)")
    print("• Gravity typically shows as ~9.81 m/s² in the Z-axis when stationary")
    
    print("\n📊 TYPICAL VALUES:")
    print("-" * 15)
    print("• Stationary device: Z ≈ -9.81 m/s² (gravity), X,Y ≈ 0 m/s²")
    print("• Walking: ±2-3 m/s² in X,Y axes")
    print("• Running: ±5-10 m/s² in X,Y axes")
    print("• Vehicle acceleration: ±2-5 m/s²")
    print("• Angular velocity (stationary): ~0 rad/s")
    print("• Angular velocity (turning): ±0.1-1.0 rad/s")
    
    print("\n🚗 VEHICLE-SPECIFIC INTERPRETATION:")
    print("-" * 35)
    print("• Hard braking: Large negative X acceleration")
    print("• Acceleration: Large positive X acceleration")
    print("• Left turn: Positive Y acceleration")
    print("• Right turn: Negative Y acceleration")
    print("• Bumps/potholes: Sharp spikes in Z acceleration")
    print("• Smooth driving: Low variance in all axes")
    
    print("\n⚠️ DATA QUALITY INDICATORS:")
    print("-" * 25)
    print("• Covariance values: Lower = more reliable measurement")
    print("• Sudden spikes: May indicate sensor noise or actual events")
    print("• Consistent bias: May indicate sensor calibration needed")
    print("• Missing data: Check for gaps in timestamps")
    
    # Create labeled CSV files
    try:
        # Save labeled accelerometer data
        accel_data.to_csv('accel_labeled.csv', index=False)
        print(f"\n💾 Labeled accelerometer data saved as 'accel_labeled.csv'")
        
        # Save labeled gyroscope data
        gyro_data.to_csv('gyro_labeled.csv', index=False)
        print(f"💾 Labeled gyroscope data saved as 'gyro_labeled.csv'")
        
        # Save labeled sample accelerometer data
        sample_accel_data.to_csv('sample_accel_labeled.csv', index=False)
        print(f"💾 Labeled sample accelerometer data saved as 'sample_accel_labeled.csv'")
        
    except Exception as e:
        print(f"❌ Error saving labeled files: {e}")

if __name__ == "__main__":
    analyze_imu_data() 
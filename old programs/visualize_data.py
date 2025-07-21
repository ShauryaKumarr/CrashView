import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def analyze_data_files():
    """Analyze and visualize all vehicle data files"""
    
    # Define paths
    hardbrake_path = "raw data/hardbrake"
    suddenturn_path = "raw data/suddenTurn"
    
    print("="*80)
    print("VEHICLE DATA ANALYSIS REPORT")
    print("="*80)
    
    # Create a large figure with multiple subplots
    fig = plt.figure(figsize=(20, 24))
    
    # Define subplot positions
    plot_num = 1
    
    # ===== HARD BRAKE DATA ANALYSIS =====
    print("\n🚗 HARD BRAKE SCENARIO DATA:")
    print("-" * 50)
    
    # 1. GPS Velocity Data
    try:
        gps_file = os.path.join(hardbrake_path, "2025-06-02-16-45-55-vehicle-gps-vel.csv")
        gps_data = pd.read_csv(gps_file)
        
        print(f"📍 GPS Velocity Data:")
        print(f"   - Time range: {len(gps_data)} data points")
        print(f"   - Linear velocity components (x, y, z) in m/s")
        print(f"   - Angular velocity components (x, y, z) in rad/s")
        print(f"   - Max linear velocity: X={gps_data['.twist.linear.x'].max():.2f}, Y={gps_data['.twist.linear.y'].max():.2f}, Z={gps_data['.twist.linear.z'].max():.2f}")
        
        # Plot GPS velocity
        plt.subplot(6, 4, plot_num)
        plt.plot(gps_data.index, gps_data['.twist.linear.x'], 'r-', label='Linear X', linewidth=2)
        plt.plot(gps_data.index, gps_data['.twist.linear.y'], 'g-', label='Linear Y', linewidth=2)
        plt.plot(gps_data.index, gps_data['.twist.linear.z'], 'b-', label='Linear Z', linewidth=2)
        plt.title('Hard Brake: GPS Linear Velocity')
        plt.xlabel('Time Index')
        plt.ylabel('Velocity (m/s)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading GPS data: {e}")
    
    # 2. Brake Report Data
    try:
        brake_file = os.path.join(hardbrake_path, "2025-06-02-16-45-55-vehicle-brake_report.csv")
        brake_data = pd.read_csv(brake_file)
        
        print(f"\n🛑 Brake Report Data:")
        print(f"   - Time range: {len(brake_data)} data points")
        print(f"   - Brake pedal input/output (0-1 range)")
        print(f"   - Brake torque input/output")
        print(f"   - Max pedal input: {brake_data['.pedal_input'].max():.3f}")
        print(f"   - Max torque input: {brake_data['.torque_input'].max():.3f}")
        
        # Plot brake data
        plt.subplot(6, 4, plot_num)
        plt.plot(brake_data.index, brake_data['.pedal_input'], 'r-', label='Pedal Input', linewidth=2)
        plt.plot(brake_data.index, brake_data['.pedal_output'], 'b-', label='Pedal Output', linewidth=2)
        plt.title('Hard Brake: Brake Pedal')
        plt.xlabel('Time Index')
        plt.ylabel('Pedal Position (0-1)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
        plt.subplot(6, 4, plot_num)
        plt.plot(brake_data.index, brake_data['.torque_input'], 'r-', label='Torque Input', linewidth=2)
        plt.plot(brake_data.index, brake_data['.torque_output'], 'b-', label='Torque Output', linewidth=2)
        plt.title('Hard Brake: Brake Torque')
        plt.xlabel('Time Index')
        plt.ylabel('Torque (Nm)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading brake data: {e}")
    
    # 3. Throttle Report Data
    try:
        throttle_file = os.path.join(hardbrake_path, "2025-06-02-16-45-55-vehicle-throttle_report.csv")
        throttle_data = pd.read_csv(throttle_file)
        
        print(f"\n⚡ Throttle Report Data:")
        print(f"   - Time range: {len(throttle_data)} data points")
        print(f"   - Throttle pedal input/output (0-1 range)")
        print(f"   - Max pedal input: {throttle_data['.pedal_input'].max():.3f}")
        print(f"   - Min pedal input: {throttle_data['.pedal_input'].min():.3f}")
        
        # Plot throttle data
        plt.subplot(6, 4, plot_num)
        plt.plot(throttle_data.index, throttle_data['.pedal_input'], 'g-', label='Throttle Input', linewidth=2)
        plt.plot(throttle_data.index, throttle_data['.pedal_output'], 'orange', label='Throttle Output', linewidth=2)
        plt.title('Hard Brake: Throttle Pedal')
        plt.xlabel('Time Index')
        plt.ylabel('Pedal Position (0-1)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading throttle data: {e}")
    
    # 4. Steering Report Data
    try:
        steering_file = os.path.join(hardbrake_path, "2025-06-02-16-45-55-vehicle-steering_report.csv")
        steering_data = pd.read_csv(steering_file)
        
        print(f"\n🎛️ Steering Report Data:")
        print(f"   - Time range: {len(steering_data)} data points")
        print(f"   - Steering wheel angle in radians")
        print(f"   - Steering wheel command and torque")
        print(f"   - Max steering angle: {steering_data['.steering_wheel_angle'].max():.3f} rad")
        print(f"   - Min steering angle: {steering_data['.steering_wheel_angle'].min():.3f} rad")
        
        # Plot steering data
        plt.subplot(6, 4, plot_num)
        plt.plot(steering_data.index, np.degrees(steering_data['.steering_wheel_angle']), 'purple', label='Steering Angle', linewidth=2)
        plt.title('Hard Brake: Steering Wheel Angle')
        plt.xlabel('Time Index')
        plt.ylabel('Angle (degrees)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
        plt.subplot(6, 4, plot_num)
        plt.plot(steering_data.index, steering_data['.steering_wheel_torque'], 'brown', label='Steering Torque', linewidth=2)
        plt.title('Hard Brake: Steering Torque')
        plt.xlabel('Time Index')
        plt.ylabel('Torque (Nm)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading steering data: {e}")
    
    # 5. Wheel Speed Report Data
    try:
        wheel_file = os.path.join(hardbrake_path, "2025-06-02-16-45-55-vehicle-wheel_speed_report.csv")
        wheel_data = pd.read_csv(wheel_file)
        
        print(f"\n🔄 Wheel Speed Report Data:")
        print(f"   - Time range: {len(wheel_data)} data points")
        print(f"   - Individual wheel speeds for all 4 wheels (m/s)")
        print(f"   - Front Left max: {wheel_data['.front_left'].max():.2f} m/s")
        print(f"   - Front Right max: {wheel_data['.front_right'].max():.2f} m/s")
        print(f"   - Rear Left max: {wheel_data['.rear_left'].max():.2f} m/s")
        print(f"   - Rear Right max: {wheel_data['.rear_right'].max():.2f} m/s")
        
        # Plot wheel speeds
        plt.subplot(6, 4, plot_num)
        plt.plot(wheel_data.index, wheel_data['.front_left'], 'r-', label='Front Left', linewidth=2)
        plt.plot(wheel_data.index, wheel_data['.front_right'], 'b-', label='Front Right', linewidth=2)
        plt.plot(wheel_data.index, wheel_data['.rear_left'], 'g-', label='Rear Left', linewidth=2)
        plt.plot(wheel_data.index, wheel_data['.rear_right'], 'orange', label='Rear Right', linewidth=2)
        plt.title('Hard Brake: Wheel Speeds')
        plt.xlabel('Time Index')
        plt.ylabel('Speed (m/s)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading wheel speed data: {e}")
    
    # ===== SUDDEN TURN DATA ANALYSIS =====
    print("\n\n🌀 SUDDEN TURN SCENARIO DATA:")
    print("-" * 50)
    
    # 1. GPS Velocity Data - Sudden Turn
    try:
        gps_file_st = os.path.join(suddenturn_path, "2025-06-02-16-46-24-vehicle-gps-vel.csv")
        gps_data_st = pd.read_csv(gps_file_st)
        
        print(f"📍 GPS Velocity Data:")
        print(f"   - Time range: {len(gps_data_st)} data points")
        print(f"   - Max linear velocity: X={gps_data_st['.twist.linear.x'].max():.2f}, Y={gps_data_st['.twist.linear.y'].max():.2f}")
        
        # Plot GPS velocity - Sudden Turn
        plt.subplot(6, 4, plot_num)
        plt.plot(gps_data_st.index, gps_data_st['.twist.linear.x'], 'r-', label='Linear X', linewidth=2)
        plt.plot(gps_data_st.index, gps_data_st['.twist.linear.y'], 'g-', label='Linear Y', linewidth=2)
        plt.plot(gps_data_st.index, gps_data_st['.twist.linear.z'], 'b-', label='Linear Z', linewidth=2)
        plt.title('Sudden Turn: GPS Linear Velocity')
        plt.xlabel('Time Index')
        plt.ylabel('Velocity (m/s)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading GPS data: {e}")
    
    # 2. Brake Report Data - Sudden Turn
    try:
        brake_file_st = os.path.join(suddenturn_path, "2025-06-02-16-46-24-vehicle-brake_report.csv")
        brake_data_st = pd.read_csv(brake_file_st)
        
        print(f"\n🛑 Brake Report Data:")
        print(f"   - Time range: {len(brake_data_st)} data points")
        print(f"   - Max pedal input: {brake_data_st['.pedal_input'].max():.3f}")
        
        # Plot brake data - Sudden Turn
        plt.subplot(6, 4, plot_num)
        plt.plot(brake_data_st.index, brake_data_st['.pedal_input'], 'r-', label='Pedal Input', linewidth=2)
        plt.plot(brake_data_st.index, brake_data_st['.pedal_output'], 'b-', label='Pedal Output', linewidth=2)
        plt.title('Sudden Turn: Brake Pedal')
        plt.xlabel('Time Index')
        plt.ylabel('Pedal Position (0-1)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading brake data: {e}")
    
    # 3. Throttle Report Data - Sudden Turn
    try:
        throttle_file_st = os.path.join(suddenturn_path, "2025-06-02-16-46-24-vehicle-throttle_report.csv")
        throttle_data_st = pd.read_csv(throttle_file_st)
        
        print(f"\n⚡ Throttle Report Data:")
        print(f"   - Time range: {len(throttle_data_st)} data points")
        print(f"   - Max pedal input: {throttle_data_st['.pedal_input'].max():.3f}")
        
        # Plot throttle data - Sudden Turn
        plt.subplot(6, 4, plot_num)
        plt.plot(throttle_data_st.index, throttle_data_st['.pedal_input'], 'g-', label='Throttle Input', linewidth=2)
        plt.plot(throttle_data_st.index, throttle_data_st['.pedal_output'], 'orange', label='Throttle Output', linewidth=2)
        plt.title('Sudden Turn: Throttle Pedal')
        plt.xlabel('Time Index')
        plt.ylabel('Pedal Position (0-1)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading throttle data: {e}")
    
    # 4. Steering Report Data - Sudden Turn
    try:
        steering_file_st = os.path.join(suddenturn_path, "2025-06-02-16-46-24-vehicle-steering_report.csv")
        steering_data_st = pd.read_csv(steering_file_st)
        
        print(f"\n🎛️ Steering Report Data:")
        print(f"   - Time range: {len(steering_data_st)} data points")
        print(f"   - Max steering angle: {steering_data_st['.steering_wheel_angle'].max():.3f} rad")
        print(f"   - Min steering angle: {steering_data_st['.steering_wheel_angle'].min():.3f} rad")
        
        # Plot steering data - Sudden Turn
        plt.subplot(6, 4, plot_num)
        plt.plot(steering_data_st.index, np.degrees(steering_data_st['.steering_wheel_angle']), 'purple', label='Steering Angle', linewidth=2)
        plt.title('Sudden Turn: Steering Wheel Angle')
        plt.xlabel('Time Index')
        plt.ylabel('Angle (degrees)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
        plt.subplot(6, 4, plot_num)
        plt.plot(steering_data_st.index, steering_data_st['.steering_wheel_torque'], 'brown', label='Steering Torque', linewidth=2)
        plt.title('Sudden Turn: Steering Torque')
        plt.xlabel('Time Index')
        plt.ylabel('Torque (Nm)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading steering data: {e}")
    
    # 5. Wheel Speed Report Data - Sudden Turn
    try:
        wheel_file_st = os.path.join(suddenturn_path, "2025-06-02-16-46-24-vehicle-wheel_speed_report.csv")
        wheel_data_st = pd.read_csv(wheel_file_st)
        
        print(f"\n🔄 Wheel Speed Report Data:")
        print(f"   - Time range: {len(wheel_data_st)} data points")
        print(f"   - Front Left max: {wheel_data_st['.front_left'].max():.2f} m/s")
        print(f"   - Front Right max: {wheel_data_st['.front_right'].max():.2f} m/s")
        print(f"   - Rear Left max: {wheel_data_st['.rear_left'].max():.2f} m/s")
        print(f"   - Rear Right max: {wheel_data_st['.rear_right'].max():.2f} m/s")
        
        # Plot wheel speeds - Sudden Turn
        plt.subplot(6, 4, plot_num)
        plt.plot(wheel_data_st.index, wheel_data_st['.front_left'], 'r-', label='Front Left', linewidth=2)
        plt.plot(wheel_data_st.index, wheel_data_st['.front_right'], 'b-', label='Front Right', linewidth=2)
        plt.plot(wheel_data_st.index, wheel_data_st['.rear_left'], 'g-', label='Rear Left', linewidth=2)
        plt.plot(wheel_data_st.index, wheel_data_st['.rear_right'], 'orange', label='Rear Right', linewidth=2)
        plt.title('Sudden Turn: Wheel Speeds')
        plt.xlabel('Time Index')
        plt.ylabel('Speed (m/s)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
        
    except Exception as e:
        print(f"   ❌ Error reading wheel speed data: {e}")
    
    # Add remaining subplots for comparison charts
    # Comparison plot - Steering angles
    try:
        plt.subplot(6, 4, plot_num)
        plt.plot(np.degrees(steering_data['.steering_wheel_angle']), 'b-', label='Hard Brake', linewidth=2, alpha=0.7)
        plt.plot(np.degrees(steering_data_st['.steering_wheel_angle']), 'r-', label='Sudden Turn', linewidth=2, alpha=0.7)
        plt.title('Comparison: Steering Angles')
        plt.xlabel('Time Index')
        plt.ylabel('Angle (degrees)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
    except:
        pass
    
    # Comparison plot - Vehicle speeds (average of all wheels)
    try:
        plt.subplot(6, 4, plot_num)
        avg_speed_hb = (wheel_data['.front_left'] + wheel_data['.front_right'] + 
                       wheel_data['.rear_left'] + wheel_data['.rear_right']) / 4
        avg_speed_st = (wheel_data_st['.front_left'] + wheel_data_st['.front_right'] + 
                       wheel_data_st['.rear_left'] + wheel_data_st['.rear_right']) / 4
        
        plt.plot(avg_speed_hb, 'b-', label='Hard Brake', linewidth=2, alpha=0.7)
        plt.plot(avg_speed_st, 'r-', label='Sudden Turn', linewidth=2, alpha=0.7)
        plt.title('Comparison: Average Vehicle Speed')
        plt.xlabel('Time Index')
        plt.ylabel('Speed (m/s)')
        plt.legend()
        plt.grid(True)
        plot_num += 1
    except:
        pass
    
    # Summary Statistics Plot
    try:
        plt.subplot(6, 4, plot_num)
        scenarios = ['Hard Brake', 'Sudden Turn']
        max_speeds = [avg_speed_hb.max(), avg_speed_st.max()]
        max_brake = [brake_data['.pedal_input'].max(), brake_data_st['.pedal_input'].max()]
        
        x = np.arange(len(scenarios))
        width = 0.35
        
        plt.bar(x - width/2, max_speeds, width, label='Max Speed (m/s)', alpha=0.8)
        plt.bar(x + width/2, [b*10 for b in max_brake], width, label='Max Brake (x10)', alpha=0.8)
        
        plt.title('Scenario Comparison')
        plt.xlabel('Scenarios')
        plt.ylabel('Values')
        plt.xticks(x, scenarios)
        plt.legend()
        plt.grid(True)
        plot_num += 1
    except:
        pass
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('vehicle_data_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*80)
    print("SUMMARY OF VEHICLE DATA FILES:")
    print("="*80)
    
    print("\n📊 DATA FILE DESCRIPTIONS:")
    print("1. 📍 GPS Velocity Files:")
    print("   - Contains linear velocity (x, y, z) and angular velocity components")
    print("   - Used to track vehicle motion and orientation changes")
    
    print("\n2. 🛑 Brake Report Files:")
    print("   - Contains brake pedal input/output positions (0-1 scale)")
    print("   - Contains brake torque input/output values")
    print("   - Includes safety status flags and fault indicators")
    
    print("\n3. ⚡ Throttle Report Files:")
    print("   - Contains throttle pedal input/output positions (0-1 scale)")
    print("   - Tracks acceleration commands and responses")
    print("   - Includes driver/autonomous mode indicators")
    
    print("\n4. 🎛️ Steering Report Files:")
    print("   - Contains steering wheel angle in radians")
    print("   - Contains steering wheel torque and commands")
    print("   - Tracks vehicle direction control")
    
    print("\n5. 🔄 Wheel Speed Report Files:")
    print("   - Contains individual wheel speeds for all 4 wheels")
    print("   - Used for traction control and vehicle dynamics analysis")
    print("   - Higher frequency data (more samples per second)")
    
    print("\n🎯 KEY INSIGHTS:")
    print("- Hard Brake scenario shows rapid deceleration patterns")
    print("- Sudden Turn scenario shows significant steering angle changes")
    print("- Wheel speed data has the highest temporal resolution")
    print("- All sensors are synchronized with timestamps")
    print("- Data can be used for vehicle dynamics analysis and safety research")
    
    print(f"\n📈 Visualization saved as: vehicle_data_analysis.png")
    print("="*80)

if __name__ == "__main__":
    analyze_data_files()
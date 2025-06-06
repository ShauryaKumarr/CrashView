# Vehicle Data Analysis Summary

## Overview
This document provides a comprehensive analysis of vehicle sensor data from two different driving scenarios: **Hard Brake** and **Sudden Turn**. The data was collected from multiple vehicle sensors and contains information about vehicle dynamics, control inputs, and responses.

## Data Files Description

### 📍 GPS Velocity Files (`*-gps-vel.csv`)
**Purpose**: Tracks vehicle motion and orientation in 3D space
- **Linear Velocity Components**: 
  - `.twist.linear.x` - Forward/backward velocity (m/s)
  - `.twist.linear.y` - Left/right velocity (m/s) 
  - `.twist.linear.z` - Up/down velocity (m/s)
- **Angular Velocity Components**:
  - `.twist.angular.x` - Roll rate (rad/s)
  - `.twist.angular.y` - Pitch rate (rad/s)
  - `.twist.angular.z` - Yaw rate (rad/s)

### 🛑 Brake Report Files (`*-brake_report.csv`)
**Purpose**: Monitors brake system input, output, and safety status
- **Key Columns**:
  - `.pedal_input` - Driver brake pedal position (0-1 scale)
  - `.pedal_output` - Actual brake pedal response (0-1 scale)
  - `.torque_input` - Brake torque command (Nm)
  - `.torque_output` - Actual brake torque applied (Nm)
  - Safety flags: `.enabled`, `.override`, `.driver`, `.timeout`
  - Fault indicators: `.fault_wdc`, `.fault_ch1`, `.fault_ch2`, `.fault_power`

### ⚡ Throttle Report Files (`*-throttle_report.csv`)
**Purpose**: Tracks acceleration commands and responses
- **Key Columns**:
  - `.pedal_input` - Driver throttle pedal position (0-1 scale)
  - `.pedal_output` - Actual throttle response (0-1 scale)
  - Control flags: `.enabled`, `.override`, `.driver`, `.timeout`
  - Fault monitoring: `.fault_wdc`, `.fault_ch1`, `.fault_ch2`, `.fault_power`

### 🎛️ Steering Report Files (`*-steering_report.csv`)
**Purpose**: Monitors steering wheel input and vehicle direction control
- **Key Columns**:
  - `.steering_wheel_angle` - Steering wheel angle (radians)
  - `.steering_wheel_cmd` - Steering command (radians)
  - `.steering_wheel_torque` - Steering torque (Nm)
  - `.speed` - Vehicle speed (m/s)
  - Safety flags and fault indicators

### 🔄 Wheel Speed Report Files (`*-wheel_speed_report.csv`)
**Purpose**: Individual wheel speed monitoring for traction control and dynamics analysis
- **Key Columns**:
  - `.front_left` - Front left wheel speed (m/s)
  - `.front_right` - Front right wheel speed (m/s)
  - `.rear_left` - Rear left wheel speed (m/s)
  - `.rear_right` - Rear right wheel speed (m/s)

## Scenario Analysis

### 🚗 Hard Brake Scenario (2025-06-02-16-45-55)
**Characteristics:**
- **Duration**: Approximately 4 seconds of data
- **Max Vehicle Speed**: ~30 m/s (~67 mph)
- **Brake Intensity**: High pedal input (up to 34.7%)
- **Throttle Behavior**: Gradual reduction from 49.9% to 15.9%
- **Steering**: Minimal steering input (mostly straight driving)
- **Key Insight**: Demonstrates emergency braking behavior with rapid deceleration

**Data Points:**
- GPS Velocity: 16 samples
- Brake Report: 882 samples  
- Throttle Report: 881 samples
- Steering Report: 881 samples
- Wheel Speed: 1,764 samples (highest frequency)

### 🌀 Sudden Turn Scenario (2025-06-02-16-46-24)
**Characteristics:**
- **Duration**: Approximately 2.8 seconds of data
- **Max Vehicle Speed**: ~20 m/s (~45 mph)
- **Steering Range**: Extreme steering angles from -4.16 to +8.33 radians
- **Brake Usage**: Moderate braking (up to 24.5%)
- **Throttle**: Significant throttle input (up to 43.3%)
- **Key Insight**: Demonstrates aggressive steering maneuver with vehicle control

**Data Points:**
- GPS Velocity: 12 samples
- Brake Report: 567 samples
- Throttle Report: 567 samples
- Steering Report: 567 samples
- Wheel Speed: 1,136 samples

## Key Findings

### 📊 Data Frequency Analysis
1. **Wheel Speed Reports**: Highest frequency (~50 Hz) - Critical for real-time control
2. **Brake/Throttle/Steering Reports**: Medium frequency (~20 Hz) - Adequate for control loops
3. **GPS Velocity**: Lowest frequency (~4 Hz) - Sufficient for navigation

### 🔍 Safety Observations
1. **Hard Brake Scenario**:
   - All wheels decelerate uniformly (good ABS performance)
   - Steering remains stable during braking
   - No fault conditions detected
   
2. **Sudden Turn Scenario**:
   - Significant steering angle changes indicate emergency maneuver
   - Speed differential between left/right wheels shows turning dynamics
   - Coordinated throttle and brake usage for vehicle control

### 📈 Vehicle Dynamics Insights
1. **Speed Consistency**: Wheel speeds track well together in normal conditions
2. **Response Times**: Input-output delays are minimal across all systems
3. **System Integration**: All subsystems work coordinately during maneuvers

## Technical Specifications

### Data Collection Setup
- **Vehicle Type**: Autonomous/connected vehicle with full sensor suite
- **Sampling Rates**: Variable by sensor type (4-50 Hz)
- **Precision**: High-precision timestamps and floating-point measurements
- **Safety Systems**: Comprehensive fault monitoring and redundancy

### File Formats
- **Format**: CSV with comma separation
- **Timestamps**: Unix timestamp format with nanosecond precision
- **Headers**: ROS-style message field naming convention
- **Size**: Ranges from 1.4KB (GPS) to 219KB (wheel speeds)

## Applications

This data is valuable for:
- 🚗 **Autonomous Vehicle Development**: Understanding vehicle behavior in critical scenarios
- 🔬 **Safety Research**: Analyzing emergency response patterns
- 📊 **Performance Analysis**: Evaluating control system effectiveness  
- 🛡️ **Fault Detection**: Developing diagnostic algorithms
- 📚 **Machine Learning**: Training models for prediction and control

## Visualization Output

The analysis generates comprehensive graphs showing:
- Time-series plots for all sensor data
- Comparison between scenarios
- Multi-channel sensor correlation
- Statistical summaries and key metrics

**Generated File**: `vehicle_data_analysis.png` (1.5MB visualization)

---
*Analysis completed on vehicle sensor data from CAR Lab Research dataset* 
import pandas as pd
import os

def clean_data_files():
    # Define paths
    hard_brake_path = "cleaned data/hard brake"
    sudden_turn_path = "cleaned data/suddenturn"
    
    # Helper to select only existing columns
    def select_existing(df, columns):
        return df[[col for col in columns if col in df.columns]]

    # Process hard brake data
    for filename in os.listdir(hard_brake_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(hard_brake_path, filename)
            df = pd.read_csv(file_path)
            
            # Keep only important columns based on file type
            if 'gps-vel' in filename:
                df = select_existing(df, ['time', '.twist.linear.x', '.twist.linear.y', '.twist.linear.z'])
            elif 'brake_report' in filename:
                df = select_existing(df, ['time', '.pedal_input', '.pedal_output', '.torque_input', '.torque_output'])
            elif 'throttle_report' in filename:
                df = select_existing(df, ['time', '.pedal_input', '.pedal_output'])
            elif 'steering_report' in filename:
                df = select_existing(df, ['time', '.steering_wheel_angle', '.steering_wheel_cmd'])
            elif 'wheel_speed_report' in filename:
                df = select_existing(df, ['time', '.wheel_speed_fl', '.wheel_speed_fr', '.wheel_speed_rl', '.wheel_speed_rr'])
            
            # Save cleaned data
            df.to_csv(file_path, index=False)
    
    # Process sudden turn data
    for filename in os.listdir(sudden_turn_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(sudden_turn_path, filename)
            df = pd.read_csv(file_path)
            
            # Keep only important columns based on file type
            if 'gps-vel' in filename:
                df = select_existing(df, ['time', '.twist.linear.x', '.twist.linear.y', '.twist.linear.z'])
            elif 'brake_report' in filename:
                df = select_existing(df, ['time', '.pedal_input', '.pedal_output', '.torque_input', '.torque_output'])
            elif 'throttle_report' in filename:
                df = select_existing(df, ['time', '.pedal_input', '.pedal_output'])
            elif 'steering_report' in filename:
                df = select_existing(df, ['time', '.steering_wheel_angle', '.steering_wheel_cmd'])
            elif 'wheel_speed_report' in filename:
                df = select_existing(df, ['time', '.wheel_speed_fl', '.wheel_speed_fr', '.wheel_speed_rl', '.wheel_speed_rr'])
            
            # Save cleaned data
            df.to_csv(file_path, index=False)

if __name__ == "__main__":
    clean_data_files() 
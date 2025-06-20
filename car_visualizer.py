import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
from scipy.spatial.transform import Rotation
import warnings
warnings.filterwarnings('ignore')

class CarVisualizer:
    def __init__(self, gyro_file='gyro_processed.csv', accel_file='accel_processed.csv'):
        """Initialize the car visualizer with sensor data files."""
        self.gyro_data = pd.read_csv(gyro_file)
        self.accel_data = pd.read_csv(accel_file)
        
        # Calculate orientation over time
        self.orientation_data = self._calculate_orientation()
        
        # Detect crash events
        self.crash_events = self._detect_crash_events()
        
        # Create car model
        self.car_vertices, self.car_faces = self._create_car_model()
        
    def _calculate_orientation(self):
        """Calculate cumulative orientation from gyroscope data."""
        dt = np.diff(self.gyro_data['time_combined'])
        dt = np.insert(dt, 0, 0)
        
        # Cumulative rotation
        orientation = {
            'roll': np.cumsum(self.gyro_data['gyro_x'] * dt),
            'pitch': np.cumsum(self.gyro_data['gyro_y'] * dt),
            'yaw': np.cumsum(self.gyro_data['gyro_z'] * dt),
            'time': self.gyro_data['time_combined']
        }
        
        return orientation
    
    def _detect_crash_events(self):
        """Detect potential crash events based on sensor data."""
        events = []
        
        # Detect sudden changes in gyroscope readings
        gyro_magnitude = np.sqrt(
            self.gyro_data['gyro_x']**2 + 
            self.gyro_data['gyro_y']**2 + 
            self.gyro_data['gyro_z']**2
        )
        
        # Find peaks in gyroscope magnitude
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(gyro_magnitude, height=0.5, distance=50)
        
        for peak in peaks:
            events.append({
                'time': self.gyro_data['time_combined'].iloc[peak],
                'type': 'sudden_rotation',
                'magnitude': gyro_magnitude[peak],
                'index': peak
            })
        
        # Detect extreme orientation changes
        roll_threshold = np.pi/2  # 90 degrees
        pitch_threshold = np.pi/2
        
        for i, (roll, pitch) in enumerate(zip(self.orientation_data['roll'], self.orientation_data['pitch'])):
            if abs(roll) > roll_threshold or abs(pitch) > pitch_threshold:
                events.append({
                    'time': self.orientation_data['time'][i],
                    'type': 'extreme_orientation',
                    'roll': roll,
                    'pitch': pitch,
                    'index': i
                })
        
        return sorted(events, key=lambda x: x['time'])
    
    def _create_car_model(self):
        """Create a simple 3D car model."""
        # Car dimensions
        length, width, height = 4, 2, 1.5
        
        # Define car vertices (simplified car shape)
        vertices = np.array([
            # Body (bottom)
            [-length/2, -width/2, 0],    # 0
            [length/2, -width/2, 0],     # 1
            [length/2, width/2, 0],      # 2
            [-length/2, width/2, 0],     # 3
            
            # Body (top)
            [-length/2, -width/2, height],    # 4
            [length/2, -width/2, height],     # 5
            [length/2, width/2, height],      # 6
            [-length/2, width/2, height],     # 7
            
            # Hood (front)
            [length/2, -width/2, height/3],   # 8
            [length/2 + 0.5, -width/2, height/3],  # 9
            [length/2 + 0.5, width/2, height/3],   # 10
            [length/2, width/2, height/3],    # 11
            
            # Trunk (back)
            [-length/2, -width/2, height/3],  # 12
            [-length/2 - 0.3, -width/2, height/3], # 13
            [-length/2 - 0.3, width/2, height/3],  # 14
            [-length/2, width/2, height/3],   # 15
            
            # Wheels
            [length/3, -width/2 - 0.3, 0.3],  # 16 (front left)
            [length/3, width/2 + 0.3, 0.3],   # 17 (front right)
            [-length/3, -width/2 - 0.3, 0.3], # 18 (back left)
            [-length/3, width/2 + 0.3, 0.3],  # 19 (back right)
        ])
        
        # Define faces (triangles and quads)
        faces = [
            # Body faces
            [0, 1, 2, 3],  # bottom
            [4, 7, 6, 5],  # top
            [0, 4, 5, 1],  # front
            [2, 6, 7, 3],  # back
            [0, 3, 7, 4],  # left
            [1, 5, 6, 2],  # right
            
            # Hood faces
            [8, 9, 10, 11],
            [8, 11, 6, 5],
            [9, 8, 5, 6],
            [10, 9, 6, 11],
            
            # Trunk faces
            [12, 15, 14, 13],
            [12, 13, 7, 4],
            [13, 14, 7, 4],
            [14, 15, 7, 4],
            
            # Wheel faces (simplified as rectangles)
            [16, 17, 18, 19],  # front wheels
        ]
        
        return vertices, faces
    
    def _rotate_car(self, vertices, roll, pitch, yaw):
        """Apply rotation to car vertices."""
        # Create rotation matrix
        r = Rotation.from_euler('xyz', [roll, pitch, yaw])
        rotation_matrix = r.as_matrix()
        
        # Apply rotation to all vertices
        rotated_vertices = np.dot(vertices, rotation_matrix.T)
        
        return rotated_vertices
    
    def _draw_car(self, ax, vertices, color='blue', alpha=0.8):
        """Draw the car model."""
        # Create polygons for each face
        polygons = []
        for face in self.car_faces:
            face_vertices = [vertices[i] for i in face]
            polygons.append(face_vertices)
        
        # Create 3D polygon collection
        poly3d = Poly3DCollection(polygons, alpha=alpha, facecolor=color, edgecolor='black')
        ax.add_collection3d(poly3d)
        
        # Draw wheels as spheres
        wheel_positions = [16, 17, 18, 19]
        for wheel_idx in wheel_positions:
            wheel_center = vertices[wheel_idx]
            # Draw wheel as a small sphere
            u = np.linspace(0, 2 * np.pi, 8)
            v = np.linspace(0, np.pi, 8)
            radius = 0.3
            x = wheel_center[0] + radius * np.outer(np.cos(u), np.sin(v))
            y = wheel_center[1] + radius * np.outer(np.sin(u), np.sin(v))
            z = wheel_center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
            ax.plot_surface(x, y, z, color='black', alpha=0.7)
    
    def create_car_animation(self, start_time=None, end_time=None, interval=50):
        """Create an animated visualization of the car moving."""
        if start_time is None:
            start_time = self.gyro_data['time_combined'].min()
        if end_time is None:
            end_time = self.gyro_data['time_combined'].max()
        
        # Filter data by time range
        mask = (self.gyro_data['time_combined'] >= start_time) & (self.gyro_data['time_combined'] <= end_time)
        orientation_filtered = {k: v[mask] for k, v in self.orientation_data.items()}
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Set consistent axis limits
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(-1, 3)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Add ground plane
        ground_x = np.array([[-3, -3], [3, 3]])
        ground_y = np.array([[-3, 3], [-3, 3]])
        ground_z = np.array([[0, 0], [0, 0]])
        ax.plot_surface(ground_x, ground_y, ground_z, alpha=0.3, color='gray')
        
        def animate(frame):
            ax.clear()
            
            # Set consistent axis limits
            ax.set_xlim(-3, 3)
            ax.set_ylim(-3, 3)
            ax.set_zlim(-1, 3)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f'Car Motion Simulation - Time: {orientation_filtered["time"][frame]:.2f}s')
            
            # Add ground plane
            ax.plot_surface(ground_x, ground_y, ground_z, alpha=0.3, color='gray')
            
            # Get current orientation
            roll = orientation_filtered['roll'][frame]
            pitch = orientation_filtered['pitch'][frame]
            yaw = orientation_filtered['yaw'][frame]
            
            # Rotate car
            rotated_vertices = self._rotate_car(self.car_vertices, roll, pitch, yaw)
            
            # Check if this is a crash event
            current_time = orientation_filtered['time'][frame]
            is_crash_event = False
            crash_type = ""
            
            for event in self.crash_events:
                if abs(event['time'] - current_time) < 0.1:  # Within 0.1 seconds
                    is_crash_event = True
                    crash_type = event['type']
                    break
            
            # Draw car with appropriate color
            if is_crash_event:
                if crash_type == 'sudden_rotation':
                    color = 'red'
                    ax.text2D(0.02, 0.98, '🚨 SUDDEN ROTATION DETECTED!', 
                             transform=ax.transAxes, fontsize=14, color='red', weight='bold')
                elif crash_type == 'extreme_orientation':
                    color = 'purple'
                    ax.text2D(0.02, 0.98, '🚨 EXTREME ORIENTATION DETECTED!', 
                             transform=ax.transAxes, fontsize=14, color='purple', weight='bold')
                else:
                    color = 'orange'
                    ax.text2D(0.02, 0.98, '🚨 CRASH EVENT DETECTED!', 
                             transform=ax.transAxes, fontsize=14, color='orange', weight='bold')
            else:
                color = 'blue'
            
            self._draw_car(ax, rotated_vertices, color=color)
            
            # Add orientation info
            ax.text2D(0.02, 0.92, f'Roll: {np.degrees(roll):.1f}°', 
                     transform=ax.transAxes, fontsize=10)
            ax.text2D(0.02, 0.88, f'Pitch: {np.degrees(pitch):.1f}°', 
                     transform=ax.transAxes, fontsize=10)
            ax.text2D(0.02, 0.84, f'Yaw: {np.degrees(yaw):.1f}°', 
                     transform=ax.transAxes, fontsize=10)
        
        frames = len(orientation_filtered['time'])
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=interval, repeat=True)
        
        return anim
    
    def create_static_car_views(self, time_points=None):
        """Create static views of the car at specific time points."""
        if time_points is None:
            # Show car at key moments
            time_points = [1.0, 20.0, 40.0, 60.0, 84.4, 84.6]  # Key moments including crash events
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw={'projection': '3d'})
        axes = axes.flatten()
        
        for i, time_point in enumerate(time_points):
            ax = axes[i]
            
            # Find closest time index
            time_idx = np.argmin(np.abs(self.orientation_data['time'] - time_point))
            
            # Get orientation at this time
            roll = self.orientation_data['roll'][time_idx]
            pitch = self.orientation_data['pitch'][time_idx]
            yaw = self.orientation_data['yaw'][time_idx]
            
            # Check if this is a crash event
            is_crash_event = False
            for event in self.crash_events:
                if abs(event['time'] - time_point) < 0.1:
                    is_crash_event = True
                    break
            
            # Set view
            ax.set_xlim(-3, 3)
            ax.set_ylim(-3, 3)
            ax.set_zlim(-1, 3)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            
            # Add ground plane
            ground_x = np.array([[-3, -3], [3, 3]])
            ground_y = np.array([[-3, 3], [-3, 3]])
            ground_z = np.array([[0, 0], [0, 0]])
            ax.plot_surface(ground_x, ground_y, ground_z, alpha=0.3, color='gray')
            
            # Rotate and draw car
            rotated_vertices = self._rotate_car(self.car_vertices, roll, pitch, yaw)
            color = 'red' if is_crash_event else 'blue'
            self._draw_car(ax, rotated_vertices, color=color)
            
            # Set title
            title = f'Time: {time_point:.1f}s'
            if is_crash_event:
                title += ' 🚨 CRASH EVENT!'
            ax.set_title(title, fontsize=12)
            
            # Add orientation info
            ax.text2D(0.02, 0.95, f'Roll: {np.degrees(roll):.1f}°', 
                     transform=ax.transAxes, fontsize=8)
            ax.text2D(0.02, 0.90, f'Pitch: {np.degrees(pitch):.1f}°', 
                     transform=ax.transAxes, fontsize=8)
            ax.text2D(0.02, 0.85, f'Yaw: {np.degrees(yaw):.1f}°', 
                     transform=ax.transAxes, fontsize=8)
        
        plt.tight_layout()
        return fig
    
    def print_crash_summary(self):
        """Print a summary of detected crash events."""
        print("=== CAR CRASH EVENT DETECTION SUMMARY ===")
        print(f"Total events detected: {len(self.crash_events)}")
        print()
        
        for i, event in enumerate(self.crash_events, 1):
            print(f"Event {i}:")
            print(f"  Time: {event['time']:.2f} seconds")
            print(f"  Type: {event['type']}")
            if 'magnitude' in event:
                print(f"  Magnitude: {event['magnitude']:.3f}")
            if 'roll' in event:
                print(f"  Roll: {event['roll']:.3f} rad ({np.degrees(event['roll']):.1f}°)")
                print(f"  Pitch: {event['pitch']:.3f} rad ({np.degrees(event['pitch']):.1f}°)")
            print()

def main():
    """Main function to run the car visualizer."""
    print("Loading car motion data...")
    visualizer = CarVisualizer()
    
    print("Detecting crash events...")
    visualizer.print_crash_summary()
    
    # Create static views of key moments
    print("\nCreating static car views...")
    fig_static = visualizer.create_static_car_views()
    plt.savefig('car_static_views.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create animation of the most interesting period (around crash events)
    print("\nCreating car animation around crash events...")
    anim = visualizer.create_car_animation(start_time=84.0, end_time=85.0, interval=100)
    
    # Save animation
    print("Saving animation...")
    anim.save('car_animation.gif', writer='pillow', fps=10)
    
    print("\nVisualization complete!")
    print("Files created:")
    print("- car_static_views.png: Static views of car at key moments")
    print("- car_animation.gif: Animated car motion (84-85 seconds)")
    print("\nCrash Detection Summary:")
    print("🔴 Red car = Crash event detected")
    print("🔵 Blue car = Normal motion")
    print("🚨 Text alerts appear during crash events")

if __name__ == "__main__":
    main() 
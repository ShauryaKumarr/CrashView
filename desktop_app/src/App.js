import React, { useState, useEffect } from 'react';
import './App.css';
import GyroSimulator from './components/GyroSimulator';

function App() {
  const [gyroData, setGyroData] = useState({ x: 0, y: 0, z: 0 });

  // Simulate gyroscope orientation updates (replace with real sensor integration)
  useEffect(() => {
    const interval = setInterval(() => {
      setGyroData(prev => ({
        x: (prev.x + 1) % 360,
        y: (prev.y + 0.7) % 360,
        z: (prev.z + 0.5) % 360,
      }));
    }, 100);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      {/* Top Bar */}
      <header className="App-header">
        <h1>AutoRec Black Box</h1>
        <div className="connection-controls">
          <button className="connect-btn">🔗 Connect to Arduino</button>
          <div className="status-indicator">
            <div className="status-dot disconnected"></div>
            <span className="status-label">Disconnected</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="main-content">
        {/* Left Panel: Sensor Readings */}
        <div className="panel sensor-panel">
          <h3>📊 Live Sensor Data</h3>
          <div className="sensor-group">
            <h4>IMU Readings</h4>
            <div className="sensor-item">
              <span>Acceleration X:</span>
              <span className="sensor-value">--- m/s²</span>
            </div>
            <div className="sensor-item">
              <span>Acceleration Y:</span>
              <span className="sensor-value">--- m/s²</span>
            </div>
            <div className="sensor-item">
              <span>Acceleration Z:</span>
              <span className="sensor-value">--- m/s²</span>
            </div>
            <div className="sensor-item">
              <span>Gyroscope X:</span>
              <span className="sensor-value">--- °/s</span>
            </div>
            <div className="sensor-item">
              <span>Gyroscope Y:</span>
              <span className="sensor-value">--- °/s</span>
            </div>
            <div className="sensor-item">
              <span>Gyroscope Z:</span>
              <span className="sensor-value">--- °/s</span>
            </div>
          </div>
          <div className="sensor-group">
            <h4>Ultrasound</h4>
            <div className="sensor-item">
              <span>Distance:</span>
              <span className="sensor-value">--- cm</span>
            </div>
          </div>
        </div>

        {/* Center: Visualization Area */}
        <div className="panel viz-panel">
          <h3>🚗 Vehicle Orientation</h3>
          {/* Gyroscope orientation simulation */}
          <GyroSimulator gyroData={gyroData} />
        </div>

        {/* Right Panel: Event Log */}
        <div className="panel log-panel">
          <h3>📝 Event Log</h3>
          <div className="log-text">
            <div className="log-entry">System initialized</div>
            <div className="log-entry">Waiting for Arduino connection...</div>
          </div>
        </div>
      </div>

      {/* Bottom Bar: Status and Controls */}
      <footer className="App-footer">
        <div className="logging-status">
          <div className="logging-indicator">
            <div className="logging-dot inactive"></div>
            <span>Auto-Logging: Ready</span>
          </div>
        </div>
        <button className="stop-btn">🛑 Stop Logging</button>
        <div className="footer-info">
          <span>Last event: None</span>
        </div>
      </footer>
    </div>
  );
}

export default App;

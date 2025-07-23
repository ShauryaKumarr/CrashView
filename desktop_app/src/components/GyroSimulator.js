import React from 'react';

export default function GyroSimulator({ gyroData }) {
  return (
    <div className="gyro-container">
      <div
        className="gyro-cube"
        style={{
          transform: `rotateX(${gyroData.x}deg) rotateY(${gyroData.y}deg) rotateZ(${gyroData.z}deg)`
        }}
      >
        <div className="face front" />
        <div className="face back" />
        <div className="face right" />
        <div className="face left" />
        <div className="face top" />
        <div className="face bottom" />
      </div>
    </div>
  );
} 
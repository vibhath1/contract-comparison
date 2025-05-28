// components/GradientBackground.tsx
import React, { useState, useEffect, useRef } from 'react';

interface MousePosition {
  x: number;
  y: number;
}

const GradientBackground: React.FC = () => {
  const [mousePosition, setMousePosition] = useState<MousePosition>({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
  const [smoothMousePosition, setSmoothMousePosition] = useState<MousePosition>({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
  const requestRef = useRef<number | null>(null);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: e.clientX,
        y: e.clientY + window.scrollY
      });
    };

    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  // Smooth animation using requestAnimationFrame
  useEffect(() => {
    const animate = () => {
      setSmoothMousePosition((prev) => ({
        x: prev.x + (mousePosition.x - prev.x) * 0.1,
        y: prev.y + (mousePosition.y - prev.y) * 0.1
      }));
      requestRef.current = requestAnimationFrame(animate);
    };

    requestRef.current = requestAnimationFrame(animate);

    return () => {
      if (requestRef.current !== null) {
        cancelAnimationFrame(requestRef.current);
      }
    };
  }, [mousePosition]);

  return (
    <div className="fixed inset-0 w-full h-full pointer-events-none overflow-hidden">
      {/* Static base gradient - always visible */}
      {/*<div 
        className="absolute inset-0 w-full h-full"
        style={{
          background: `
            radial-gradient(
              ellipse 1000px 700px at 40% 40%,
              rgba(255, 102, 0, 0.5) 0%,
              rgba(255, 80, 0, 0.3) 20%,
              rgba(204, 51, 0, 0.2) 35%,
              rgba(102, 20, 0, 0.1) 50%,
              rgba(51, 10, 0, 0.05) 65%,
              transparent 80%
            )
          `,
          filter: 'blur(80px)',
          transform: 'translateZ(0)',
        }}
      />*/}
      
      {/* Mouse-following gradient */}
      <div 
        className="absolute inset-0 w-full h-full"
        style={{
          background: `
            radial-gradient(
              ellipse 600px 400px at ${smoothMousePosition.x}px ${smoothMousePosition.y}px,
              rgba(255, 140, 0, 0.4) 0%,
              rgba(255, 102, 0, 0.25) 20%,
              rgba(255, 80, 0, 0.15) 35%,
              rgba(204, 51, 0, 0.1) 50%,
              transparent 70%
            )
          `,
          filter: 'blur(60px)',
          transform: 'translateZ(0)',
          mixBlendMode: 'screen'
        }}
      />
    </div>
  );
};

export default GradientBackground;
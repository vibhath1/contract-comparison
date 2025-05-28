import React from "react";
import "./AnimatedBorderBox.css"; // Ensure to include your custom CSS here

interface AnimatedBorderBoxProps {
  children: React.ReactNode;
  className?: string; // Add the className prop
}

const AnimatedBorderBox: React.FC<AnimatedBorderBoxProps> = ({ children, className }) => {
  return (
    <div className={`wrapper ${className}`}>
      <div className="animated-border" />
      <div className="content">{children}</div>
    </div>
  );
};

export default AnimatedBorderBox;
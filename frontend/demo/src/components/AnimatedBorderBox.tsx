import React from "react";
import "./AnimatedBorderBox.css"; // Ensure to include your custom CSS here

interface AnimatedBorderBoxProps {
  children: React.ReactNode;
}

const AnimatedBorderBox: React.FC<AnimatedBorderBoxProps> = ({ children }) => {
  return (
    <div className="wrapper">
      <div className="animated-border" />
      <div className="content">{children}</div>
    </div>
  );
};

export default AnimatedBorderBox;

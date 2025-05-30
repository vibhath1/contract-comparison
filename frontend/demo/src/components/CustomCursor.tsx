import { useEffect } from "react";
import "./CustomCursor.css";

const CustomCursor = () => {
  useEffect(() => {
    const coords = { x: 0, y: 0 };
    const circles = document.querySelectorAll<HTMLDivElement>(".circle");

    // Track each circle's trail position separately
    const positions = new Array(circles.length).fill(null).map(() => ({ x: 0, y: 0 }));

    // Mouse coordinates update
    const handleMouseMove = (e: MouseEvent) => {
      coords.x = e.clientX;
      coords.y = e.clientY;
    };
    window.addEventListener("mousemove", handleMouseMove);

    // Trail animation
    function animateCircles() {
      let x = coords.x;
      let y = coords.y;

      circles.forEach((circle, index) => {
        const nextPos = positions[index + 1] || positions[0];

        // Update circle position from positions array
        positions[index].x = x;
        positions[index].y = y;

        // Update circle style
        circle.style.left = x + "px";
        circle.style.top = y + "px";

        const scale = (circles.length - index) / circles.length;
        circle.style.transform = `translate(-50%, -50%) scale(${scale})`;

        // Move toward next position smoothly
        x += (nextPos.x - x) * 0.3;
        y += (nextPos.y - y) * 0.3;
      });

      requestAnimationFrame(animateCircles);
    }

    animateCircles();

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <div className="cursor">
      {Array.from({ length: 20 }).map((_, i) => (
        <div className="circle" key={i}></div>
      ))}
    </div>
  );
};

export default CustomCursor;

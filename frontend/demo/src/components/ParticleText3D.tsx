import React, { useRef, useMemo, useEffect, useState } from 'react';
import { Canvas, useFrame, useThree, useLoader } from '@react-three/fiber';
import * as THREE from 'three';
import { TextureLoader } from 'three';

interface ParticleSystemProps {
  text: string;
  isHovered: boolean;
  color : string; // added prop to track hover
}

function ParticleSystem({ text, isHovered,color = '#ffffff' }: ParticleSystemProps) {
  const meshRef = useRef<THREE.Points>(null);
  const mouseRef = useRef({ x: 0, y: 0 });
  const { viewport } = useThree();

  const discTexture = useLoader(TextureLoader, '/images/disc.png');

  const particlesPosition = useMemo(() => {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) return new Float32Array(0);

  canvas.width = 3000;
  canvas.height = 600;

  ctx.font = '800 500px "Montserrat", Montserrat, sans-serif';
  ctx.fillStyle = 'white';
  ctx.textAlign = 'left'; // We'll position each char manually
  ctx.textBaseline = 'middle';

  const textToDraw = text;
  const totalWidth = ctx.measureText(textToDraw).width;
  const letterSpacing = -0.10 * (totalWidth / textToDraw.length); // 5% tighter spacing per letter
  let x = (canvas.width - (totalWidth + letterSpacing * (textToDraw.length - 1))) / 2;

  const y = canvas.height / 2;

  for (let i = 0; i < textToDraw.length; i++) {
    const char = textToDraw[i];
    ctx.fillText(char, x, y);
    const charWidth = ctx.measureText(char).width;
    x += charWidth + letterSpacing;
  }

  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const pixels = imageData.data;
  const scale = 0.025;
  const particles = [];
  const gap = 3;

  for (let y = 0; y < canvas.height; y += gap) {
    for (let x = 0; x < canvas.width; x += gap) {
      const index = (y * canvas.width + x) * 4;
      const alpha = pixels[index + 3];
      if (alpha > 128) {
        const posX = (x - canvas.width / 2) * scale;
        const posY = -(y - canvas.height / 2) * scale;
        const posZ = (Math.random() - 0.5) * 2;
        particles.push(posX, posY, posZ);
      }
    }
  }

  return new Float32Array(particles);
}, [text]);


  const originalPositions = useMemo(() => new Float32Array(particlesPosition), [particlesPosition]);

  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      if (!isHovered) return; // Only update mouse position if hovered

      mouseRef.current = {
        x: (event.clientX / window.innerWidth) * 2 - 1,
        y: -(event.clientY / window.innerHeight) * 2 + 1,
      };
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [isHovered]); // reattach listener on hover change

  useFrame((state) => {
    if (!meshRef.current) return;
    const positions = meshRef.current.geometry.attributes.position.array as Float32Array;
    const time = state.clock.elapsedTime;

    // If not hovered, move mouse way off-screen so no influence
    const mouseX = isHovered ? mouseRef.current.x * viewport.width * 0.7 : 9999;
    const mouseY = isHovered ? mouseRef.current.y * viewport.height * 0.7 : 9999;

    for (let i = 0; i < positions.length; i += 3) {
      const x = originalPositions[i];
      const y = originalPositions[i + 1];
      const z = originalPositions[i + 2];
      const dx = mouseX - x;
      const dy = mouseY - y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < 5) {
        const force = (3 - distance) / 3;
        const angle = Math.atan2(dy, dx);
        positions[i] = x - Math.cos(angle) * force * 1.5 + Math.sin(time * 2 + i) * 0.1;
        positions[i + 1] = y - Math.sin(angle) * force * 1.5 + Math.cos(time * 2 + i) * 0.1;
        positions[i + 2] = z + force * 2 + Math.sin(time * 3 + i) * 0.2;
      } else {
        positions[i] += (x - positions[i]) * 0.1;
        positions[i + 1] += (y - positions[i + 1]) * 0.1;
        positions[i + 2] += (z - positions[i + 2]) * 0.1;
      }
    }

    meshRef.current.geometry.attributes.position.needsUpdate = true;
    {/*meshRef.current.rotation.y = Math.sin(time * 0.2) * 0.1;*/}
     meshRef.current.position.y = Math.sin(time * 1) * 0.3;

  });

  return (
    <points ref={meshRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[particlesPosition, 3]} />
      </bufferGeometry>
      <pointsMaterial
        size={0.20}
        map={discTexture}
        color={new THREE.Color(color)}
        alphaTest={0}
        transparent
        opacity={0.9}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  );
}

const ParticleText3D: React.FC<{ text: string; color?: string; className?: string }> = ({ text, color = '#ffffff', className }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={className}
      style={{ width: '1000px', height: '300px' }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Canvas camera={{ position: [0, 0, 50], fov: 23 }} style={{ background: 'transparent' }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <ParticleSystem text={text} isHovered={isHovered} color={color}/>
      </Canvas>
    </div>
  );
};

export default ParticleText3D;

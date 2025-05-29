// components/LandingPage.tsx
import React from 'react';
import ParticleText3D from './ParticleText3D';
import { EvervaultCardDemo } from './EvervaultCardDemo';

const LandingPage: React.FC = () => {
  return (
    <div className="w-full bg-[url('/images/verdictobg3.png')] bg-cover bg-center">
      {/* Hero Section */}
      <section className="min-h-screen flex flex-col justify-center items-center text-center">
        <ParticleText3D text="Verdicto" className="mb-3" />
        <h1 className="text-[24px] text-gray-300 font-italiana -mt-14 drop-shadow-[0_0_8px_rgba(255,255,255,0.7)]">
          Contract Comparison AI Tool
        </h1>
      </section>

      {/* Main Content Section */}
      <section className="min-h-screen flex flex-col justify-center items-center px-8 py-20 gap-10">
        {/*<div className="flex flex-wrap gap-10 justify-center">
          <div className="flex flex-col gap-10">
            <AnimatedBorderBox>
              <h2 className="text-2xl font-bold text-orange-500">Introducing our AI powered Contract Comparison</h2>
            </AnimatedBorderBox>

            <AnimatedBorderBox>
              <h2 className="text-2xl font-bold text-orange-500">Add necessary content</h2>
            </AnimatedBorderBox>
          </div>
          <AnimatedBorderBox className="flex flex-1">
            <h2 className="text-3xl font-bold text-orange-500">Your Contract Solution in ONE CLICK!</h2>
          </AnimatedBorderBox>
        </div>

        <AnimatedBorderBox className="w-full max-w-3xl">
          <h2 className="text-2xl font-bold text-orange-500">Add necessary content</h2>
        </AnimatedBorderBox>

        <h2 className="text-xl mt-12 text-white">Click the button below to Start.</h2>
        */}

          <EvervaultCardDemo></EvervaultCardDemo>

      </section>
    </div>
  );
};

export default LandingPage;
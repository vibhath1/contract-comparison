// components/LandingPage.tsx
import React from 'react';
import ParticleText3D from './ParticleText3D';
import { EvervaultCardDemo } from './EvervaultCardDemo';
import { HoverBorderGradientDemo } from './HoverBorderGradientDemo';


const LandingPage: React.FC = () => {
  return (
    <div className="w-full bg-[url('/images/verdictobg3.png')] bg-cover bg-center">
      {/* Hero Section */}
      <section className="min-h-screen flex flex-col justify-center items-center text-center">
        <ParticleText3D text="Verdicto" className="mb-3" color="#dbdbdb"/>
        <h1 className="text-[24px] text-gray-300 font-italiana -mt-14 drop-shadow-[0_0_8px_rgba(255,255,255,0.7)]">
          Contract Comparison AI Tool (do we use ai)?! recheck the objectives and usecases.
        </h1>
      </section>

      {/* Main Content Section */}
      <section className="min-h-screen flex flex-col justify-center items-center">
      <div className='flex justify-center gap-5'> 
      <EvervaultCardDemo></EvervaultCardDemo>
      </div>
      </section>
      <section className="min-h-screen flex flex-col justify-center items-center">
        <ParticleText3D text="⌕" color="#ff4800"/> 
        <h1 className='text-orange-500 text-[30px] -mt-6'>Click the button below to Start.</h1>
        <HoverBorderGradientDemo></HoverBorderGradientDemo>
      </section>
    </div>
  );
};

export default LandingPage;
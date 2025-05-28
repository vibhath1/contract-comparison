// components/LandingPage.tsx
import React, { useState } from 'react';
import Uploader from './Uploader';
import DocumentViewer from './DocumentViewer';
import SummaryTable from './SummaryTable';
import GradientBackground from './GradientBackground';
import ParticleText3D from './ParticleText3D';
import AnimatedBorderBox from './AnimatedBorderBox';



const LandingPage: React.FC = () => {
  const [leftFile, setLeftFile] = useState<File | null>(null);
  const [rightFile, setRightFile] = useState<File | null>(null);
  const [showComparison, setShowComparison] = useState(false);

  const handleCompare = () => setShowComparison(true);
  const handleBackToUpload = () => setShowComparison(false);
  const scrollToUploader = () => {
    const uploaderSection = document.getElementById("uploader-section");
    if (uploaderSection) {
      uploaderSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="relative w-full bg-[url('/images/Verdicto.png')] bg-cover bg-center">
      <GradientBackground />
      <div className="relative z-10">
        {!showComparison ? (
          <>
            <section className="min-h-screen flex flex-col justify-center items-center relative px-8">
              <div className="flex-1 flex flex-col justify-center items-center">
                <ParticleText3D
                  text="verdicto" 
                  className="mb-8"
                />

                
                  <h1 className="text-[30px] text-gray-100 font-italiana absolute mt-[150px] ">
                    Contract Comparison AI Tool
                  </h1>
                  
              </div>
            </section>

            <AnimatedBorderBox>
        <h1 className="text-2xl font-bold">Your Glowing Box</h1>
        <p>Drop in content here with styled glow effects.</p>
      </AnimatedBorderBox>

            <section id="uploader-section" className="min-h-screen flex items-center justify-center py-20">
              <div className="w-full max-w-7xl mx-auto px-8">
                <Uploader 
                  leftFile={leftFile}
                  rightFile={rightFile}
                  setLeftFile={setLeftFile}
                  setRightFile={setRightFile}
                  onCompare={handleCompare}
                />
              </div>
            </section>
          </>
        ) : (
          <section className="min-h-screen py-8">
            <div className="max-w-7xl mx-auto px-8">
              <div className="flex flex-col h-full">
                <header className="flex justify-between items-center mb-8">
                  <h1 className="text-3xl font-bold">Contract Comparison</h1>
                  <button 
                    onClick={handleBackToUpload}
                    className="bg-purple-600 text-white hover:bg-purple-700 transition-colors py-2 px-6 rounded-md font-medium"
                  >
                    Back to Upload
                  </button>
                </header>

                <main className="flex-1">
                  <DocumentViewer leftFile={leftFile} rightFile={rightFile} />
                  <div className="mt-8">
                    <SummaryTable />
                  </div>
                </main>
              </div>
            </div>
          </section>
        )}
      </div>
    </div>
  );
};

export default LandingPage;

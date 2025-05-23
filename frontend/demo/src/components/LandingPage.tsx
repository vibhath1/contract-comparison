// LandingPage.tsx
import React from 'react';

const LandingPage: React.FC = () => {
  // Function to scroll to the uploader section
  const scrollToUploader = () => {
    const uploaderSection = document.getElementById('uploader-section');
    if (uploaderSection) {
      uploaderSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center relative">
      <h1 className="text-8xl font-bold text-purple-700 mb-4">Verdicto</h1>
      <h1 className="text-4xl font-bold text-purple-700 mb-4">Contract Comparison AI Tool</h1>
      <p className="text-lg text-center max-w-2xl text-gray-700 mb-12">
        Our AI-powered tool allows you to effortlessly compare two contract documents.
        Upload your documents and receive a detailed comparison highlighting textual, grammatical,
        formatting, and visual differences. Perfect for legal professionals and businesses
        to ensure accuracy and consistency.
      </p>
      
      {/* Downward arrow with drop shadow */}
      <button 
        onClick={scrollToUploader}
        className="absolute bottom-20 animate-bounce"
        aria-label="Scroll to uploader"
      >
        <svg 
          className="w-10 h-10 text-purple-600 filter drop-shadow-md" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M19 14l-7 7m0 0l-7-7m7 7V3"
          />
        </svg>
      </button>
    </div>
  );
};

export default LandingPage;
// App.tsx
import React, { useState } from 'react';
import Uploader from './components/Uploader';
import DocumentViewer from './components/DocumentViewer';
import SummaryTable from './components/SummaryTable';
import LandingPage from './components/LandingPage';

const App: React.FC = () => {
  // State for tracking files and view mode
  const [leftFile, setLeftFile] = useState<File | null>(null);
  const [rightFile, setRightFile] = useState<File | null>(null);
  const [showComparison, setShowComparison] = useState(false);
  
  // Function to handle comparison button click
  const handleCompare = () => {
    if (leftFile && rightFile) {
      setShowComparison(true);
    }
  };
  
  // Function to go back to upload view
  const handleBackToUpload = () => {
    setShowComparison(false);
  };
  
  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Show landing page and uploader if not in comparison mode */}
      {!showComparison ? (
        <>
          <LandingPage />
          <div id="uploader-section">
            <Uploader 
              leftFile={leftFile}
              rightFile={rightFile}
              setLeftFile={setLeftFile}
              setRightFile={setRightFile}
              onCompare={handleCompare}
            />
          </div>
        </>
      ) : (
        /* Show comparison view if files are uploaded and compare is clicked */
        <div className="flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-xl font-bold">Contract Comparison</h1>
            <button 
              onClick={handleBackToUpload}
              className="text-purple-600 hover:text-purple-800"
            >
              Back to Upload
            </button>
          </div>
          
          <DocumentViewer leftFile={leftFile} rightFile={rightFile} />
          <div className="mt-4">
            <SummaryTable />
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
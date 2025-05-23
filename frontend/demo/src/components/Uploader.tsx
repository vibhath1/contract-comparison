// Update to Uploader.tsx
import React, { useRef } from 'react';
import type { DragEvent, ChangeEvent } from 'react';

interface UploaderProps {
  leftFile: File | null;
  rightFile: File | null;
  setLeftFile: (file: File | null) => void;
  setRightFile: (file: File | null) => void;
  onCompare: () => void;
}

const Uploader: React.FC<UploaderProps> = ({ 
  leftFile, 
  rightFile, 
  setLeftFile, 
  setRightFile, 
  onCompare 
}) => {
  // References to hidden file inputs
  const leftFileInputRef = useRef<HTMLInputElement>(null);
  const rightFileInputRef = useRef<HTMLInputElement>(null);

  // Handle drag events
  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('border-purple-400');
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('border-purple-400');
  };

  // Handle file drop
  const handleDrop = (side: 'left' | 'right') => (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('border-purple-400');

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (side === 'left') {
        setLeftFile(file);
      } else {
        setRightFile(file);
      }
    }
  };

  // Handle file selection via button
  const handleFileSelect = (side: 'left' | 'right') => (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      if (side === 'left') {
        setLeftFile(file);
      } else {
        setRightFile(file);
      }
    }
  };

  // Trigger file input click
  const openFileDialog = (side: 'left' | 'right') => () => {
    if (side === 'left' && leftFileInputRef.current) {
      leftFileInputRef.current.click();
    } else if (side === 'right' && rightFileInputRef.current) {
      rightFileInputRef.current.click();
    }
  };

  return (
    <div className="p-8 min-h-screen flex flex-col">
      <div className="flex-grow flex space-x-4">
        {/* Left Upload Area */}
        <div 
          className={`flex-1 border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center transition-colors duration-200 ${leftFile ? 'bg-gray-50' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop('left')}
        >
          <input 
            type="file" 
            ref={leftFileInputRef} 
            className="hidden" 
            onChange={handleFileSelect('left')} 
            accept="*/*"
          />
          
          {leftFile ? (
            <div className="text-center">
              <p className="font-medium">{leftFile.name}</p>
              <p className="text-sm text-gray-500">{(leftFile.size / 1024).toFixed(2)} KB</p>
              <button 
                onClick={() => setLeftFile(null)} 
                className="mt-2 text-red-500 text-sm hover:text-red-700"
              >
                Remove
              </button>
            </div>
          ) : (
            <>
              <p className="text-gray-500 mb-2">Drag and Drop File</p>
              <p className="text-gray-400 text-sm mb-2">or</p>
              <button 
                onClick={openFileDialog('left')} 
                className="bg-white text-purple-500 hover:bg-purple-600 hover:text-white border border-purple-500 py-1 px-4 rounded-md "
              >
                Select File
              </button>
            </>
          )}
        </div>
        
        {/* Right Upload Area */}
        <div 
          className={`flex-1 border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center transition-colors duration-200 ${rightFile ? 'bg-gray-50' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop('right')}
        >
          <input 
            type="file" 
            ref={rightFileInputRef} 
            className="hidden" 
            onChange={handleFileSelect('right')} 
            accept="*/*"
          />
          
          {rightFile ? (
            <div className="text-center">
              <p className="font-medium">{rightFile.name}</p>
              <p className="text-sm text-gray-500">{(rightFile.size / 1024).toFixed(2)} KB</p>
              <button 
                onClick={() => setRightFile(null)} 
                className="mt-2 text-red-500 text-sm hover:text-red-700"
              >
                Remove
              </button>
            </div>
          ) : (
            <>
              <p className="text-gray-500 mb-2">Drag and Drop File</p>
              <p className="text-gray-400 text-sm mb-2">or</p>
              <button 
                onClick={openFileDialog('right')} 
                className="bg-white text-purple-500 hover:bg-purple-600 hover:text-white border border-purple-500 py-1 px-4 rounded-md"
              >
                Select File
              </button>
            </>
          )}
        </div>
      </div>
      
      {/* Compare Button */}
      <div className="flex justify-center mt-4">
        <button 
          className={`py-2 px-6 rounded-md flex items-center ${
            leftFile && rightFile 
              ? 'bg-purple-500 text-white hover:bg-purple-600' 
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          disabled={!leftFile || !rightFile}
          onClick={onCompare}
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          Compare
        </button>
      </div>
    </div>
  );
};

export default Uploader;
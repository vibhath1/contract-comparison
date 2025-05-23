// DocumentViewer.tsx
import React from 'react';

interface DocumentViewerProps {
  leftFile: File | null;
  rightFile: File | null;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ leftFile, rightFile }) => {
  return (
    <div className="flex w-full h-[65vh] border rounded-lg overflow-hidden mb-4 bg-white shadow-md">
      {/* Left Document */}
      <div className="w-1/2 flex flex-col border-r">
        <div className="bg-gray-100 p-2 flex justify-between items-center border-b">
          <h3 className="font-medium truncate">{leftFile?.name || 'Document 1'}</h3>
          
        </div>
        <div className="flex-1 overflow-auto p-4">
          {/* This is where document content would be rendered */}
          <div className="prose max-w-none">
            <h1>Overview of LangChain Framework</h1>
            <p>LangChain is a <span className="bg-red-100">powerful</span> framework designed for <span className="bg-red-100">development, productionization,</span> and debugging of LLM applications.</p>
            
            <h2>Core Features</h2>
            <ol>
              <li>
                <strong>Development</strong>
                <ul>
                  <li>Open-Source Components: Build applications using LangChain components.</li>
                  <li>LangGraph: A tool for creating stateful agents with streaming and human-in-the-loop.</li>
                </ul>
              </li>
              <li>
                <strong>Productionization</strong>
                <ul>
                  <li>LangSmith: A platform for tracing, testing, and evaluating applications.</li>
                </ul>
              </li>
            </ol>
          </div>
        </div>
      </div>
      
      {/* Right Document */}
      <div className="w-1/2 flex flex-col">
        <div className="bg-gray-100 p-2 flex justify-between items-center border-b">
          <h3 className="font-medium truncate">{rightFile?.name || 'Document 2'}</h3>
          
        </div>
        <div className="flex-1 overflow-auto p-4">
          {/* This is where document content would be rendered */}
          <div className="prose max-w-none">
            <h1>Overview of LangChain Framework</h1>
            <p>LangChain is a <span className="bg-green-100">specialized</span> framework designed for <span className="bg-green-100">development, applications,</span> and debugging of large language models (LLMs).</p>
            
            <h2>Key Features</h2>
            <ol>
              <li>
                <strong>Development</strong>
                <ul>
                  <li>Open-Source Components: Build applications using LangChain modules.</li>
                  <li>LangGraph: A system for developing stateful agents with real-time streaming.</li>
                </ul>
              </li>
              <li>
                <strong>Productionization</strong>
                <ul>
                  <li>LangSmith: A platform for monitoring, testing, and evaluating applications.</li>
                </ul>
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentViewer;
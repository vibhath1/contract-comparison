// SummaryTable.tsx
import React from 'react';

const SummaryTable: React.FC = () => {
  return (
    <div className="w-full h-[30vh] border rounded-lg overflow-hidden bg-white shadow-md">
      <div className="bg-gray-100 p-2 border-b flex justify-between items-center">
        <h3 className="font-medium">Comparison</h3>
        <div className="text-xs text-gray-500">Page 1</div>
      </div>
      <div className="overflow-auto h-[calc(100%-2.5rem)]">
        <div className="divide-y">
          {/* Old vs New comparison items */}
          <div className="p-3 hover:bg-gray-50">
            <div className="flex justify-between mb-1">
              <span className="text-gray-500 text-sm">Old</span>
              <span className="text-xs text-gray-400">powerful</span>
            </div>
            <div className="bg-red-50 p-2 rounded text-sm">
              powerful
            </div>
            
            <div className="flex justify-between mb-1 mt-2">
              <span className="text-gray-500 text-sm">New</span>
              <span className="text-xs text-gray-400">specialized</span>
            </div>
            <div className="bg-green-50 p-2 rounded text-sm">
              specialized
            </div>
            <div className="mt-2 text-right">
              <button className="text-xs text-purple-600 hover:text-purple-800">Edit</button>
            </div>
          </div>
          
          <div className="p-3 hover:bg-gray-50">
            <div className="flex justify-between mb-1">
              <span className="text-gray-500 text-sm">Old</span>
              <span className="text-xs text-gray-400">development, productionization</span>
            </div>
            <div className="bg-red-50 p-2 rounded text-sm">
              development, productionization,
            </div>
            
            <div className="flex justify-between mb-1 mt-2">
              <span className="text-gray-500 text-sm">New</span>
              <span className="text-xs text-gray-400">development, applications</span>
            </div>
            <div className="bg-green-50 p-2 rounded text-sm">
              development, applications,
            </div>
            <div className="mt-2 text-right">
              <button className="text-xs text-purple-600 hover:text-purple-800">Edit</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SummaryTable;
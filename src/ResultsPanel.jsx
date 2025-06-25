import React from 'react';

const ResultsPanel = ({ resultData, isLoading }) => {
  return (
    <div className="flex-1 bg-gray-700 text-gray-200 overflow-hidden flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h3 className="text-lg font-semibold text-white">Pipeline Results</h3>
      </div>

      <div className="flex-1 p-4 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
              <div className="text-sm text-gray-400">Processing with X-Agents...</div>
            </div>
          </div>
        ) : resultData ? (
          <pre className="text-sm text-gray-200 whitespace-pre-wrap font-mono bg-gray-800 p-3 rounded">
            {resultData}
          </pre>
        ) : (
          <div className="text-center text-gray-500 mt-8">
            <div className="text-4xl mb-4">🤖</div>
            <div className="text-lg mb-2">X-Agent Pipeline Ready</div>
            <div className="text-sm">Submit a document to see agent processing results</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPanel;
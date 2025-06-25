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
          <div className="space-y-4">
            {/* Pipeline Step Indicator */}
            <div className="bg-gray-800 p-4 rounded-lg">
              <h4 className="text-sm font-semibold text-white mb-3">Pipeline Progress</h4>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span className="text-sm text-gray-300">📊 Analyst - Document Analysis Complete</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span className="text-sm text-gray-300">📋 Product Manager - Requirements Extracted</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span className="text-sm text-gray-300">🔧 Task Manager - Tasks Generated</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`w-2 h-2 rounded-full ${
                    resultData.includes('approved="true"') ? 'bg-green-500' : 'bg-red-500'
                  }`}></span>
                  <span className="text-sm text-gray-300">
                    ✅ PO Scrum Master - {resultData.includes('approved="true"') ? 'Approved' : 'Rejected (Feedback Provided)'}
                  </span>
                </div>
              </div>
            </div>

            {/* Detailed Results */}
            <div className="bg-gray-800 p-4 rounded-lg">
              <h4 className="text-sm font-semibold text-white mb-3">Detailed Results</h4>
              <pre className="text-sm text-gray-200 whitespace-pre-wrap font-mono max-h-96 overflow-y-auto">
                {resultData}
              </pre>
            </div>

            {/* Interactive Chat Hint */}
            {!resultData.includes('approved="true"') && (
              <div className="bg-blue-900 border border-blue-700 p-4 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-blue-400">💡</span>
                  <span className="text-sm font-semibold text-blue-300">Need Help?</span>
                </div>
                <p className="text-sm text-blue-200">
                  Use the 💬 Chat tab to discuss requirements with the AI advisor and refine your project scope.
                </p>
              </div>
            )}
          </div>
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
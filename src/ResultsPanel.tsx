
import React from 'react';

interface ResultsPanelProps {
  resultData: string | null;
  isLoading: boolean;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({ resultData, isLoading }) => {
  const parseXmlResponse = (xmlString: string) => {
    try {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlString, 'text/xml');
      const approvalElement = xmlDoc.querySelector('approval');
      
      if (approvalElement) {
        const status = approvalElement.getAttribute('status');
        const reasoning = approvalElement.textContent?.trim();
        
        return {
          status: status || 'unknown',
          reasoning: reasoning || 'No reasoning provided'
        };
      }
    } catch (error) {
      console.error('Error parsing XML:', error);
    }
    return null;
  };

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-300">Processing pipeline...</p>
          </div>
        </div>
      );
    }

    if (!resultData) {
      return (
        <div className="flex items-center justify-center h-full">
          <p className="text-gray-400">Results will appear here after running the pipeline</p>
        </div>
      );
    }

    const parsedResult = parseXmlResponse(resultData);
    
    if (parsedResult) {
      const { status, reasoning } = parsedResult;
      const isApproved = status?.toLowerCase() === 'approved';
      
      return (
        <div className="p-6">
          <div className={`p-4 rounded-lg mb-4 ${isApproved ? 'bg-green-900 border border-green-700' : 'bg-red-900 border border-red-700'}`}>
            <h3 className="text-lg font-semibold mb-2">
              Status: <span className={isApproved ? 'text-green-400' : 'text-red-400'}>
                {status?.toUpperCase()}
              </span>
            </h3>
            <p className="text-gray-200">{reasoning}</p>
          </div>
          
          <div className="bg-gray-900 p-4 rounded-lg">
            <h4 className="text-sm font-medium text-gray-400 mb-2">Raw Response:</h4>
            <pre className="text-xs text-gray-300 whitespace-pre-wrap overflow-auto max-h-96">
              {resultData}
            </pre>
          </div>
        </div>
      );
    }

    return (
      <div className="p-6">
        <div className="bg-gray-900 p-4 rounded-lg">
          <h4 className="text-sm font-medium text-gray-400 mb-2">Response:</h4>
          <pre className="text-sm text-gray-300 whitespace-pre-wrap overflow-auto max-h-96">
            {resultData}
          </pre>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-gray-200">Pipeline Results</h2>
      </div>
      <div className="flex-grow overflow-auto">
        {renderContent()}
      </div>
    </div>
  );
};

export default ResultsPanel;

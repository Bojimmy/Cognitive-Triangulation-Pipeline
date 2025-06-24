
import React from 'react';

const ResultsPanel = ({ resultData, isLoading }) => {
  const parseXmlResponse = (xmlString) => {
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

    const parsedData = parseXmlResponse(resultData);
    
    if (parsedData) {
      const statusColor = parsedData.status === 'approved' ? 'text-green-400' : 'text-red-400';
      return (
        <div className="p-4">
          <div className="mb-4">
            <h3 className="text-lg font-semibold mb-2">Approval Status</h3>
            <p className={`font-bold ${statusColor}`}>
              {parsedData.status.toUpperCase()}
            </p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-2">Reasoning</h3>
            <p className="text-gray-300 whitespace-pre-wrap">{parsedData.reasoning}</p>
          </div>
        </div>
      );
    }

    return (
      <div className="p-4">
        <pre className="text-gray-300 whitespace-pre-wrap overflow-auto">{resultData}</pre>
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

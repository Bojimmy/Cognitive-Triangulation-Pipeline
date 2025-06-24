
import React, { useState } from 'react';
import InputPanel from './InputPanel.jsx';
import ResultsPanel from './ResultsPanel.jsx';

export default function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [resultData, setResultData] = useState(null);

  const handleRunPipeline = async (promptText) => {
    setIsLoading(true);
    setResultData(null);

    try {
      const response = await fetch('http://localhost:5001/api/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: promptText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.text();
      setResultData(result);
    } catch (error) {
      console.error('Error processing pipeline:', error);
      setResultData(`Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <div className="w-[35%]">
        <InputPanel onRunPipeline={handleRunPipeline} isLoading={isLoading} />
      </div>
      <div className="w-[65%] bg-gray-800">
        <ResultsPanel resultData={resultData} isLoading={isLoading} />
      </div>
    </div>
  );
}

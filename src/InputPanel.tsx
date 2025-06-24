
import React, { useState } from 'react';

interface InputPanelProps {
  onRunPipeline: (promptText: string) => void;
  isLoading: boolean;
}

const InputPanel: React.FC<InputPanelProps> = ({ onRunPipeline, isLoading }) => {
  const [text, setText] = useState('');

  const handleRunClick = () => {
    if (!text.trim() || isLoading) return;
    onRunPipeline(text);
  };

  return (
    <div className="flex flex-col h-full p-4 bg-gray-800 border-r border-gray-700">
      <label htmlFor="prd-input" className="mb-2 text-sm font-medium text-gray-300">
        Project Requirements Document
      </label>
      <textarea
        id="prd-input"
        className="w-full flex-grow bg-gray-900 rounded-md p-3 text-sm text-gray-200 resize-none focus:ring-2 focus:ring-blue-500 focus:outline-none"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste your project description here..."
      />
      <button
        onClick={handleRunClick}
        disabled={isLoading}
        className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed"
      >
        {isLoading ? 'Processing...' : 'Run X-Flow Pipeline'}
      </button>
    </div>
  );
};

export default InputPanel;

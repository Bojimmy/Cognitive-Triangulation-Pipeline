
import React, { useState } from 'react';

export default function DocumentFormatter({ onFormatComplete }) {
  const [content, setContent] = useState('');
  const [targetDomain, setTargetDomain] = useState('');
  const [isFormatting, setIsFormatting] = useState(false);
  const [result, setResult] = useState(null);

  const handleFormat = async () => {
    if (!content.trim()) return;

    setIsFormatting(true);
    setResult(null); // Clear previous results
    
    try {
      console.log('Attempting to connect to backend...');
      const response = await fetch('http://localhost:5000/api/format-document', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content,
          domain: targetDomain || null
        })
      });

      console.log('Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Response data:', data);
      
      if (data.success) {
        setResult(data);
        if (onFormatComplete) {
          onFormatComplete(data.formatted_content);
        }
      } else {
        console.error('Formatting failed:', data.error);
        setResult({ error: data.error });
      }
    } catch (error) {
      console.error('Network error:', error);
      setResult({ 
        error: `Connection failed: ${error.message}. Make sure the Flask backend is running on port 5000.` 
      });
    } finally {
      setIsFormatting(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Document Formatter</h2>
      
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Raw Document Content:
        </label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full h-40 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Paste your document content here..."
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Target Domain (optional):
        </label>
        <select
          value={targetDomain}
          onChange={(e) => setTargetDomain(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Auto-detect</option>
          <option value="real_estate">Real Estate</option>
          <option value="customer_support">Customer Support</option>
          <option value="healthcare">Healthcare</option>
          <option value="fintech">Fintech</option>
          <option value="ecommerce">E-commerce</option>
          <option value="mobile_app">Mobile App</option>
        </select>
      </div>

      <button
        onClick={handleFormat}
        disabled={isFormatting || !content.trim()}
        className={`w-full py-2 px-4 rounded-md font-medium ${
          isFormatting || !content.trim()
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700'
        }`}
      >
        {isFormatting ? 'Formatting...' : 'Format Document'}
      </button>

      {result && (
        <div className="mt-6 space-y-4">
          {result.error ? (
            <div className="p-4 bg-red-50 rounded-md">
              <h3 className="font-semibold text-red-800 mb-2">Formatting Error</h3>
              <p className="text-red-700">{result.error}</p>
            </div>
          ) : (
            <div className="p-4 bg-green-50 rounded-md">
              <h3 className="font-semibold text-green-800 mb-2">Formatting Complete!</h3>
              <p className="text-green-700">
                Validation Score: {result.validation_score}% | 
                Domain: {result.domain || 'Auto-detected'} | 
                Requirements: {result.requirements?.length || 0}
              </p>
            </div>
          )}

          <div className="p-4 bg-gray-50 rounded-md">
            <h4 className="font-medium text-gray-800 mb-2">Formatted Content:</h4>
            <pre className="whitespace-pre-wrap text-sm text-gray-700 bg-white p-3 rounded border max-h-60 overflow-y-auto">
              {result.formatted_content}
            </pre>
          </div>

          {result.requirements && result.requirements.length > 0 && (
            <div className="p-4 bg-blue-50 rounded-md">
              <h4 className="font-medium text-blue-800 mb-2">Extracted Requirements:</h4>
              <ul className="space-y-1">
                {result.requirements.map((req, index) => (
                  <li key={index} className="text-sm text-blue-700">
                    <span className="font-medium">{req.id}:</span> {req.title}
                    {req.domain_keywords && req.domain_keywords.length > 0 && (
                      <span className="text-xs text-gray-500 ml-2">
                        ({req.domain_keywords.join(', ')})
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

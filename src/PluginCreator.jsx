
import React, { useState } from 'react';

export default function PluginCreator() {
  const [content, setContent] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [isCreating, setIsCreating] = useState(false);

  const handleAnalyze = async () => {
    if (!content.trim()) return;

    setIsAnalyzing(true);
    try {
      const response = await fetch('/api/create-plugin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content })
      });

      const data = await response.json();
      
      if (data.success) {
        setAnalysis(data);
      } else {
        console.error('Analysis failed:', data.error);
      }
    } catch (error) {
      console.error('Network error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleCreatePlugin = async () => {
    if (!analysis?.suggested_plugin) return;

    setIsCreating(true);
    try {
      const response = await fetch('/api/create-plugin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          plugin_spec: analysis.suggested_plugin 
        })
      });

      const data = await response.json();
      
      if (data.success) {
        alert(`Plugin "${data.domain_name}" created successfully!`);
        setAnalysis(null);
        setContent('');
      } else {
        alert(`Plugin creation failed: ${data.error}`);
      }
    } catch (error) {
      console.error('Network error:', error);
      alert('Network error during plugin creation');
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
        <h2 className="text-2xl font-bold text-yellow-800 mb-2">🔧 Domain Plugin Creator</h2>
        <p className="text-yellow-700 text-sm">
          <strong>Admin Tool:</strong> Analyze content to create new domain plugins for the X-Agent system
        </p>
      </div>
      
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Sample Content for Domain Analysis:
        </label>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Paste sample content from a new domain to analyze..."
        />
      </div>

      <button
        onClick={handleAnalyze}
        disabled={isAnalyzing || !content.trim()}
        className={`w-full py-2 px-4 rounded-md font-medium mb-4 ${
          isAnalyzing || !content.trim()
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-purple-600 text-white hover:bg-purple-700'
        }`}
      >
        {isAnalyzing ? 'Analyzing...' : 'Analyze for Plugin Creation'}
      </button>

      {analysis && (
        <div className="space-y-4">
          <div className="p-4 bg-purple-50 rounded-md">
            <h3 className="font-semibold text-purple-800 mb-2">Analysis Results</h3>
            <div className="space-y-2 text-sm">
              <p><strong>Suggested Domain:</strong> {analysis.suggested_plugin.domain_name}</p>
              <p><strong>Confidence:</strong> {(analysis.confidence * 100).toFixed(1)}%</p>
              <p><strong>Priority Score:</strong> {analysis.suggested_plugin.priority_score}/5</p>
              <p><strong>Keywords:</strong> {analysis.suggested_plugin.keywords.join(', ')}</p>
              <p><strong>Stakeholders:</strong> {analysis.suggested_plugin.stakeholders.join(', ')}</p>
            </div>
          </div>

          {analysis.suggested_plugin.requirements_patterns && (
            <div className="p-4 bg-blue-50 rounded-md">
              <h4 className="font-medium text-blue-800 mb-2">Detected Requirement Patterns:</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                {analysis.suggested_plugin.requirements_patterns.map((pattern, index) => (
                  <li key={index}>
                    <strong>{pattern.type}:</strong> {pattern.template}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <button
            onClick={handleCreatePlugin}
            disabled={isCreating}
            className={`w-full py-2 px-4 rounded-md font-medium ${
              isCreating
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-green-600 text-white hover:bg-green-700'
            }`}
          >
            {isCreating ? 'Creating Plugin...' : 'Create Plugin'}
          </button>
        </div>
      )}
    </div>
  );
}

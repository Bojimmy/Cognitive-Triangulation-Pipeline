
import React, { useState } from 'react';

const InputPanel = ({ onRunPipeline, isLoading }) => {
  const [text, setText] = useState('');
  const [mode, setMode] = useState('text'); // 'text', 'file', 'chat'
  const [chatHistory, setChatHistory] = useState([]);
  const [chatInput, setChatInput] = useState('');

  const handleRunClick = () => {
    if (!text.trim() || isLoading) return;
    onRunPipeline(text);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setText(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleChatSubmit = () => {
    if (!chatInput.trim()) return;
    
    const newMessage = {
      type: 'user',
      content: chatInput,
      timestamp: new Date().toLocaleTimeString()
    };
    
    setChatHistory(prev => [...prev, newMessage]);
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        type: 'ai',
        content: `I understand you want to know about: "${chatInput}". Let me help you structure this for the X-Agents pipeline. Consider breaking this into specific requirements with REQ-001, REQ-002 format.`,
        timestamp: new Date().toLocaleTimeString()
      };
      setChatHistory(prev => [...prev, aiResponse]);
    }, 1000);
    
    setChatInput('');
  };

  const clearChat = () => {
    setChatHistory([]);
  };

  const generateFromChat = () => {
    const chatText = chatHistory
      .filter(msg => msg.type === 'user')
      .map((msg, idx) => `REQ-${(idx + 1).toString().padStart(3, '0')}: ${msg.content}`)
      .join('\n\n');
    setText(chatText);
    setMode('text');
  };

  return (
    <div className="flex flex-col h-full bg-gray-800 border-r border-gray-700">
      {/* Mode Tabs */}
      <div className="flex border-b border-gray-700">
        <button
          onClick={() => setMode('text')}
          className={`flex-1 px-4 py-2 text-sm font-medium ${
            mode === 'text' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:text-gray-200'
          }`}
        >
          📝 Text
        </button>
        <button
          onClick={() => setMode('file')}
          className={`flex-1 px-4 py-2 text-sm font-medium ${
            mode === 'file' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:text-gray-200'
          }`}
        >
          📄 File
        </button>
        <button
          onClick={() => setMode('chat')}
          className={`flex-1 px-4 py-2 text-sm font-medium ${
            mode === 'chat' ? 'bg-gray-700 text-white' : 'text-gray-400 hover:text-gray-200'
          }`}
        >
          💬 Chat
        </button>
      </div>

      <div className="flex-1 p-4 overflow-hidden flex flex-col">
        {mode === 'text' && (
          <>
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
          </>
        )}

        {mode === 'file' && (
          <>
            <label className="mb-2 text-sm font-medium text-gray-300">
              Upload Document
            </label>
            <div className="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center mb-4">
              <input
                type="file"
                accept=".txt,.md,.doc,.docx"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="text-gray-400 mb-2">📁</div>
                <div className="text-sm text-gray-300">Click to upload document</div>
                <div className="text-xs text-gray-500 mt-1">Supports .txt, .md, .doc, .docx</div>
              </label>
            </div>
            <textarea
              className="w-full flex-grow bg-gray-900 rounded-md p-3 text-sm text-gray-200 resize-none focus:ring-2 focus:ring-blue-500 focus:outline-none"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Uploaded content will appear here..."
            />
          </>
        )}

        {mode === 'chat' && (
          <>
            <div className="flex justify-between items-center mb-2">
              <label className="text-sm font-medium text-gray-300">
                Requirements Chat
              </label>
              <div className="space-x-2">
                {chatHistory.length > 0 && (
                  <button
                    onClick={generateFromChat}
                    className="text-xs px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-white"
                  >
                    Use for Pipeline
                  </button>
                )}
                <button
                  onClick={clearChat}
                  className="text-xs px-2 py-1 bg-red-600 hover:bg-red-700 rounded text-white"
                >
                  Clear
                </button>
              </div>
            </div>
            
            <div className="flex-grow bg-gray-900 rounded-md p-3 overflow-y-auto mb-3">
              {chatHistory.length === 0 ? (
                <div className="text-gray-500 text-sm">
                  Ask questions about your project requirements...
                </div>
              ) : (
                <div className="space-y-3">
                  {chatHistory.map((msg, idx) => (
                    <div key={idx} className={`${msg.type === 'user' ? 'text-blue-300' : 'text-green-300'}`}>
                      <div className="text-xs text-gray-500 mb-1">
                        {msg.type === 'user' ? '👤 You' : '🤖 AI'} - {msg.timestamp}
                      </div>
                      <div className="text-sm">{msg.content}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
            
            <div className="flex gap-2">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleChatSubmit()}
                placeholder="Ask about requirements..."
                className="flex-1 bg-gray-700 text-white text-sm px-3 py-2 rounded focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
              <button
                onClick={handleChatSubmit}
                className="px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded"
              >
                Send
              </button>
            </div>
          </>
        )}
      </div>

      {(mode === 'text' || mode === 'file') && (
        <div className="p-4 border-t border-gray-700">
          <button
            onClick={handleRunClick}
            disabled={isLoading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Processing...' : 'Run X-Flow Pipeline'}
          </button>
        </div>
      )}
    </div>
  );
};

export default InputPanel;

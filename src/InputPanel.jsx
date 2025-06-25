
import React, { useState } from 'react';

const InputPanel = ({ onRunPipeline, isLoading }) => {
  const [text, setText] = useState('');
  const [mode, setMode] = useState('text'); // 'text', 'file', 'chat'
  const [chatHistory, setChatHistory] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [showChatPopup, setShowChatPopup] = useState(false);

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

  const handleChatSubmit = async () => {
    if (!chatInput.trim() || isLoading) return;
    
    const userMessage = chatInput;
    const newMessage = {
      type: 'user',
      content: userMessage,
      timestamp: new Date().toLocaleTimeString()
    };
    
    setChatHistory(prev => [...prev, newMessage]);
    setChatInput('');
    
    // Add typing indicator
    const typingMessage = {
      type: 'ai',
      content: '🤖 Generating requirements...',
      timestamp: new Date().toLocaleTimeString()
    };
    setChatHistory(prev => [...prev, typingMessage]);
    
    // Generate structured requirements directly
    const requirements = generateRequirements(userMessage);
    
    // Remove typing indicator and add requirements
    setChatHistory(prev => {
      const withoutTyping = prev.slice(0, -1);
      return [...withoutTyping, {
        type: 'ai',
        content: requirements,
        timestamp: new Date().toLocaleTimeString()
      }];
    });
  };

  const generateRequirements = (description) => {
    const lowerDesc = description.toLowerCase();
    let requirements = [];
    let reqNum = 1;

    // Core requirements based on project type
    if (lowerDesc.includes('web') || lowerDesc.includes('website') || lowerDesc.includes('app')) {
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: User Interface Design - Create responsive and intuitive user interface`);
      reqNum++;
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: User Authentication - Implement secure login and registration system`);
      reqNum++;
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Database Integration - Set up data storage and retrieval system`);
      reqNum++;
    }

    if (lowerDesc.includes('mobile') || lowerDesc.includes('ios') || lowerDesc.includes('android')) {
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Platform Support - Support for iOS and/or Android platforms`);
      reqNum++;
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Offline Functionality - Core features work without internet connection`);
      reqNum++;
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Push Notifications - Real-time user engagement notifications`);
      reqNum++;
    }

    if (lowerDesc.includes('api') || lowerDesc.includes('backend') || lowerDesc.includes('server')) {
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: API Endpoints - RESTful API design and implementation`);
      reqNum++;
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Data Validation - Input validation and sanitization`);
      reqNum++;
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Error Handling - Comprehensive error management system`);
      reqNum++;
    }

    if (lowerDesc.includes('ecommerce') || lowerDesc.includes('shop') || lowerDesc.includes('store')) {
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Product Catalog - Product listing and search functionality`);
      reqNum++;
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Shopping Cart - Add to cart and checkout process`);
      reqNum++;
      requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Payment Integration - Secure payment processing system`);
      reqNum++;
    }

    // Security requirements
    requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Security - Data encryption and secure communication protocols`);
    reqNum++;

    // Performance requirements  
    requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Performance - Page load times under 3 seconds`);
    reqNum++;

    // Testing requirements
    requirements.push(`REQ-${reqNum.toString().padStart(3, '0')}: Testing - Unit tests and integration test coverage`);
    reqNum++;

    if (requirements.length === 3) {
      // Generic requirements if no specific type detected
      requirements = [
        `REQ-001: Core Functionality - Implement main features as described`,
        `REQ-002: User Experience - Intuitive and user-friendly interface`,
        `REQ-003: Data Management - Proper data handling and storage`,
        `REQ-004: Security - Secure data transmission and storage`,
        `REQ-005: Performance - Optimized for speed and efficiency`,
        `REQ-006: Testing - Comprehensive testing coverage`
      ];
    }

    return requirements.join('\n\n');
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
          onClick={() => setShowChatPopup(true)}
          className="flex-1 px-4 py-2 text-sm font-medium text-gray-400 hover:text-gray-200"
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

      {/* Chat Popup */}
      {showChatPopup && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg w-96 h-96 flex flex-col border border-gray-700">
            {/* Chat Header */}
            <div className="flex justify-between items-center p-4 border-b border-gray-700">
              <h3 className="text-sm font-medium text-gray-300">
                🤖 Requirements Assistant
              </h3>
              <div className="flex gap-2">
                {chatHistory.length > 0 && (
                  <button
                    onClick={() => {
                      generateFromChat();
                      setShowChatPopup(false);
                    }}
                    className="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-white text-xs"
                  >
                    Use for Pipeline
                  </button>
                )}
                <button
                  onClick={clearChat}
                  className="px-2 py-1 bg-red-600 hover:bg-red-700 rounded text-white text-xs"
                >
                  Clear
                </button>
                <button
                  onClick={() => setShowChatPopup(false)}
                  className="px-2 py-1 bg-gray-600 hover:bg-gray-700 rounded text-white text-xs"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* Chat Messages Area */}
            <div className="flex-1 p-4 overflow-y-auto bg-gray-900">
              {chatHistory.length === 0 ? (
                <div className="text-center text-gray-500 text-sm mt-8">
                  <div className="text-3xl mb-3">💬</div>
                  <div className="mb-2">Requirements Assistant</div>
                  <div className="text-xs">I'll help you create structured requirements in REQ-001 format</div>
                </div>
              ) : (
                <div className="space-y-4">
                  {chatHistory.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[90%] px-3 py-2 rounded-lg ${
                        msg.type === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gray-700 text-gray-200'
                      }`}>
                        <div className="text-xs opacity-70 mb-1">
                          {msg.type === 'user' ? '👤 You' : '🤖 AI'} • {msg.timestamp}
                        </div>
                        <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Chat Input Area */}
            <div className="p-4 border-t border-gray-700">
              <div className="flex gap-2">
                <textarea
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleChatSubmit();
                    }
                  }}
                  placeholder="Describe your project for structured requirements..."
                  className="flex-1 bg-gray-700 text-white text-sm px-3 py-2 rounded focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
                  rows="2"
                  disabled={isLoading}
                />
                <button
                  onClick={handleChatSubmit}
                  disabled={!chatInput.trim() || isLoading}
                  className="px-3 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white text-sm rounded font-medium"
                >
                  {isLoading ? '...' : 'Send'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InputPanel;


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
      content: '🤖 Thinking...',
      timestamp: new Date().toLocaleTimeString()
    };
    setChatHistory(prev => [...prev, typingMessage]);
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          history: chatHistory
        })
      });
      
      const data = await response.json();
      
      // Remove typing indicator and add real response
      setChatHistory(prev => {
        const withoutTyping = prev.slice(0, -1);
        return [...withoutTyping, {
          type: 'ai',
          content: data.response || 'Sorry, I encountered an error processing your request.',
          timestamp: new Date().toLocaleTimeString()
        }];
      });
    } catch (error) {
      console.error('Chat error:', error);
      setChatHistory(prev => {
        const withoutTyping = prev.slice(0, -1);
        return [...withoutTyping, {
          type: 'ai',
          content: 'Sorry, I encountered an error. Please try again later.',
          timestamp: new Date().toLocaleTimeString()
        }];
      });
    }
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
          <div className="flex flex-col h-full">
            {/* Chat Header */}
            <div className="flex justify-between items-center mb-3 pb-2 border-b border-gray-700">
              <h3 className="text-sm font-medium text-gray-300">
                🤖 Requirements Assistant
              </h3>
              <div className="flex gap-2">
                {chatHistory.length > 0 && (
                  <button
                    onClick={generateFromChat}
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
              </div>
            </div>

            {/* Chat Messages Area */}
            <div className="bg-gray-900 rounded-lg p-4 overflow-y-auto mb-3" style={{ minHeight: '300px', maxHeight: '400px' }}>
              {chatHistory.length === 0 ? (
                <div className="text-center text-gray-500 text-sm mt-12">
                  <div className="text-3xl mb-3">💬</div>
                  <div className="mb-2">Welcome to Requirements Chat!</div>
                  <div className="text-xs">Ask questions like:</div>
                  <div className="text-xs mt-1 text-gray-400">
                    • "Help me structure a web app"<br/>
                    • "What features should I include?"<br/>
                    • "Break this down into requirements"
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  {chatHistory.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-xs px-3 py-2 rounded-lg ${
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
            <div className="bg-gray-800 rounded-lg p-3 border border-gray-700">
              <div className="flex flex-col gap-2">
                <textarea
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleChatSubmit();
                    }
                  }}
                  placeholder="Type your question about requirements..."
                  className="w-full bg-gray-700 text-white text-sm px-3 py-3 rounded focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
                  rows="3"
                  disabled={isLoading}
                />
                <div className="flex justify-between items-center">
                  <div className="text-xs text-gray-500">
                    Press Enter to send • Shift+Enter for new line
                  </div>
                  <button
                    onClick={handleChatSubmit}
                    disabled={!chatInput.trim() || isLoading}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white text-sm rounded font-medium"
                  >
                    {isLoading ? '...' : 'Send'}
                  </button>
                </div>
              </div>
            </div>
          </div>
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

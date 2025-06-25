import React, { useState, useEffect } from 'react';

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
      content: '🤖 Thinking...',
      timestamp: new Date().toLocaleTimeString()
    };
    setChatHistory(prev => [...prev, typingMessage]);

    try {
      // Call the actual LLM API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          history: chatHistory.filter(msg => msg.content !== '🤖 Thinking...')
        })
      });

      const data = await response.json();
      const aiResponse = data.response || 'Sorry, I encountered an error. Please try again.';

      // Remove typing indicator and add real AI response
      setChatHistory(prev => {
        const withoutTyping = prev.slice(0, -1);
        return [...withoutTyping, {
          type: 'ai',
          content: aiResponse,
          timestamp: new Date().toLocaleTimeString()
        }];
      });

    } catch (error) {
      console.error('Chat API error:', error);
      
      // Remove typing indicator and add error message
      setChatHistory(prev => {
        const withoutTyping = prev.slice(0, -1);
        return [...withoutTyping, {
          type: 'ai',
          content: 'Sorry, I had trouble connecting. Please try again or check if the backend is running.',
          timestamp: new Date().toLocaleTimeString()
        }];
      });
    }
  };

  

  // Auto-scroll chat to bottom when new messages are added
  useEffect(() => {
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }, [chatHistory]);

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
    setShowChatPopup(false);
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
          className="flex-1 px-4 py-2 text-sm font-medium text-gray-400 hover:text-gray-200 relative"
        >
          💬 AI Advisor
          {chatHistory.length > 0 && (
            <span className="absolute -top-1 -right-1 bg-blue-500 text-xs rounded-full w-5 h-5 flex items-center justify-center">
              {chatHistory.filter(msg => msg.type === 'user').length}
            </span>
          )}
        </button>
      </div>

      <div className="flex-1 p-4 overflow-hidden flex flex-col">
        {/* Workflow Guide */}
        <div className="mb-4 p-3 bg-gray-900 rounded-lg border border-gray-600">
          <h4 className="text-xs font-semibold text-gray-300 mb-2">🔄 X-Agent Workflow</h4>
          <div className="text-xs text-gray-400 space-y-1">
            <div>1. 📊 <strong>Analyst</strong> analyzes your input</div>
            <div>2. 📋 <strong>Product Manager</strong> extracts requirements</div>
            <div>3. 🔧 <strong>Task Manager</strong> breaks into tasks</div>
            <div>4. ✅ <strong>PO Scrum Master</strong> approves or provides feedback</div>
          </div>
        </div>

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
              placeholder="Describe your project requirements here...

Example:
I need a mobile app for task management with user authentication, offline sync, and real-time collaboration features."
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
        <div className="p-4 border-t border-gray-600">
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
          <div className="rounded-lg w-96 h-96 flex flex-col border border-gray-700" style={{backgroundColor: '#1f2937'}}>
            {/* Chat Header */}
            <div className="flex justify-between items-center p-4 border-b border-gray-700" style={{backgroundColor: '#1f2937'}}>
              <h3 className="text-sm font-medium text-gray-300">
                🤖 Development Advisor
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
            <div className="flex-1 p-4 overflow-y-auto" id="chat-messages" style={{backgroundColor: '#1f2937'}}>
              {chatHistory.length === 0 ? (
                <div className="text-center text-gray-400 text-sm mt-8">
                  <div className="text-3xl mb-3">💬</div>
                  <div className="mb-2 text-gray-300">Development Advisor</div>
                  <div className="text-xs text-gray-500">Ask questions, get advice, or brainstorm ideas - I'm here to help!</div>
                </div>
              ) : (
                <div className="space-y-4">
                  {chatHistory.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[90%] px-3 py-2 rounded-lg ${
                        msg.type === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gray-700 text-white'
                      }`}>
                        <div className={`text-xs mb-1 ${
                          msg.type === 'user' ? 'text-blue-200' : 'text-gray-400'
                        }`}>
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
            <div className="p-4 border-t border-gray-600" style={{backgroundColor: '#1f2937'}}>
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
                  placeholder="Ask a question or describe your project..."
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
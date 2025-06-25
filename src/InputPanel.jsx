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

    // Simulate realistic response time
    setTimeout(() => {
      const response = generateResponse(userMessage);

      // Remove typing indicator and add response
      setChatHistory(prev => {
        const withoutTyping = prev.slice(0, -1);
        return [...withoutTyping, {
          type: 'ai',
          content: response,
          timestamp: new Date().toLocaleTimeString()
        }];
      });
    }, 1000 + Math.random() * 1500); // 1-2.5 seconds delay
  };

  const generateResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();

    // Project management and workflow advice
    if (lowerInput.includes('start') || lowerInput.includes('begin') || lowerInput.includes('getting started')) {
      return "Great! Starting a new project? Here's my advice:\n\n1. **Define your goals clearly** - What problem are you solving?\n2. **Start small** - Build an MVP first\n3. **Plan your tech stack** - Choose familiar technologies\n4. **Set up version control** - Use Git from day one\n5. **Think about your users** - Who will use this?\n\nWhat kind of project are you thinking about?";
    }

    if (lowerInput.includes('stuck') || lowerInput.includes('problem') || lowerInput.includes('issue')) {
      return "I understand you're facing a challenge! Here's how I'd approach it:\n\n💡 **Break it down**: What's the smallest part you can tackle first?\n🔍 **Research**: Have others solved similar problems?\n🤝 **Ask for help**: Don't hesitate to reach out to communities\n📝 **Document**: Write down what you've tried\n\nTell me more about what's blocking you - I'm here to help brainstorm solutions!";
    }

    if (lowerInput.includes('tech stack') || lowerInput.includes('technology') || lowerInput.includes('framework')) {
      return "Choosing the right tech stack is crucial! Here's my framework for deciding:\n\n🎯 **Consider your goals**: Performance? Speed of development? Team expertise?\n📊 **Popular combos**:\n   • Frontend: React/Vue + Tailwind\n   • Backend: Node.js/Python + Database\n   • Full-stack: Next.js, Django, or Rails\n\n💭 **My advice**: Start with what you know, then expand. What type of application are you building?";
    }

    if (lowerInput.includes('design') || lowerInput.includes('ui') || lowerInput.includes('user interface')) {
      return "Great question about design! Here's my design philosophy:\n\n✨ **Keep it simple**: Users should understand it immediately\n📱 **Mobile-first**: Most users are on phones\n🎨 **Consistent patterns**: Use established UI conventions\n⚡ **Fast loading**: Performance is user experience\n♿ **Accessible**: Design for everyone\n\nAre you looking for design tools, principles, or specific UI advice?";
    }

    if (lowerInput.includes('database') || lowerInput.includes('data') || lowerInput.includes('storage')) {
      return "Data strategy is so important! Here's how I think about it:\n\n📊 **Start simple**: PostgreSQL or MySQL for most projects\n🏗️ **Design your schema carefully**: Think about relationships early\n📈 **Plan for scale**: But don't over-engineer initially\n🔒 **Security first**: Always encrypt sensitive data\n💾 **Backup strategy**: Automate backups from day one\n\nWhat kind of data are you working with?";
    }

    if (lowerInput.includes('learn') || lowerInput.includes('improve') || lowerInput.includes('better')) {
      return "Love the growth mindset! Here's my learning strategy:\n\n📚 **Build projects**: Learning by doing is most effective\n🎯 **Focus deeply**: Master one thing at a time\n👥 **Join communities**: Discord, Reddit, local meetups\n📖 **Read code**: Study well-written open source projects\n🔄 **Practice daily**: Even 30 minutes helps\n\nWhat specific skill are you trying to develop?";
    }

    if (lowerInput.includes('deployment') || lowerInput.includes('deploy') || lowerInput.includes('hosting')) {
      return "Deployment advice coming up! Here's my hosting strategy:\n\n🚀 **For beginners**: Vercel (frontend) + Railway/Heroku (backend)\n💰 **Budget-friendly**: Netlify, GitHub Pages, or Replit\n⚡ **Performance**: AWS, Google Cloud, or Digital Ocean\n🔄 **CI/CD**: Set up automated deployments early\n📊 **Monitoring**: Use analytics and error tracking\n\nWhat type of app are you looking to deploy?";
    }

    if (lowerInput.includes('team') || lowerInput.includes('collaboration') || lowerInput.includes('working together')) {
      return "Team collaboration is an art! Here's what works:\n\n🎯 **Clear communication**: Regular standups and documentation\n📋 **Define roles**: Who does what, when\n🔄 **Version control**: Git workflow with code reviews\n📊 **Project management**: Trello, Notion, or Linear\n🤝 **Code standards**: Consistent formatting and conventions\n\nAre you leading a team or joining one?";
    }

    // React Flow and tool-specific advice
    if (lowerInput.includes('react flow') || lowerInput.includes('workflow') || lowerInput.includes('visual')) {
      return "React Flow is fantastic for visual workflows! Here's how to make the most of it:\n\n🎨 **Custom nodes**: Create nodes that match your domain\n🔗 **Smart connections**: Validate connections between node types\n💾 **Save/load**: Let users save their workflows\n📱 **Responsive**: Make sure it works on different screen sizes\n⚡ **Performance**: Use React.memo for complex workflows\n\nWhat kind of workflow are you visualizing?";
    }

    // Encouragement and motivation
    if (lowerInput.includes('difficult') || lowerInput.includes('hard') || lowerInput.includes('frustrated')) {
      return "I hear you - coding can be challenging! Remember:\n\n💪 **Every expert was once a beginner**\n🎯 **Break big problems into tiny pieces**\n🎉 **Celebrate small wins**\n🤝 **It's okay to ask for help**\n🔄 **Debugging is a skill - you're getting better**\n\nYou've got this! What's the specific challenge you're facing?";
    }

    // Default conversational response
    const responses = [
      "That's interesting! Tell me more about what you're working on. I'm here to help with advice, suggestions, and problem-solving.",
      "I'd love to help! What specific aspect of your project or coding journey can I assist with?",
      "Great question! I'm here to provide guidance on development, design, project management, and technical decisions. What's on your mind?",
      "I'm here to be your coding advisor! Whether it's technical choices, project planning, or just brainstorming - what can I help with?",
      "Sounds like you're working on something exciting! I can offer advice on architecture, tools, best practices, or just be a sounding board. What's up?"
    ];

    return responses[Math.floor(Math.random() * responses.length)];
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
          <div className="bg-gray-800 rounded-lg w-96 h-96 flex flex-col border border-gray-700">
            {/* Chat Header */}
            <div className="flex justify-between items-center p-4 border-b border-gray-700">
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
            <div className="flex-1 p-4 overflow-y-auto bg-gray-800" id="chat-messages">
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
            <div className="p-4 border-t border-gray-600">
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

import React, { useState, useRef, useCallback } from 'react';
import './index.css';

const agents = [
  {
    id: 'analyst',
    name: 'Document Analyst',
    description: 'Document analysis',
    color: 'bg-cyan-500',
    icon: '🔍',
    position: { x: 100, y: 200 }
  },
  {
    id: 'pm',
    name: 'Product Manager', 
    description: 'Requirements extraction',
    color: 'bg-emerald-500',
    icon: '👥',
    position: { x: 350, y: 200 }
  },
  {
    id: 'taskmanager',
    name: 'Task Manager',
    description: 'Task breakdown',
    color: 'bg-amber-500', 
    icon: '📋',
    position: { x: 600, y: 200 }
  },
  {
    id: 'scrum',
    name: 'PO/Scrum Master',
    description: 'Final approval',
    color: 'bg-violet-500',
    icon: '🛡️',
    position: { x: 850, y: 200 }
  }
];

const connections = [
  { from: 'analyst', to: 'pm' },
  { from: 'pm', to: 'taskmanager' },
  { from: 'taskmanager', to: 'scrum' }
];

export default function App() {
  const [selectedNode, setSelectedNode] = useState(null);
  const [nodePositions, setNodePositions] = useState(
    Object.fromEntries(agents.map(agent => [agent.id, agent.position]))
  );
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const canvasRef = useRef(null);

  const handleMouseDown = useCallback((e, nodeId) => {
    e.preventDefault();
    const rect = canvasRef.current.getBoundingClientRect();
    const nodePos = nodePositions[nodeId];
    setDragOffset({
      x: e.clientX - rect.left - nodePos.x,
      y: e.clientY - rect.top - nodePos.y
    });
    setIsDragging(nodeId);
    setSelectedNode(nodeId);
  }, [nodePositions]);

  const handleMouseMove = useCallback((e) => {
    if (!isDragging) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const newX = e.clientX - rect.left - dragOffset.x;
    const newY = e.clientY - rect.top - dragOffset.y;
    
    setNodePositions(prev => ({
      ...prev,
      [isDragging]: { x: Math.max(0, newX), y: Math.max(0, newY) }
    }));
  }, [isDragging, dragOffset]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  const getConnectionPath = (fromId, toId) => {
    const fromPos = nodePositions[fromId];
    const toPos = nodePositions[toId];
    
    const startX = fromPos.x + 120;
    const startY = fromPos.y + 40;
    const endX = toPos.x;
    const endY = toPos.y + 40;
    
    const midX = (startX + endX) / 2;
    
    return `M ${startX} ${startY} C ${midX} ${startY}, ${midX} ${endY}, ${endX} ${endY}`;
  };

  const selectedAgent = selectedNode ? agents.find(a => a.id === selectedNode) : null;

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Left Sidebar */}
      <div className="w-64 bg-gray-800 border-r border-gray-700 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 bg-blue-500 rounded flex items-center justify-center text-white font-bold">
              X
            </div>
            <span className="font-bold">X-Flow</span>
          </div>
          <div className="flex gap-2">
            <button className="bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded text-sm">
              + New
            </button>
            <button className="bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded text-sm">
              💾 Save
            </button>
            <button className="bg-gray-700 hover:bg-gray-600 px-3 py-1 rounded text-sm">
              📤 Export
            </button>
          </div>
        </div>

        {/* Database Node */}
        <div className="p-4 border-b border-gray-700">
          <div className="bg-red-100 border border-red-300 rounded p-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-red-500 rounded flex items-center justify-center text-white">
                🗄️
              </div>
              <div>
                <div className="font-medium text-red-800">Database</div>
                <div className="text-sm text-red-600">Query/Store data</div>
              </div>
            </div>
          </div>
        </div>

        {/* X-Agents Section */}
        <div className="flex-1 p-4">
          <h3 className="text-sm font-medium text-gray-400 mb-3">X-AGENTS (FAB 4)</h3>
          <div className="space-y-3">
            {agents.map(agent => (
              <div
                key={agent.id}
                className={`p-3 rounded border ${
                  selectedNode === agent.id 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-600 bg-gray-700'
                } cursor-pointer hover:bg-gray-600`}
                onClick={() => setSelectedNode(agent.id)}
              >
                <div className="flex items-center gap-2">
                  <div className={`w-8 h-8 ${agent.color} rounded flex items-center justify-center text-white`}>
                    {agent.icon}
                  </div>
                  <div>
                    <div className="font-medium">{agent.name}</div>
                    <div className="text-sm text-gray-400">{agent.description}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Canvas Area */}
      <div className="flex-1 flex">
        <div className="flex-1 relative overflow-hidden">
          <svg
            ref={canvasRef}
            className="absolute inset-0 w-full h-full cursor-grab"
            style={{
              backgroundImage: `
                radial-gradient(circle, #374151 1px, transparent 1px)
              `,
              backgroundSize: '20px 20px'
            }}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            {/* Connection Lines */}
            {connections.map((conn, i) => (
              <path
                key={i}
                d={getConnectionPath(conn.from, conn.to)}
                stroke="#6b7280"
                strokeWidth="2"
                fill="none"
                markerEnd="url(#arrowhead)"
              />
            ))}
            
            {/* Arrow Marker */}
            <defs>
              <marker
                id="arrowhead"
                markerWidth="10"
                markerHeight="7"
                refX="9"
                refY="3.5"
                orient="auto"
              >
                <polygon
                  points="0 0, 10 3.5, 0 7"
                  fill="#6b7280"
                />
              </marker>
            </defs>

            {/* Agent Nodes */}
            {agents.map(agent => {
              const pos = nodePositions[agent.id];
              return (
                <g key={agent.id}>
                  <foreignObject
                    x={pos.x}
                    y={pos.y}
                    width="120"
                    height="80"
                    className="cursor-move"
                    onMouseDown={(e) => handleMouseDown(e, agent.id)}
                  >
                    <div className={`
                      w-full h-full border-2 rounded-lg p-3 bg-gray-800 text-white
                      ${selectedNode === agent.id ? 'border-blue-500' : 'border-gray-600'}
                      hover:border-gray-500
                    `}>
                      <div className="flex items-center gap-2 mb-1">
                        <div className={`w-6 h-6 ${agent.color} rounded flex items-center justify-center text-sm`}>
                          {agent.icon}
                        </div>
                        <div className="text-xs font-medium truncate">{agent.name}</div>
                      </div>
                      <div className="text-xs text-gray-400">{agent.description}</div>
                      
                      {/* Connection Handles */}
                      <div className="absolute -right-1 top-1/2 w-2 h-2 bg-gray-500 rounded-full transform -translate-y-1/2"></div>
                      <div className="absolute -left-1 top-1/2 w-2 h-2 bg-gray-500 rounded-full transform -translate-y-1/2"></div>
                    </div>
                  </foreignObject>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Right Properties Panel */}
        <div className="w-80 bg-gray-800 border-l border-gray-700 p-4">
          {selectedAgent ? (
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className={`w-8 h-8 ${selectedAgent.color} rounded flex items-center justify-center text-white`}>
                  {selectedAgent.icon}
                </div>
                <h3 className="font-medium">{selectedAgent.name}</h3>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Agent Type
                  </label>
                  <input
                    type="text"
                    value={selectedAgent.name}
                    className="w-full bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white"
                    readOnly
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Description
                  </label>
                  <textarea
                    value={selectedAgent.description}
                    className="w-full bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white h-20"
                    readOnly
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">
                    Status
                  </label>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-sm">Ready</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-400 mt-20">
              <div className="w-16 h-16 border-2 border-gray-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                <div className="w-8 h-8 border border-gray-600 rounded-full"></div>
              </div>
              <h3 className="font-medium mb-2">No Node Selected</h3>
              <p className="text-sm">Select a node to view and edit its properties</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

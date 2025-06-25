
import React, { useState, useCallback, useRef } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType,
  Handle,
  Position,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './App.css';
import InputPanel from './InputPanel';
import ResultsPanel from './ResultsPanel';

// Custom Node Components
const AnalystNode = ({ data, selected }) => (
  <div className={`px-4 py-2 shadow-md rounded-md bg-blue-500 border-2 ${selected ? 'border-blue-700' : 'border-blue-600'} min-w-[150px]`}>
    <Handle type="target" position={Position.Left} id="input" />
    <div className="flex items-center">
      <div className="ml-2">
        <div className="text-lg font-bold text-white">📊 Analyst</div>
        <div className="text-white text-sm">{data.label}</div>
      </div>
    </div>
    <div className="text-xs text-blue-100 mt-1">{data.description}</div>
    <Handle type="source" position={Position.Right} id="output" />
  </div>
);

const ProductManagerNode = ({ data, selected }) => (
  <div className={`px-4 py-2 shadow-md rounded-md bg-green-500 border-2 ${selected ? 'border-green-700' : 'border-green-600'} min-w-[150px]`}>
    <Handle type="target" position={Position.Left} id="input" />
    <Handle type="target" position={Position.Top} id="feedback" />
    <div className="flex items-center">
      <div className="ml-2">
        <div className="text-lg font-bold text-white">📋 Product Manager</div>
        <div className="text-white text-sm">{data.label}</div>
      </div>
    </div>
    <div className="text-xs text-green-100 mt-1">{data.description}</div>
    <Handle type="source" position={Position.Bottom} id="output" />
  </div>
);

const TaskManagerNode = ({ data, selected }) => (
  <div className={`px-4 py-2 shadow-md rounded-md bg-purple-500 border-2 ${selected ? 'border-purple-700' : 'border-purple-600'} min-w-[150px]`}>
    <Handle type="target" position={Position.Top} id="input" />
    <div className="flex items-center">
      <div className="ml-2">
        <div className="text-lg font-bold text-white">📝 Task Manager</div>
        <div className="text-white text-sm">{data.label}</div>
      </div>
    </div>
    <div className="text-xs text-purple-100 mt-1">{data.description}</div>
    <Handle type="source" position={Position.Right} id="output" />
  </div>
);

const ScrumMasterNode = ({ data, selected }) => (
  <div className={`px-4 py-2 shadow-md rounded-md bg-orange-500 border-2 ${selected ? 'border-orange-700' : 'border-orange-600'} min-w-[150px]`}>
    <Handle type="target" position={Position.Left} id="input" />
    <div className="flex items-center">
      <div className="ml-2">
        <div className="text-lg font-bold text-white">🎯 Scrum Master</div>
        <div className="text-white text-sm">{data.label}</div>
      </div>
    </div>
    <div className="text-xs text-orange-100 mt-1">{data.description}</div>
    <Handle type="source" position={Position.Bottom} id="feedback" />
    <Handle type="source" position={Position.Right} id="output" />
  </div>
);

const InputNode = ({ data, selected }) => (
  <div className={`px-4 py-2 shadow-md rounded-md bg-gray-600 border-2 ${selected ? 'border-gray-800' : 'border-gray-700'} min-w-[150px]`}>
    <div className="flex items-center">
      <div className="ml-2">
        <div className="text-lg font-bold text-white">📥 Input</div>
        <div className="text-white text-sm">{data.label}</div>
      </div>
    </div>
    <div className="text-xs text-gray-200 mt-1">{data.description}</div>
    <Handle type="source" position={Position.Right} id="output" />
  </div>
);

const OutputNode = ({ data, selected }) => (
  <div className={`px-4 py-2 shadow-md rounded-md bg-red-500 border-2 ${selected ? 'border-red-700' : 'border-red-600'} min-w-[150px]`}>
    <Handle type="target" position={Position.Top} id="input" />
    <div className="flex items-center">
      <div className="ml-2">
        <div className="text-lg font-bold text-white">📤 Output</div>
        <div className="text-white text-sm">{data.label}</div>
      </div>
    </div>
    <div className="text-xs text-red-100 mt-1">{data.description}</div>
  </div>
);

// Node types - defined outside component to prevent React Flow warnings
const nodeTypes = {
  analyst: AnalystNode,
  productManager: ProductManagerNode,
  taskManager: TaskManagerNode,
  scrumMaster: ScrumMasterNode,
  input: InputNode,
  output: OutputNode,
};

// Node Palette Data
const nodeTypesData = [
  {
    category: "Core Agents",
    nodes: [
      {
        type: "analyst",
        label: "Document Analyst",
        description: "Analyzes documents and extracts insights",
        icon: "📊",
        gradient: "from-blue-400 to-blue-600"
      },
      {
        type: "productManager",
        label: "Product Manager", 
        description: "Extracts and manages requirements",
        icon: "📋",
        gradient: "from-green-400 to-green-600"
      },
      {
        type: "taskManager",
        label: "Task Manager",
        description: "Breaks down requirements into tasks",
        icon: "📝",
        gradient: "from-purple-400 to-purple-600"
      },
      {
        type: "scrumMaster",
        label: "Scrum Master",
        description: "Reviews and approves with feedback",
        icon: "🎯",
        gradient: "from-orange-400 to-orange-600"
      }
    ]
  },
  {
    category: "I/O",
    nodes: [
      {
        type: "input",
        label: "Input Node",
        description: "Data input point",
        icon: "📥",
        gradient: "from-gray-400 to-gray-600"
      },
      {
        type: "output",
        label: "Output Node",
        description: "Data output point", 
        icon: "📤",
        gradient: "from-red-400 to-red-600"
      }
    ]
  }
];

// Node Palette Component
const NodePalette = () => {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredNodeTypes = nodeTypesData.map(category => ({
    ...category,
    nodes: category.nodes.filter(node =>
      node.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
      node.description.toLowerCase().includes(searchTerm.toLowerCase())
    ),
  })).filter(category => category.nodes.length > 0);

  const handleDragStart = (event, nodeType) => {
    event.dataTransfer.setData("application/reactflow", JSON.stringify({
      type: nodeType.type,
      label: nodeType.label,
      description: nodeType.description,
    }));
    event.dataTransfer.effectAllowed = "move";
  };

  return (
    <aside className="w-64 bg-white border-r border-slate-200 overflow-y-auto">
      <div className="p-4">
        <div className="mb-4">
          <h2 className="text-sm font-semibold text-slate-800 mb-3">Agent Nodes</h2>
          <div className="relative">
            <input
              type="text"
              placeholder="Search nodes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-8 pr-3 py-2 border border-gray-300 rounded-md text-sm"
            />
            <div className="absolute left-2.5 top-2.5 h-4 w-4 text-slate-400">🔍</div>
          </div>
        </div>

        {filteredNodeTypes.map((category) => (
          <div key={category.category} className="mb-6">
            <h3 className="text-xs font-medium text-slate-600 uppercase tracking-wide mb-2">
              {category.category}
            </h3>
            <div className="space-y-2">
              {category.nodes.map((node) => (
                <div
                  key={node.type}
                  className={`p-3 border border-slate-200 rounded-lg bg-gradient-to-r ${node.gradient} cursor-grab active:cursor-grabbing transition-all duration-200 hover:scale-[1.02] hover:shadow-md`}
                  draggable
                  onDragStart={(e) => handleDragStart(e, node)}
                >
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
                      <span className="text-white text-xs">{node.icon}</span>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-white">{node.label}</div>
                      <div className="text-xs text-white text-opacity-80">{node.description}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
};

const initialNodes = [
  {
    id: '1',
    type: 'input',
    position: { x: 50, y: 50 },
    data: { label: 'Input Document', description: 'Project requirements input' },
  },
  {
    id: '2',
    type: 'analyst',
    position: { x: 300, y: 50 },
    data: { label: 'Document Analyst', description: 'Analyzes documents and extracts insights' },
  },
  {
    id: '3',
    type: 'productManager',
    position: { x: 550, y: 50 },
    data: { label: 'Product Manager', description: 'Extracts and manages requirements' },
  },
  {
    id: '4',
    type: 'taskManager',
    position: { x: 300, y: 200 },
    data: { label: 'Task Manager', description: 'Breaks down requirements into tasks' },
  },
  {
    id: '5',
    type: 'scrumMaster',
    position: { x: 550, y: 200 },
    data: { label: 'Scrum Master', description: 'Reviews and approves with feedback' },
  },
  {
    id: '6',
    type: 'output',
    position: { x: 300, y: 350 },
    data: { label: 'Final Output', description: 'Processed tasks and feedback' },
  },
];

const initialEdges = [
  {
    id: 'e1-2',
    source: '1',
    target: '2',
    sourceHandle: 'output',
    targetHandle: 'input',
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'e2-3',
    source: '2',
    target: '3',
    sourceHandle: 'output',
    targetHandle: 'input',
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'e3-4',
    source: '3',
    target: '4',
    sourceHandle: 'output',
    targetHandle: 'input',
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'e4-5',
    source: '4',
    target: '5',
    sourceHandle: 'output',
    targetHandle: 'input',
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: 'e5-3',
    source: '5',
    target: '3',
    sourceHandle: 'feedback',
    targetHandle: 'feedback',
    markerEnd: { type: MarkerType.ArrowClosed },
    style: { stroke: '#f59e0b' },
    label: 'feedback',
  },
  {
    id: 'e5-6',
    source: '5',
    target: '6',
    sourceHandle: 'output',
    targetHandle: 'input',
    markerEnd: { type: MarkerType.ArrowClosed },
  },
];

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [resultData, setResultData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({ ...params, markerEnd: { type: MarkerType.ArrowClosed } }, eds)),
    [],
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      const nodeData = JSON.parse(event.dataTransfer.getData('application/reactflow'));

      if (typeof nodeData === 'undefined' || !nodeData) {
        return;
      }

      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const newNode = {
        id: `${nodes.length + 1}`,
        type: nodeData.type,
        position,
        data: { label: nodeData.label, description: nodeData.description },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, nodes],
  );

  const onSelectionChange = useCallback((elements) => {
    setSelectedNodes(elements.nodes || []);
  }, []);

  const deleteSelectedNodes = useCallback(() => {
    if (selectedNodes.length > 0) {
      const selectedNodeIds = selectedNodes.map(node => node.id);
      setNodes((nds) => nds.filter(node => !selectedNodeIds.includes(node.id)));
      setEdges((eds) => eds.filter(edge => 
        !selectedNodeIds.includes(edge.source) && !selectedNodeIds.includes(edge.target)
      ));
      setSelectedNodes([]);
    }
  }, [selectedNodes, setNodes, setEdges]);

  // Handle keyboard events for deletion
  React.useEffect(() => {
    const handleKeyDown = (event) => {
      if ((event.key === 'Delete' || event.key === 'Backspace') && selectedNodes.length > 0) {
        deleteSelectedNodes();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [deleteSelectedNodes, selectedNodes]);

  const handleRunPipeline = async (inputText) => {
    setIsLoading(true);
    setResultData(null);

    try {
      const response = await fetch('/api/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ document: inputText })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();
        setResultData(JSON.stringify(data, null, 2));
      } else {
        // Handle XML/text response from Flask backend
        const textData = await response.text();
        setResultData(textData);
      }
    } catch (error) {
      console.error('Error:', error);
      setResultData(`Error: ${error.message}\n\nMake sure the Flask backend is running on port 5002`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-80 flex flex-col">
        <InputPanel onRunPipeline={handleRunPipeline} isLoading={isLoading} />
        <ResultsPanel resultData={resultData} isLoading={isLoading} />
      </div>
      
      <NodePalette />
      
      <div className="flex-1 relative h-screen">
        <div className="absolute top-4 right-4 z-10 flex gap-2">
          {selectedNodes.length > 0 && (
            <button
              onClick={deleteSelectedNodes}
              className="px-3 py-2 bg-red-600 hover:bg-red-700 text-white text-sm rounded shadow"
            >
              Delete Selected ({selectedNodes.length})
            </button>
          )}
        </div>
        
        <div className="w-full h-full" ref={reactFlowWrapper}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onInit={setReactFlowInstance}
            onDrop={onDrop}
            onDragOver={onDragOver}
            onSelectionChange={onSelectionChange}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="top-right"
          >
            <MiniMap />
            <Controls />
            <Background color="#aaa" gap={16} />
          </ReactFlow>
        </div>
      </div>
    </div>
  );
}

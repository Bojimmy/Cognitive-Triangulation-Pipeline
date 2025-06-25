
import React from 'react';

const ResultsPanel = ({ resultData, isLoading }) => {
  // Parse XML result if available
  const parseXMLResult = (xmlString) => {
    if (!xmlString) return null;
    
    try {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlString, 'text/xml');
      
      // Check if it's the new comprehensive format
      const completeResult = xmlDoc.querySelector('CompletePipelineResult');
      if (completeResult) {
        return {
          type: 'complete',
          status: completeResult.querySelector('Status')?.textContent,
          iterations: completeResult.querySelector('Iterations')?.textContent,
          domain: completeResult.querySelector('Domain')?.textContent,
          complexity: completeResult.querySelector('Complexity')?.textContent,
          requirements: Array.from(completeResult.querySelectorAll('Requirements Requirement')).map(req => ({
            id: req.getAttribute('id'),
            priority: req.getAttribute('priority'),
            title: req.textContent
          })),
          tasks: Array.from(completeResult.querySelectorAll('TaskBreakdown Task')).map(task => ({
            id: task.getAttribute('id'),
            reqId: task.getAttribute('req_id'),
            points: task.getAttribute('points'),
            hours: task.getAttribute('hours'),
            priority: task.getAttribute('priority'),
            title: task.textContent
          })),
          totalTasks: completeResult.querySelector('TotalTasks')?.textContent,
          storyPoints: completeResult.querySelector('StoryPoints')?.textContent,
          expansionRatio: completeResult.querySelector('ExpansionRatio')?.textContent,
          approved: completeResult.querySelector('Decision')?.getAttribute('approved') === 'true',
          qualityScore: completeResult.querySelector('QualityScore')?.textContent,
          riskLevel: completeResult.querySelector('RiskLevel')?.textContent,
          feedback: completeResult.querySelector('Feedback')?.textContent
        };
      }
      
      // Fallback to legacy format
      const decision = xmlDoc.querySelector('Decision');
      if (decision) {
        return {
          type: 'legacy',
          approved: decision.getAttribute('approved') === 'true',
          qualityScore: xmlDoc.querySelector('QualityScore')?.textContent,
          riskLevel: xmlDoc.querySelector('RiskLevel')?.textContent,
          totalTasks: xmlDoc.querySelector('TotalTasks')?.textContent,
          storyPoints: xmlDoc.querySelector('StoryPoints')?.textContent,
          feedback: xmlDoc.querySelector('Feedback')?.textContent
        };
      }
    } catch (error) {
      console.error('Error parsing XML:', error);
    }
    
    return null;
  };

  const parsedResult = parseXMLResult(resultData);

  const downloadTaskBreakdown = () => {
    if (!parsedResult || parsedResult.type !== 'complete') return;
    
    let content = `# Project Task Breakdown\n\n`;
    content += `**Status:** ${parsedResult.status}\n`;
    content += `**Domain:** ${parsedResult.domain}\n`;
    content += `**Iterations:** ${parsedResult.iterations}\n`;
    content += `**Total Tasks:** ${parsedResult.totalTasks}\n`;
    content += `**Story Points:** ${parsedResult.storyPoints}\n`;
    content += `**Quality Score:** ${parsedResult.qualityScore}\n`;
    content += `**Risk Level:** ${parsedResult.riskLevel}\n\n`;
    
    content += `## Requirements (${parsedResult.requirements.length})\n\n`;
    parsedResult.requirements.forEach(req => {
      content += `- **${req.id}** [${req.priority}]: ${req.title}\n`;
    });
    
    content += `\n## Task Breakdown (${parsedResult.tasks.length} tasks)\n\n`;
    parsedResult.tasks.forEach(task => {
      content += `### ${task.id} - ${task.title}\n`;
      content += `- **Requirement:** ${task.reqId}\n`;
      content += `- **Story Points:** ${task.points}\n`;
      content += `- **Hours:** ${task.hours}\n`;
      content += `- **Priority:** ${task.priority}\n\n`;
    });
    
    content += `## Feedback\n${parsedResult.feedback}\n`;
    
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `project-breakdown-${new Date().toISOString().slice(0, 10)}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex-1 bg-gray-700 text-gray-200 overflow-hidden flex flex-col">
      <div className="p-4 border-b border-gray-700 flex justify-between items-center">
        <h3 className="text-lg font-semibold text-white">Pipeline Results</h3>
        {parsedResult && parsedResult.type === 'complete' && (
          <button
            onClick={downloadTaskBreakdown}
            className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg flex items-center space-x-2"
          >
            <span>📄</span>
            <span>Download Breakdown</span>
          </button>
        )}
      </div>

      <div className="flex-1 p-4 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
              <div className="text-sm text-gray-400">Processing with X-Agents...</div>
            </div>
          </div>
        ) : parsedResult ? (
          <div className="space-y-4">
            {/* Pipeline Status */}
            <div className="bg-gray-800 p-4 rounded-lg">
              <h4 className="text-sm font-semibold text-white mb-3">Pipeline Status</h4>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="text-gray-400 text-sm">Status:</span>
                  <div className={`text-lg font-semibold ${parsedResult.approved ? 'text-green-400' : 'text-red-400'}`}>
                    {parsedResult.status || (parsedResult.approved ? 'APPROVED' : 'REJECTED')}
                  </div>
                </div>
                <div>
                  <span className="text-gray-400 text-sm">Quality Score:</span>
                  <div className="text-lg font-semibold text-blue-400">{parsedResult.qualityScore}</div>
                </div>
                {parsedResult.iterations && (
                  <div>
                    <span className="text-gray-400 text-sm">Iterations:</span>
                    <div className="text-lg font-semibold text-yellow-400">{parsedResult.iterations}</div>
                  </div>
                )}
                <div>
                  <span className="text-gray-400 text-sm">Risk Level:</span>
                  <div className={`text-lg font-semibold ${
                    parsedResult.riskLevel === 'low' ? 'text-green-400' : 
                    parsedResult.riskLevel === 'medium' ? 'text-yellow-400' : 'text-red-400'
                  }`}>{parsedResult.riskLevel}</div>
                </div>
              </div>
            </div>

            {/* Project Summary */}
            {parsedResult.type === 'complete' && (
              <div className="bg-gray-800 p-4 rounded-lg">
                <h4 className="text-sm font-semibold text-white mb-3">Project Summary</h4>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <span className="text-gray-400 text-sm">Domain:</span>
                    <div className="text-white font-medium">{parsedResult.domain}</div>
                  </div>
                  <div>
                    <span className="text-gray-400 text-sm">Story Points:</span>
                    <div className="text-blue-400 font-medium">{parsedResult.storyPoints}</div>
                  </div>
                  <div>
                    <span className="text-gray-400 text-sm">Total Tasks:</span>
                    <div className="text-purple-400 font-medium">{parsedResult.totalTasks}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Requirements */}
            {parsedResult.type === 'complete' && parsedResult.requirements.length > 0 && (
              <div className="bg-gray-800 p-4 rounded-lg">
                <h4 className="text-sm font-semibold text-white mb-3">
                  Requirements ({parsedResult.requirements.length})
                </h4>
                <div className="space-y-2">
                  {parsedResult.requirements.map((req, index) => (
                    <div key={index} className="flex items-start space-x-3 p-2 bg-gray-900 rounded">
                      <span className={`px-2 py-1 text-xs rounded font-medium ${
                        req.priority === 'high' ? 'bg-red-600 text-white' :
                        req.priority === 'medium' ? 'bg-yellow-600 text-white' : 'bg-green-600 text-white'
                      }`}>
                        {req.priority}
                      </span>
                      <div className="flex-1">
                        <div className="text-sm font-medium text-blue-300">{req.id}</div>
                        <div className="text-sm text-gray-300">{req.title}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Task Breakdown */}
            {parsedResult.type === 'complete' && parsedResult.tasks.length > 0 && (
              <div className="bg-gray-800 p-4 rounded-lg">
                <h4 className="text-sm font-semibold text-white mb-3">
                  Task Breakdown ({parsedResult.tasks.length} tasks)
                </h4>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {parsedResult.tasks.map((task, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-900 rounded">
                      <div className="flex-shrink-0">
                        <div className="text-xs font-medium text-purple-300">{task.id}</div>
                        <div className="text-xs text-gray-500">{task.reqId}</div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm text-gray-200 truncate">{task.title}</div>
                        <div className="flex space-x-4 mt-1">
                          <span className="text-xs text-blue-400">{task.points} pts</span>
                          <span className="text-xs text-green-400">{task.hours}h</span>
                          <span className={`text-xs ${
                            task.priority === 'high' ? 'text-red-400' :
                            task.priority === 'medium' ? 'text-yellow-400' : 'text-green-400'
                          }`}>{task.priority}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Feedback */}
            <div className="bg-gray-800 p-4 rounded-lg">
              <h4 className="text-sm font-semibold text-white mb-3">
                {parsedResult.approved ? 'Approval' : 'Feedback'}
              </h4>
              <div className={`p-3 rounded ${
                parsedResult.approved ? 'bg-green-900 border border-green-700' : 'bg-red-900 border border-red-700'
              }`}>
                <div className="text-sm text-gray-200">{parsedResult.feedback}</div>
              </div>
            </div>

            {/* Raw XML (collapsible) */}
            <details className="bg-gray-800 p-4 rounded-lg">
              <summary className="text-sm font-semibold text-white cursor-pointer mb-3">
                Raw XML Output
              </summary>
              <pre className="text-sm text-gray-300 whitespace-pre-wrap font-mono max-h-64 overflow-y-auto bg-gray-900 p-3 rounded">
                {resultData}
              </pre>
            </details>

            {/* Interactive Chat Hint */}
            {!parsedResult.approved && (
              <div className="bg-blue-900 border border-blue-700 p-4 rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-blue-400">💡</span>
                  <span className="text-sm font-semibold text-blue-300">Need Help?</span>
                </div>
                <p className="text-sm text-blue-200">
                  Use the 💬 Chat tab to discuss requirements with the AI advisor and refine your project scope.
                </p>
              </div>
            )}
          </div>
        ) : resultData ? (
          // Fallback for non-XML or unparseable results
          <div className="bg-gray-800 p-4 rounded-lg">
            <h4 className="text-sm font-semibold text-white mb-3">Raw Results</h4>
            <pre className="text-sm text-gray-200 whitespace-pre-wrap font-mono max-h-96 overflow-y-auto">
              {resultData}
            </pre>
          </div>
        ) : (
          <div className="text-center text-gray-500 mt-8">
            <div className="text-4xl mb-4">🤖</div>
            <div className="text-lg mb-2">X-Agent Pipeline Ready</div>
            <div className="text-sm">Submit a document to see agent processing results</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsPanel;

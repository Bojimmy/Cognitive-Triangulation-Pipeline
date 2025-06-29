"""
Base Agent Template for X-Agent Pipeline

Use this template when creating new agents for the pipeline.
Follow this pattern for consistency and easy integration.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
from lxml import etree


class BaseXAgent(ABC):
    """Base X-Agent with XML processing and performance tracking"""

    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.metrics = {'total_time': 0.0}

    def process(self, input_xml: str) -> str:
        """Main processing with timing"""
        start_time = time.time()

        # Parse input
        parsed = etree.fromstring(input_xml.encode())

        # Process with agent intelligence
        result = self._process_intelligence(parsed)

        # Generate output XML
        output_xml = self._generate_xml(result)

        self.metrics['total_time'] = float((time.time() - start_time) * 1000)
        return output_xml

    @abstractmethod
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Agent-specific processing logic"""
        pass

    @abstractmethod
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output for next agent"""
        pass


# Example implementation (delete when creating real agent)
class ExampleAgent(BaseXAgent):
    """Template example - replace with your agent logic"""
    
    def __init__(self):
        super().__init__("ExampleAgent")
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Your agent's core logic goes here"""
        # Extract data from parsed XML
        # Process with your agent's intelligence  
        # Return dictionary with results
        return {
            'result': 'example_output',
            'confidence': 0.95
        }
    
    def _generate_xml(self, result: dict) -> str:
        """Generate XML for next agent in pipeline"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<ExampleOutput>
    <Result>{result['result']}</Result>
    <Confidence>{result['confidence']}</Confidence>
</ExampleOutput>"""

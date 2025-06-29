"""
Customer Service Agent for X-Agent Pipeline
Specializes in customer support ticket processing and response generation
"""

from agents.agent_template import BaseXAgent
from lxml import etree


class CustomerServiceXAgent(BaseXAgent):
    """Specialized agent for customer service workflows"""
    
    def __init__(self):
        super().__init__("CustomerServiceXAgent")
        self.priority_keywords = ['urgent', 'critical', 'escalate', 'complaint']
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Process customer service tickets"""
        # Extract ticket content
        content_elem = parsed_input.find('.//Content')
        content = content_elem.text if content_elem is not None else ""
        
        # Analyze priority
        priority = self._analyze_priority(content)
        
        # Extract customer info
        customer_info = self._extract_customer_info(content)
        
        # Generate response suggestions
        response_suggestions = self._generate_responses(content, priority)
        
        return {
            'priority': priority,
            'customer_info': customer_info,
            'response_suggestions': response_suggestions,
            'processing_time': '2ms'
        }
    
    def _analyze_priority(self, content: str) -> str:
        """Analyze ticket priority"""
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in self.priority_keywords):
            return 'high'
        elif 'refund' in content_lower or 'billing' in content_lower:
            return 'medium'
        else:
            return 'low'
    
    def _extract_customer_info(self, content: str) -> dict:
        """Extract customer information"""
        # Simple extraction - can be enhanced
        return {
            'type': 'individual' if '@gmail.com' in content else 'business',
            'sentiment': 'positive' if 'thanks' in content.lower() else 'neutral'
        }
    
    def _generate_responses(self, content: str, priority: str) -> list:
        """Generate response suggestions"""
        base_responses = [
            "Thank you for contacting us. We're reviewing your request.",
            "We understand your concern. Let me help you with this.",
            "I've escalated this to our specialist team."
        ]
        
        if priority == 'high':
            return ["URGENT: " + resp for resp in base_responses[:2]]
        else:
            return base_responses
    
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output for next agent"""
        responses_xml = '\n'.join([
            f'        <Response>{resp}</Response>' 
            for resp in result['response_suggestions']
        ])
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<CustomerServiceAnalysis>
    <Priority>{result['priority']}</Priority>
    <CustomerType>{result['customer_info']['type']}</CustomerType>
    <Sentiment>{result['customer_info']['sentiment']}</Sentiment>
    <ResponseSuggestions>
{responses_xml}
    </ResponseSuggestions>
    <ProcessingTime>{result['processing_time']}</ProcessingTime>
</CustomerServiceAnalysis>"""

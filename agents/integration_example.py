"""
Integration Example: How to add new agents to main.py pipeline

This shows how to import and use agents from the new agents/ folder structure.
"""

# Example imports for main.py
from agents.specialized.customer_service_agent import CustomerServiceXAgent
from agents.core.analytics_agent import AnalyticsXAgent  # Future agent example

class XAgentPipeline:
    """Updated pipeline with new agent architecture"""
    
    def __init__(self):
        # Existing agents (embedded in main.py for now)
        self.analyst = AnalystXAgent()
        self.product_manager = ProductManagerXAgent() 
        self.task_manager = TaskManagerXAgent()
        self.scrum_master = POScrumMasterXAgent()
        
        # New agents from agents/ folder
        self.customer_service = CustomerServiceXAgent()
        # self.analytics = AnalyticsXAgent()  # Future agent
        
        # Existing separate agents
        try:
            from document_formatter_agent import DocumentFormatterXAgent
            self.document_formatter = DocumentFormatterXAgent()
        except ImportError:
            self.document_formatter = None
    
    def execute_customer_service_workflow(self, ticket_content: str) -> dict:
        """Example: Customer service specific workflow"""
        # Format ticket
        formatted_xml = f'<Ticket><Content>{ticket_content}</Content></Ticket>'
        
        # Process through customer service agent
        cs_result = self.customer_service.process(formatted_xml)
        
        # Could continue through other agents...
        return {'success': True, 'analysis': cs_result}


# Usage example:
# pipeline = XAgentPipeline()
# result = pipeline.execute_customer_service_workflow("URGENT: My account is locked!")

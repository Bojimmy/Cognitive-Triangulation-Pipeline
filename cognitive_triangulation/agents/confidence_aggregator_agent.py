#!/usr/bin/env python3
"""
ConfidenceAggregator Agent with Co-Located Plugins
Fourth agent in the Cognitive Triangulation pipeline - aggregates evidence and calculates confidence scores
"""

import re
import time
import math
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Set
from lxml import etree
from collections import defaultdict, Counter

class BaseXAgent(ABC):
    """Base X-Agent with XML processing and performance tracking"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.metrics = {'total_time': 0.0}
    
    def process(self, input_xml: str) -> str:
        """Parse input → Process → Generate output XML"""
        start_time = time.perf_counter()
        
        try:
            # Parse XML input using lxml
            parsed_input = etree.fromstring(input_xml.encode('utf-8'))
            
            # Process with agent-specific intelligence
            result = self._process_intelligence(parsed_input)
            
            # Generate XML output
            output_xml = self._generate_xml(result)
            
            # Track performance
            end_time = time.perf_counter()
            self.metrics['total_time'] = (end_time - start_time) * 1000
            
            return output_xml
            
        except Exception as e:
            return f"<Error agent='{self.agent_type}'>Error processing: {str(e)}</e>"
    
    @abstractmethod
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Agent-specific logic - implemented by subclasses"""
        pass
    
    @abstractmethod
    def _generate_xml(self, result: dict) -> str:
        """Generate XML for next agent - implemented by subclasses"""
        pass

# ================================
# CONFIDENCE SCORING PLUGINS
# ================================

class BaseConfidencePlugin(ABC):
    """Base class for confidence scoring plugins - co-located"""
    
    @abstractmethod
    def get_scoring_methods(self) -> List[str]:
        """Return the confidence scoring methods this plugin supports"""
        pass
    
    @abstractmethod
    def calculate_relationship_confidence(self, relationship: Dict, all_relationships: List[Dict], 
                                        patterns: List[Dict], context_scores: Dict) -> float:
        """Calculate confidence score for a single relationship"""
        pass
    
    @abstractmethod
    def calculate_pattern_confidence(self, pattern: Dict, all_patterns: List[Dict], 
                                   relationships: List[Dict], context_scores: Dict) -> float:
        """Calculate confidence score for a semantic pattern"""
        pass
    
    @abstractmethod
    def aggregate_evidence_scores(self, evidence_items: List[Dict]) -> Dict[str, float]:
        """Aggregate multiple pieces of evidence into confidence scores"""
        pass
    
    @abstractmethod
    def calculate_overall_confidence(self, relationships: List[Dict], patterns: List[Dict], 
                                   context_scores: Dict) -> Dict[str, float]:
        """Calculate overall confidence metrics for the entire analysis"""
        pass

class MathematicalConfidencePlugin(BaseConfidencePlugin):
    """Mathematical confidence scoring plugin - no LLM needed"""
    
    def __init__(self):
        # Weight different types of evidence
        self.evidence_weights = {
            'DETERMINISTIC': 1.0,      # Direct code analysis
            'STATISTICAL': 0.8,        # Pattern matching
            'SEMANTIC': 0.7,           # Context analysis
            'HEURISTIC': 0.6           # Best guess
        }
        
        # Confidence thresholds
        self.thresholds = {
            'HIGH_CONFIDENCE': 0.8,
            'MEDIUM_CONFIDENCE': 0.6,
            'LOW_CONFIDENCE': 0.4
        }
    
    def get_scoring_methods(self) -> List[str]:
        return ["BAYESIAN", "WEIGHTED_AVERAGE", "EVIDENCE_ACCUMULATION", "STATISTICAL_CORRELATION"]
    
    def calculate_relationship_confidence(self, relationship: Dict, all_relationships: List[Dict], 
                                        patterns: List[Dict], context_scores: Dict) -> float:
        """Calculate confidence for a relationship using multiple mathematical approaches"""
        
        # Base confidence from original detection
        base_confidence = float(relationship.get('confidence', 0.5))
        
        # Evidence strength scoring
        evidence_score = self._score_evidence_strength(relationship)
        
        # Cross-validation with other relationships
        cross_validation_score = self._cross_validate_relationship(relationship, all_relationships)
        
        # Pattern support scoring
        pattern_support_score = self._calculate_pattern_support(relationship, patterns)
        
        # Context alignment scoring
        context_alignment_score = self._calculate_context_alignment(relationship, context_scores)
        
        # Weighted combination using Bayesian-like approach
        confidence_factors = [
            (base_confidence, 0.3),
            (evidence_score, 0.25),
            (cross_validation_score, 0.2),
            (pattern_support_score, 0.15),
            (context_alignment_score, 0.1)
        ]
        
        # Calculate weighted average
        weighted_confidence = sum(score * weight for score, weight in confidence_factors)
        
        # Apply sigmoid normalization to keep in [0,1] range
        normalized_confidence = self._sigmoid_normalize(weighted_confidence)
        
        return min(1.0, max(0.0, normalized_confidence))
    
    def calculate_pattern_confidence(self, pattern: Dict, all_patterns: List[Dict], 
                                   relationships: List[Dict], context_scores: Dict) -> float:
        """Calculate confidence for a semantic pattern"""
        
        base_confidence = float(pattern.get('confidence', 0.5))
        
        # Evidence strength for patterns
        evidence_count = len(pattern.get('evidence', []))
        evidence_score = min(1.0, evidence_count / 3.0)  # Normalize to 3 pieces of evidence
        
        # Pattern frequency scoring (more common patterns get slight boost)
        pattern_type = pattern.get('type', '')
        similar_patterns = [p for p in all_patterns if p.get('type') == pattern_type]
        frequency_score = min(0.2, len(similar_patterns) * 0.05)  # Max 20% boost
        
        # Relationship support (patterns supported by relationships get boost)
        relationship_support = self._calculate_relationship_support_for_pattern(pattern, relationships)
        
        # Context alignment
        context_support = self._calculate_pattern_context_support(pattern, context_scores)
        
        # Combine scores
        final_confidence = (
            base_confidence * 0.4 +
            evidence_score * 0.3 +
            relationship_support * 0.2 +
            context_support * 0.1 +
            frequency_score  # Small boost for frequency
        )
        
        return min(1.0, max(0.0, final_confidence))
    
    def aggregate_evidence_scores(self, evidence_items: List[Dict]) -> Dict[str, float]:
        """Aggregate evidence using multiple mathematical approaches"""
        
        if not evidence_items:
            return {'aggregated_confidence': 0.0, 'evidence_strength': 0.0, 'consensus_score': 0.0}
        
        # Extract confidence scores
        confidences = [float(item.get('confidence', 0.5)) for item in evidence_items]
        
        # Method 1: Weighted average (higher weights for higher confidence)
        weighted_avg = self._calculate_weighted_average(confidences)
        
        # Method 2: Evidence accumulation (more evidence = higher confidence)
        evidence_accumulation = self._calculate_evidence_accumulation(evidence_items)
        
        # Method 3: Consensus scoring (agreement between sources)
        consensus_score = self._calculate_consensus_score(confidences)
        
        # Method 4: Bayesian-like update
        bayesian_score = self._bayesian_evidence_update(confidences)
        
        # Combine methods
        aggregated_confidence = (
            weighted_avg * 0.3 +
            evidence_accumulation * 0.25 +
            consensus_score * 0.25 +
            bayesian_score * 0.2
        )
        
        return {
            'aggregated_confidence': aggregated_confidence,
            'evidence_strength': evidence_accumulation,
            'consensus_score': consensus_score,
            'bayesian_score': bayesian_score,
            'evidence_count': len(evidence_items)
        }
    
    def calculate_overall_confidence(self, relationships: List[Dict], patterns: List[Dict], 
                                   context_scores: Dict) -> Dict[str, float]:
        """Calculate overall confidence metrics for the entire analysis"""
        
        if not relationships and not patterns:
            return {'overall_confidence': 0.0, 'analysis_quality': 0.0, 'reliability_score': 0.0}
        
        # Relationship confidence statistics
        rel_confidences = [float(r.get('confidence', 0.5)) for r in relationships]
        rel_avg_confidence = sum(rel_confidences) / len(rel_confidences) if rel_confidences else 0.0
        rel_consistency = 1.0 - (self._calculate_std_dev(rel_confidences) if rel_confidences else 0.5)
        
        # Pattern confidence statistics
        pattern_confidences = [float(p.get('confidence', 0.5)) for p in patterns]
        pattern_avg_confidence = sum(pattern_confidences) / len(pattern_confidences) if pattern_confidences else 0.0
        pattern_consistency = 1.0 - (self._calculate_std_dev(pattern_confidences) if pattern_confidences else 0.5)
        
        # Coverage metrics
        total_items = len(relationships) + len(patterns)
        high_confidence_items = sum(1 for r in relationships if float(r.get('confidence', 0)) >= self.thresholds['HIGH_CONFIDENCE'])
        high_confidence_items += sum(1 for p in patterns if float(p.get('confidence', 0)) >= self.thresholds['HIGH_CONFIDENCE'])
        
        coverage_score = high_confidence_items / total_items if total_items > 0 else 0.0
        
        # Context alignment score
        context_alignment = context_scores.get('overall_context', 0.0)
        
        # Calculate overall metrics
        analysis_quality = (
            rel_avg_confidence * 0.3 +
            pattern_avg_confidence * 0.2 +
            coverage_score * 0.3 +
            context_alignment * 0.2
        )
        
        reliability_score = (
            rel_consistency * 0.4 +
            pattern_consistency * 0.3 +
            coverage_score * 0.3
        )
        
        overall_confidence = (
            analysis_quality * 0.6 +
            reliability_score * 0.4
        )
        
        return {
            'overall_confidence': overall_confidence,
            'analysis_quality': analysis_quality,
            'reliability_score': reliability_score,
            'coverage_score': coverage_score,
            'relationship_avg_confidence': rel_avg_confidence,
            'pattern_avg_confidence': pattern_avg_confidence,
            'high_confidence_ratio': coverage_score
        }
    
    def _score_evidence_strength(self, relationship: Dict) -> float:
        """Score the strength of evidence for a relationship"""
        evidence = relationship.get('evidence', '')
        
        # Count evidence indicators
        evidence_indicators = len(evidence.split(';')) if evidence else 1
        
        # More evidence = higher confidence (with diminishing returns)
        evidence_score = 1.0 - math.exp(-evidence_indicators / 3.0)
        
        # Look for strong evidence keywords
        strong_indicators = ['explicit', 'direct', 'found', 'detected', 'pattern']
        weak_indicators = ['possible', 'potential', 'might', 'could', 'inferred']
        
        strong_count = sum(1 for indicator in strong_indicators if indicator in evidence.lower())
        weak_count = sum(1 for indicator in weak_indicators if indicator in evidence.lower())
        
        # Adjust based on evidence quality
        quality_adjustment = (strong_count * 0.1) - (weak_count * 0.05)
        
        return min(1.0, evidence_score + quality_adjustment)
    
    def _cross_validate_relationship(self, relationship: Dict, all_relationships: List[Dict]) -> float:
        """Cross-validate a relationship against others"""
        
        rel_from = relationship.get('from', '')
        rel_to = relationship.get('to', '')
        rel_type = relationship.get('type', '')
        
        # Find supporting relationships
        supporting_relationships = 0
        conflicting_relationships = 0
        
        for other_rel in all_relationships:
            if other_rel == relationship:
                continue
                
            other_from = other_rel.get('from', '')
            other_to = other_rel.get('to', '')
            other_type = other_rel.get('type', '')
            
            # Check for support (similar patterns)
            if ((rel_from == other_from or rel_to == other_to) and 
                rel_type == other_type):
                supporting_relationships += 1
            
            # Check for conflicts (contradictory relationships)
            if (rel_from == other_from and rel_to == other_to and 
                rel_type != other_type):
                conflicting_relationships += 1
        
        # Calculate cross-validation score
        support_score = min(1.0, supporting_relationships / 5.0)  # Normalize to 5 supporting relationships
        conflict_penalty = min(0.5, conflicting_relationships / 3.0)  # Max 50% penalty
        
        return max(0.0, support_score - conflict_penalty)
    
    def _calculate_pattern_support(self, relationship: Dict, patterns: List[Dict]) -> float:
        """Calculate how well patterns support a relationship"""
        
        rel_type = relationship.get('type', '')
        rel_from = relationship.get('from', '')
        rel_to = relationship.get('to', '')
        
        supporting_patterns = 0
        
        for pattern in patterns:
            pattern_type = pattern.get('type', '')
            
            # Check if pattern supports relationship type
            if self._pattern_supports_relationship(pattern_type, rel_type):
                supporting_patterns += 1
            
            # Check if pattern involves same entities
            if (rel_from in str(pattern) or rel_to in str(pattern)):
                supporting_patterns += 0.5
        
        return min(1.0, supporting_patterns / 3.0)  # Normalize to 3 supporting patterns
    
    def _calculate_context_alignment(self, relationship: Dict, context_scores: Dict) -> float:
        """Calculate how well a relationship aligns with context"""
        
        # Use overall context score as baseline
        context_quality = context_scores.get('overall_context', 0.5)
        
        # Adjust based on relationship type importance
        rel_type = relationship.get('type', '')
        type_importance = {
            'INHERITS_FROM': 1.0,
            'CALLS': 0.9,
            'USES': 0.8,
            'IMPORTS': 0.9,
            'CONTAINS': 0.85
        }
        
        importance_multiplier = type_importance.get(rel_type, 0.7)
        
        return context_quality * importance_multiplier
    
    def _calculate_relationship_support_for_pattern(self, pattern: Dict, relationships: List[Dict]) -> float:
        """Calculate how well relationships support a pattern"""
        
        pattern_type = pattern.get('type', '')
        pattern_scope = pattern.get('scope', 'unknown')
        
        supporting_relationships = 0
        
        for rel in relationships:
            rel_type = rel.get('type', '')
            
            # Check if relationship supports pattern
            if self._relationship_supports_pattern(rel_type, pattern_type):
                supporting_relationships += 1
        
        return min(1.0, supporting_relationships / 5.0)  # Normalize to 5 supporting relationships
    
    def _calculate_pattern_context_support(self, pattern: Dict, context_scores: Dict) -> float:
        """Calculate context support for a pattern"""
        
        pattern_type = pattern.get('type', '')
        
        # Different patterns align with different context aspects
        if 'DESIGN_PATTERN' in pattern_type:
            return context_scores.get('architectural_maturity', 0.5)
        elif 'FLOW' in pattern_type:
            return context_scores.get('pattern_density', 0.5)
        elif 'CONCERN' in pattern_type:
            return context_scores.get('code_quality', 0.5)
        else:
            return context_scores.get('overall_context', 0.5)
    
    def _calculate_weighted_average(self, confidences: List[float]) -> float:
        """Calculate weighted average where higher values get more weight"""
        if not confidences:
            return 0.0
        
        # Use confidence as weight (higher confidence = more weight)
        weights = confidences
        weighted_sum = sum(conf * weight for conf, weight in zip(confidences, weights))
        weight_sum = sum(weights)
        
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    def _calculate_evidence_accumulation(self, evidence_items: List[Dict]) -> float:
        """More evidence = higher confidence with diminishing returns"""
        evidence_count = len(evidence_items)
        
        # Asymptotic approach to 1.0
        return 1.0 - math.exp(-evidence_count / 4.0)
    
    def _calculate_consensus_score(self, confidences: List[float]) -> float:
        """Higher consensus = lower standard deviation"""
        if len(confidences) <= 1:
            return 1.0
        
        std_dev = self._calculate_std_dev(confidences)
        # Convert std dev to consensus (lower std dev = higher consensus)
        return max(0.0, 1.0 - (std_dev * 2.0))
    
    def _bayesian_evidence_update(self, confidences: List[float]) -> float:
        """Bayesian-like update starting from neutral prior"""
        
        if not confidences:
            return 0.5  # Neutral prior
        
        # Start with neutral prior
        posterior = 0.5
        
        # Update with each piece of evidence
        for confidence in confidences:
            # Simple Bayesian update (simplified for speed)
            likelihood = confidence
            posterior = (likelihood * posterior) / ((likelihood * posterior) + ((1 - likelihood) * (1 - posterior)))
        
        return posterior
    
    def _calculate_std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if len(values) <= 1:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    def _sigmoid_normalize(self, value: float, center: float = 0.5, steepness: float = 6.0) -> float:
        """Apply sigmoid normalization to keep values in [0,1] range"""
        return 1.0 / (1.0 + math.exp(-steepness * (value - center)))
    
    def _pattern_supports_relationship(self, pattern_type: str, rel_type: str) -> bool:
        """Check if a pattern type supports a relationship type"""
        support_map = {
            'SINGLETON_PATTERN': ['USES', 'CALLS'],
            'FACTORY_PATTERN': ['CALLS', 'CREATES'],
            'OBSERVER_PATTERN': ['CALLS', 'USES'],
            'SERVICE_LAYER_PATTERN': ['CALLS', 'USES'],
            'REPOSITORY_PATTERN': ['CALLS', 'USES'],
            'CONSTRUCTOR_INJECTION': ['USES', 'CONTAINS'],
            'DATA_TRANSFORMATION': ['CALLS', 'USES'],
            'VARIABLE_FLOW': ['USES']
        }
        
        supported_rels = support_map.get(pattern_type, [])
        return rel_type in supported_rels
    
    def _relationship_supports_pattern(self, rel_type: str, pattern_type: str) -> bool:
        """Check if a relationship type supports a pattern type"""
        return self._pattern_supports_relationship(pattern_type, rel_type)

class StatisticalConfidencePlugin(BaseConfidencePlugin):
    """Statistical confidence scoring plugin - alternative approach"""
    
    def get_scoring_methods(self) -> List[str]:
        return ["FREQUENCY_ANALYSIS", "CORRELATION_SCORING", "OUTLIER_DETECTION"]
    
    def calculate_relationship_confidence(self, relationship: Dict, all_relationships: List[Dict], 
                                        patterns: List[Dict], context_scores: Dict) -> float:
        """Statistical approach to relationship confidence"""
        
        # Frequency-based scoring
        rel_type = relationship.get('type', '')
        type_frequency = sum(1 for r in all_relationships if r.get('type') == rel_type)
        frequency_score = min(1.0, type_frequency / 10.0)  # Normalize to 10 occurrences
        
        # Use base confidence with frequency adjustment
        base_confidence = float(relationship.get('confidence', 0.5))
        
        return (base_confidence * 0.7) + (frequency_score * 0.3)
    
    def calculate_pattern_confidence(self, pattern: Dict, all_patterns: List[Dict], 
                                   relationships: List[Dict], context_scores: Dict) -> float:
        """Statistical approach to pattern confidence"""
        
        return float(pattern.get('confidence', 0.5))  # Simplified for now
    
    def aggregate_evidence_scores(self, evidence_items: List[Dict]) -> Dict[str, float]:
        """Statistical evidence aggregation"""
        
        if not evidence_items:
            return {'aggregated_confidence': 0.0}
        
        confidences = [float(item.get('confidence', 0.5)) for item in evidence_items]
        return {'aggregated_confidence': sum(confidences) / len(confidences)}
    
    def calculate_overall_confidence(self, relationships: List[Dict], patterns: List[Dict], 
                                   context_scores: Dict) -> Dict[str, float]:
        """Statistical overall confidence calculation"""
        
        all_confidences = []
        all_confidences.extend([float(r.get('confidence', 0.5)) for r in relationships])
        all_confidences.extend([float(p.get('confidence', 0.5)) for p in patterns])
        
        if not all_confidences:
            return {'overall_confidence': 0.0}
        
        return {'overall_confidence': sum(all_confidences) / len(all_confidences)}

# ================================
# CONFIDENCE PLUGIN REGISTRY
# ================================

class ConfidencePluginRegistry:
    """Registry for confidence scoring plugins - co-located"""
    
    def __init__(self):
        self.plugins = {}
        self._register_built_in_plugins()
    
    def _register_built_in_plugins(self):
        """Register all built-in confidence plugins"""
        self.plugins['mathematical'] = MathematicalConfidencePlugin()
        self.plugins['statistical'] = StatisticalConfidencePlugin()
    
    def get_plugin(self, scoring_method: str = 'mathematical') -> BaseConfidencePlugin:
        """Get confidence plugin for specific scoring method"""
        return self.plugins.get(scoring_method, self.plugins['mathematical'])

# ================================
# CONFIDENCE AGGREGATOR AGENT
# ================================

class ConfidenceAggregatorAgent(BaseXAgent):
    """Aggregates evidence and calculates mathematical confidence scores"""
    
    def __init__(self):
        super().__init__("ConfidenceAggregatorAgent")
        self.plugin_registry = ConfidencePluginRegistry()
        
        # Confidence thresholds for filtering
        self.thresholds = {
            'MINIMUM_CONFIDENCE': 0.4,
            'MEDIUM_CONFIDENCE': 0.6,
            'HIGH_CONFIDENCE': 0.8
        }
    
    def _process_intelligence(self, parsed_input: etree.Element) -> dict:
        """Aggregate evidence and calculate confidence scores using mathematical plugins"""
        
        # Extract metadata
        file_path = self._get_text_content(parsed_input, 'FilePath', 'unknown')
        content_length = int(self._get_text_content(parsed_input, 'ContentLength', '0'))
        language = self._get_text_content(parsed_input, 'Language', 'python')
        input_relationships = int(self._get_text_content(parsed_input, 'InputRelationships', '0'))
        total_patterns = int(self._get_text_content(parsed_input, 'TotalPatterns', '0'))
        
        # Extract context scores
        context_scores = self._extract_context_scores_from_xml(parsed_input)
        
        # Extract semantic analysis data
        semantic_analysis = self._extract_semantic_analysis_from_xml(parsed_input)
        
        # Extract relationships from pipeline (they may be embedded in earlier agents)
        relationships = self._extract_all_relationships_from_pipeline(parsed_input)
        
        # Get confidence scoring plugin
        confidence_plugin = self.plugin_registry.get_plugin('mathematical')
        
        # Calculate confidence scores for all relationships
        scored_relationships = []
        for relationship in relationships:
            confidence_score = confidence_plugin.calculate_relationship_confidence(
                relationship, relationships, semantic_analysis['all_patterns'], context_scores
            )
            
            # Update relationship with new confidence score
            updated_relationship = relationship.copy()
            updated_relationship['aggregated_confidence'] = confidence_score
            updated_relationship['original_confidence'] = relationship.get('confidence', 0.5)
            
            scored_relationships.append(updated_relationship)
        
        # Calculate confidence scores for all patterns
        scored_patterns = []
        for pattern in semantic_analysis['all_patterns']:
            confidence_score = confidence_plugin.calculate_pattern_confidence(
                pattern, semantic_analysis['all_patterns'], relationships, context_scores
            )
            
            # Update pattern with new confidence score
            updated_pattern = pattern.copy()
            updated_pattern['aggregated_confidence'] = confidence_score
            updated_pattern['original_confidence'] = pattern.get('confidence', 0.5)
            
            scored_patterns.append(updated_pattern)
        
        # Filter by confidence thresholds
        high_confidence_relationships = [r for r in scored_relationships 
                                       if r.get('aggregated_confidence', 0) >= self.thresholds['HIGH_CONFIDENCE']]
        medium_confidence_relationships = [r for r in scored_relationships 
                                         if self.thresholds['MEDIUM_CONFIDENCE'] <= r.get('aggregated_confidence', 0) < self.thresholds['HIGH_CONFIDENCE']]
        
        high_confidence_patterns = [p for p in scored_patterns 
                                  if p.get('aggregated_confidence', 0) >= self.thresholds['HIGH_CONFIDENCE']]
        medium_confidence_patterns = [p for p in scored_patterns 
                                    if self.thresholds['MEDIUM_CONFIDENCE'] <= p.get('aggregated_confidence', 0) < self.thresholds['HIGH_CONFIDENCE']]
        
        # Calculate overall confidence metrics
        overall_metrics = confidence_plugin.calculate_overall_confidence(
            scored_relationships, scored_patterns, context_scores
        )
        
        # Generate summary statistics
        summary_stats = self._generate_summary_statistics(
            scored_relationships, scored_patterns, context_scores, overall_metrics
        )
        
        return {
            'file_path': file_path,
            'content_length': content_length,
            'language': language,
            'plugin_used': 'mathematical_confidence_plugin',
            'input_relationships': input_relationships,
            'input_patterns': total_patterns,
            'scored_relationships': scored_relationships,
            'scored_patterns': scored_patterns,
            'high_confidence_relationships': high_confidence_relationships,
            'medium_confidence_relationships': medium_confidence_relationships,
            'high_confidence_patterns': high_confidence_patterns,
            'medium_confidence_patterns': medium_confidence_patterns,
            'context_scores': context_scores,
            'overall_metrics': overall_metrics,
            'summary_stats': summary_stats,
            'ready_for_approval': len(high_confidence_relationships) + len(high_confidence_patterns) > 0
        }
    
    def _get_text_content(self, element: etree.Element, tag_name: str, default: str = '') -> str:
        """Safely extract text content from XML element"""
        found = element.find(f'.//{tag_name}')
        return found.text if found is not None and found.text else default
    
    def _extract_context_scores_from_xml(self, parsed_input: etree.Element) -> Dict[str, float]:
        """Extract context scores from semantic analysis XML"""
        context_scores = {}
        
        score_elements = parsed_input.findall('.//Score')
        for score_elem in score_elements:
            score_name = score_elem.get('name', '')
            score_value = float(score_elem.get('value', 0.0))
            context_scores[score_name] = score_value
        
        return context_scores
    
    def _extract_semantic_analysis_from_xml(self, parsed_input: etree.Element) -> Dict:
        """Extract semantic analysis data from XML"""
        
        all_patterns = []
        
        # Extract all pattern types
        pattern_sections = [
            'Design_Patterns', 'Architectural_Patterns', 'Data_Flows', 
            'Dependency_Injection', 'Cross_Cutting_Concerns'
        ]
        
        for section in pattern_sections:
            section_elem = parsed_input.find(f'.//{section}')
            if section_elem is not None:
                pattern_elements = section_elem.findall('.//Pattern')
                for pattern_elem in pattern_elements:
                    pattern = {
                        'type': pattern_elem.get('type', ''),
                        'confidence': float(pattern_elem.get('confidence', 0.5)),
                        'evidence': [pattern_elem.text] if pattern_elem.text else [],
                        'section': section
                    }
                    
                    # Add optional attributes
                    for attr in ['class', 'method', 'function', 'variable', 'scope', 'line']:
                        if pattern_elem.get(attr):
                            pattern[attr] = pattern_elem.get(attr)
                    
                    all_patterns.append(pattern)
        
        return {'all_patterns': all_patterns}
    
    def _extract_all_relationships_from_pipeline(self, parsed_input: etree.Element) -> List[Dict]:
        """Extract relationships from the entire pipeline (may be in multiple places)"""
        relationships = []
        
        # Look for relationships in current XML
        rel_elements = parsed_input.findall('.//Relationship')
        for rel_elem in rel_elements:
            relationship = {
                'from': rel_elem.get('from', ''),
                'to': rel_elem.get('to', ''),
                'type': rel_elem.get('type', ''),
                'confidence': float(rel_elem.get('confidence', 0.5)),
                'evidence': rel_elem.text or ''
            }
            
            # Add optional attributes
            for attr in ['line', 'source_module']:
                if rel_elem.get(attr):
                    relationship[attr] = rel_elem.get(attr)
            
            relationships.append(relationship)
        
        # TODO: In full implementation, we might need to look back at previous agent outputs
        # For now, we work with what's in the current XML
        
        return relationships
    
    def _generate_summary_statistics(self, relationships: List[Dict], patterns: List[Dict], 
                                   context_scores: Dict, overall_metrics: Dict) -> Dict:
        """Generate comprehensive summary statistics"""
        
        stats = {
            'total_relationships': len(relationships),
            'total_patterns': len(patterns),
            'confidence_distribution': {
                'high': 0,
                'medium': 0,
                'low': 0
            },
            'relationship_types': Counter(),
            'pattern_types': Counter(),
            'average_confidences': {},
            'quality_indicators': {}
        }
        
        # Confidence distribution for relationships
        for rel in relationships:
            confidence = rel.get('aggregated_confidence', rel.get('confidence', 0.5))
            if confidence >= self.thresholds['HIGH_CONFIDENCE']:
                stats['confidence_distribution']['high'] += 1
            elif confidence >= self.thresholds['MEDIUM_CONFIDENCE']:
                stats['confidence_distribution']['medium'] += 1
            else:
                stats['confidence_distribution']['low'] += 1
            
            stats['relationship_types'][rel.get('type', 'unknown')] += 1
        
        # Confidence distribution for patterns
        for pattern in patterns:
            confidence = pattern.get('aggregated_confidence', pattern.get('confidence', 0.5))
            if confidence >= self.thresholds['HIGH_CONFIDENCE']:
                stats['confidence_distribution']['high'] += 1
            elif confidence >= self.thresholds['MEDIUM_CONFIDENCE']:
                stats['confidence_distribution']['medium'] += 1
            else:
                stats['confidence_distribution']['low'] += 1
            
            stats['pattern_types'][pattern.get('type', 'unknown')] += 1
        
        # Average confidences
        if relationships:
            rel_confidences = [r.get('aggregated_confidence', r.get('confidence', 0.5)) for r in relationships]
            stats['average_confidences']['relationships'] = sum(rel_confidences) / len(rel_confidences)
        
        if patterns:
            pattern_confidences = [p.get('aggregated_confidence', p.get('confidence', 0.5)) for p in patterns]
            stats['average_confidences']['patterns'] = sum(pattern_confidences) / len(pattern_confidences)
        
        # Quality indicators
        total_items = len(relationships) + len(patterns)
        if total_items > 0:
            high_quality_ratio = stats['confidence_distribution']['high'] / total_items
            stats['quality_indicators']['high_confidence_ratio'] = high_quality_ratio
            stats['quality_indicators']['analysis_completeness'] = min(1.0, total_items / 50.0)  # Normalize to 50 items
        
        return stats
    
    def _generate_xml(self, result: dict) -> str:
        """Generate XML output with confidence-scored analysis results"""
        
        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<ConfidenceAggregationResult>',
            f'  <FilePath>{result["file_path"]}</FilePath>',
            f'  <ContentLength>{result["content_length"]}</ContentLength>',
            f'  <Language>{result["language"]}</Language>',
            f'  <PluginUsed>{result["plugin_used"]}</PluginUsed>',
            f'  <InputRelationships>{result["input_relationships"]}</InputRelationships>',
            f'  <InputPatterns>{result["input_patterns"]}</InputPatterns>',
            f'  <TotalScoredItems>{len(result["scored_relationships"]) + len(result["scored_patterns"])}</TotalScoredItems>',
            f'  <ReadyForApproval>{str(result["ready_for_approval"]).lower()}</ReadyForApproval>'
        ]
        
        # Add overall confidence metrics
        xml_parts.append('  <OverallMetrics>')
        for metric_name, metric_value in result['overall_metrics'].items():
            xml_parts.append(f'    <Metric name="{metric_name}" value="{metric_value:.3f}"/>')
        xml_parts.append('  </OverallMetrics>')
        
        # Add summary statistics
        xml_parts.append('  <SummaryStatistics>')
        stats = result['summary_stats']
        xml_parts.append(f'    <TotalRelationships>{stats["total_relationships"]}</TotalRelationships>')
        xml_parts.append(f'    <TotalPatterns>{stats["total_patterns"]}</TotalPatterns>')
        
        # Confidence distribution
        xml_parts.append('    <ConfidenceDistribution>')
        for level, count in stats['confidence_distribution'].items():
            xml_parts.append(f'      <Level name="{level}" count="{count}"/>')
        xml_parts.append('    </ConfidenceDistribution>')
        
        xml_parts.append('  </SummaryStatistics>')
        
        # Add high confidence relationships
        xml_parts.append('  <HighConfidenceRelationships>')
        for rel in result['high_confidence_relationships']:
            rel_xml = (
                f'    <Relationship '
                f'from="{rel["from"]}" '
                f'to="{rel["to"]}" '
                f'type="{rel["type"]}" '
                f'original_confidence="{rel.get("original_confidence", 0.5):.3f}" '
                f'aggregated_confidence="{rel.get("aggregated_confidence", 0.5):.3f}"'
            )
            
            if 'line' in rel:
                rel_xml += f' line="{rel["line"]}"'
            
            rel_xml += f'>{rel.get("evidence", "")}</Relationship>'
            xml_parts.append(rel_xml)
        
        xml_parts.append('  </HighConfidenceRelationships>')
        
        # Add high confidence patterns
        xml_parts.append('  <HighConfidencePatterns>')
        for pattern in result['high_confidence_patterns']:
            pattern_xml = (
                f'    <Pattern '
                f'type="{pattern.get("type", "")}" '
                f'original_confidence="{pattern.get("original_confidence", 0.5):.3f}" '
                f'aggregated_confidence="{pattern.get("aggregated_confidence", 0.5):.3f}"'
            )
            
            # Add optional attributes
            for attr in ['class', 'method', 'function', 'scope', 'line']:
                if attr in pattern:
                    pattern_xml += f' {attr}="{pattern[attr]}"'
            
            evidence_text = "; ".join(pattern.get('evidence', []))
            pattern_xml += f'>{evidence_text}</Pattern>'
            xml_parts.append(pattern_xml)
        
        xml_parts.append('  </HighConfidencePatterns>')
        
        xml_parts.extend([
            f'  <ProcessingTime>{self.metrics["total_time"]:.2f}ms</ProcessingTime>',
            '</ConfidenceAggregationResult>'
        ])
        
        return '\n'.join(xml_parts)

# Test the confidence aggregator agent
if __name__ == "__main__":
    print("🧪 Testing Confidence Aggregator Agent")
    
    # Create sample XML input (from ContextAnalyzer output)
    sample_input = """<?xml version="1.0" encoding="UTF-8"?>
<SemanticAnalysisResult>
  <FilePath>sample_code.py</FilePath>
  <ContentLength>5836</ContentLength>
  <Language>python</Language>
  <PluginUsed>python_semantic_plugin</PluginUsed>
  <InputRelationships>3</InputRelationships>
  <TotalPatterns>4</TotalPatterns>
  <PatternTypes>SERVICE_LAYER_PATTERN, CONSTRUCTOR_INJECTION, ERROR_HANDLING_CONCERN, DATA_TRANSFORMATION</PatternTypes>
  <ContextScores>
    <Score name="pattern_density" value="1.000"/>
    <Score name="architectural_maturity" value="0.300"/>
    <Score name="code_quality" value="0.333"/>
    <Score name="overall_context" value="0.520"/>
  </ContextScores>
  <SemanticAnalysis>
    <Architectural_Patterns>
      <Pattern type="SERVICE_LAYER_PATTERN" confidence="0.75" class="UserService" line="23">Service layer with business logic: 1 methods</Pattern>
    </Architectural_Patterns>
    <Data_Flows>
      <Pattern type="DATA_TRANSFORMATION" confidence="0.7" function="create_user" line="27">Function with 2 returns and 0 transformations</Pattern>
      <Pattern type="DATA_TRANSFORMATION" confidence="0.7" function="process_user_data" line="35">Function with 1 returns and 0 transformations</Pattern>
    </Data_Flows>
    <Dependency_Injection>
      <Pattern type="CONSTRUCTOR_INJECTION" confidence="0.8" class="PostgreSQLConnection" line="15">Constructor injection with 2 dependencies</Pattern>
    </Dependency_Injection>
  </SemanticAnalysis>
  <Relationships>
    <Relationship from="code" to="__init__" type="CALLS" confidence="0.85">Function call found</Relationship>
    <Relationship from="UserService" to="DatabaseConnection" type="USES" confidence="0.9">Dependency injection</Relationship>
    <Relationship from="PostgreSQLConnection" to="DatabaseConnection" type="INHERITS_FROM" confidence="0.95">Class inheritance</Relationship>
  </Relationships>
</SemanticAnalysisResult>"""
    
    # Test the agent
    agent = ConfidenceAggregatorAgent()
    result = agent.process(sample_input)
    
    print(f"✅ Processing completed in {agent.metrics['total_time']:.2f}ms")
    print(f"📄 Result length: {len(result)} characters")
    print("\n📊 Confidence aggregation result:")
    print(result)

#!/usr/bin/env python3
"""
Enhanced Logging Configuration for X-Agent Pipeline
Enables both console and file logging for debugging and monitoring
"""

import logging
import os
from datetime import datetime

def setup_logging(log_level=logging.INFO, enable_file_logging=True, log_dir="logs"):
    """
    Setup comprehensive logging for X-Agent Pipeline
    
    Args:
        log_level: Logging level (INFO, DEBUG, etc.)
        enable_file_logging: Whether to save logs to files
        log_dir: Directory to save log files
    """
    
    # Create logs directory if it doesn't exist
    if enable_file_logging and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler (for immediate feedback)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)
    
    if enable_file_logging:
        # Generate timestamp for log files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Main log file (all messages)
        main_log_file = os.path.join(log_dir, f"x_agent_pipeline_{timestamp}.log")
        file_handler = logging.FileHandler(main_log_file, mode='w')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
        # Plugin Creator specific log
        plugin_log_file = os.path.join(log_dir, f"plugin_creator_{timestamp}.log")
        plugin_handler = logging.FileHandler(plugin_log_file, mode='w')
        plugin_handler.setLevel(log_level)
        plugin_handler.setFormatter(detailed_formatter)
        
        # Add filter for plugin creator messages
        plugin_handler.addFilter(lambda record: 'Plugin Creator' in record.getMessage())
        root_logger.addHandler(plugin_handler)
        
        # Error log file (errors only)
        error_log_file = os.path.join(log_dir, f"errors_{timestamp}.log")
        error_handler = logging.FileHandler(error_log_file, mode='w')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
        
        print(f"📝 Logging enabled!")
        print(f"   Main Log: {main_log_file}")
        print(f"   Plugin Log: {plugin_log_file}")
        print(f"   Error Log: {error_log_file}")
    
    return root_logger

# Convenience function for testing
def enable_debug_logging():
    """Enable debug-level logging for detailed troubleshooting"""
    return setup_logging(log_level=logging.DEBUG, enable_file_logging=True)

# Quick setup for production
def enable_production_logging():
    """Enable production-level logging"""
    return setup_logging(log_level=logging.INFO, enable_file_logging=True)

if __name__ == "__main__":
    # Test the logging setup
    logger = setup_logging()
    logger.info("🧪 Logging system test")
    logger.debug("Debug message (only visible if debug enabled)")
    logger.warning("Warning message")
    logger.error("Error message test")
    print("✅ Logging configuration test complete!")

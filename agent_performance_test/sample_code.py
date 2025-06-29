#!/usr/bin/env python3
"""
Sample Code File for Agent Performance Testing
This file contains various code structures to test POI detection and relationship analysis.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Test different import styles
import requests
from datetime import datetime
from collections import defaultdict

@dataclass
class UserProfile:
    """User profile data structure"""
    user_id: str
    name: str
    email: str
    created_at: datetime
    is_active: bool = True

class DatabaseConnection(ABC):
    """Abstract base class for database connections"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.is_connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish database connection"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection"""
        pass
    
    def get_status(self) -> Dict[str, bool]:
        """Get connection status"""
        return {"connected": self.is_connected}

class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL database connection implementation"""
    
    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        super().__init__(connection_string)
        self.host = host
        self.port = port
        self.database = database
    
    def connect(self) -> bool:
        """Connect to PostgreSQL database"""
        try:
            # Simulate database connection
            print(f"Connecting to PostgreSQL at {self.host}:{self.port}")
            self.is_connected = True
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from PostgreSQL"""
        self.is_connected = False
        print("Disconnected from PostgreSQL")
    
    def execute_query(self, query: str) -> Optional[List[Dict]]:
        """Execute SQL query"""
        if not self.is_connected:
            raise ConnectionError("Database not connected")
        
        # Simulate query execution
        print(f"Executing query: {query}")
        return [{"result": "sample_data"}]

class UserService:
    """Service for managing user operations"""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
        self.cache = defaultdict(dict)
        self._user_count = 0
    
    async def create_user(self, user_data: Dict[str, str]) -> UserProfile:
        """Create a new user"""
        user_id = f"user_{self._user_count + 1}"
        
        profile = UserProfile(
            user_id=user_id,
            name=user_data.get("name", ""),
            email=user_data.get("email", ""),
            created_at=datetime.now()
        )
        
        # Cache the user
        self.cache[user_id] = profile
        self._user_count += 1
        
        return profile
    
    def get_user(self, user_id: str) -> Optional[UserProfile]:
        """Retrieve user by ID"""
        return self.cache.get(user_id)
    
    def list_active_users(self) -> List[UserProfile]:
        """Get all active users"""
        return [user for user in self.cache.values() if user.is_active]
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user account"""
        user = self.get_user(user_id)
        if user:
            user.is_active = False
            return True
        return False

def load_configuration(config_path: str) -> Dict[str, any]:
    """Load application configuration from file"""
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in configuration file: {e}")
        return {}

async def initialize_application():
    """Initialize the application with database and services"""
    # Load configuration
    config = load_configuration("config.json")
    
    # Setup database connection
    db_config = config.get("database", {})
    db_connection = PostgreSQLConnection(
        host=db_config.get("host", "localhost"),
        port=db_config.get("port", 5432),
        database=db_config.get("name", "myapp"),
        username=db_config.get("username", "user"),
        password=db_config.get("password", "password")
    )
    
    # Connect to database
    if not db_connection.connect():
        raise RuntimeError("Failed to connect to database")
    
    # Initialize services
    user_service = UserService(db_connection)
    
    # Create sample user
    sample_user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    
    user = await user_service.create_user(sample_user_data)
    print(f"Created user: {user.name} ({user.user_id})")
    
    return {
        "database": db_connection,
        "user_service": user_service,
        "config": config
    }

if __name__ == "__main__":
    print("Starting application...")
    try:
        app_context = asyncio.run(initialize_application())
        print("Application initialized successfully")
        
        # Test user operations
        user_service = app_context["user_service"]
        active_users = user_service.list_active_users()
        print(f"Active users: {len(active_users)}")
        
    except Exception as e:
        print(f"Application startup failed: {e}")
    finally:
        print("Application shutdown")

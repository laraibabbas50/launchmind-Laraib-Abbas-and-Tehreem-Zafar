"""
Message Bus - Handles communication between agents
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List

class MessageBus:
    """Simple message bus for agents to communicate"""
    
    def __init__(self):
        self.all_messages = []      # Stores every message ever sent
        self.queues = {}            # Stores messages waiting for each agent
    
    def send_message(self, from_agent: str, to_agent: str, 
                     message_type: str, payload: dict, 
                     parent_message_id: str = None) -> str:
        """Send a message from one agent to another"""
        
        message = {
            "message_id": str(uuid.uuid4()),
            "from_agent": from_agent,
            "to_agent": to_agent,
            "message_type": message_type,  # 'task', 'result', 'revision_request', 'confirmation'
            "payload": payload,
            "timestamp": datetime.now().isoformat() + "Z",
            "parent_message_id": parent_message_id
        }
        
        # Store in history
        self.all_messages.append(message)
        
        # Add to recipient's queue
        if to_agent not in self.queues:
            self.queues[to_agent] = []
        self.queues[to_agent].append(message)
        
        print(f"\n📨 MESSAGE: {from_agent} → {to_agent} ({message_type})")
        
        return message["message_id"]
    
    def get_messages_for_agent(self, agent_name: str) -> List[Dict]:
        """Get all pending messages for an agent"""
        return self.queues.get(agent_name, [])
    
    def clear_queue(self, agent_name: str):
        """Clear an agent's message queue"""
        self.queues[agent_name] = []
    
    def print_all_messages(self):
        """Show all messages (for demo)"""
        print("\n" + "="*50)
        print("MESSAGE HISTORY")
        print("="*50)
        for msg in self.all_messages:
            print(f"\n{msg['timestamp']} | {msg['from_agent']} → {msg['to_agent']}")
            print(f"  Type: {msg['message_type']}")
            print(f"  Payload: {str(msg['payload'])[:100]}...")


# Create a single message bus that all agents will use
message_bus = MessageBus()
"""
Product Agent - Generates product specifications
"""

from message_bus import message_bus

class ProductAgent:
    def __init__(self):
        self.name = "product"
    
    def generate_mock_spec(self, idea: str) -> dict:
        """Generate a mock product specification"""
        
        return {
            "value_proposition": "An app that helps students find tutors easily",
            "personas": [
                {"name": "Sarah", "role": "Student", "pain_point": "Can't find affordable tutors"},
                {"name": "Mike", "role": "Tutor", "pain_point": "Needs more students"}
            ],
            "features": [
                {"name": "Search", "description": "Find tutors by subject", "priority": 1},
                {"name": "Booking", "description": "Schedule sessions", "priority": 2}
            ],
            "user_stories": [
                "As a student, I want to find a tutor so I can improve my grades",
                "As a tutor, I want to list my availability so I can get bookings"
            ]
        }
    
    def process_messages(self):
        messages = message_bus.get_messages_for_agent(self.name)
        
        for msg in messages:
            if msg["message_type"] == "task":
                print(f"\n📥 PRODUCT AGENT: Received task")
                spec = self.generate_mock_spec(msg["payload"].get("idea", ""))
                
                message_bus.send_message(
                    from_agent=self.name,
                    to_agent="engineer",
                    message_type="result",
                    payload=spec
                )
                
                message_bus.send_message(
                    from_agent=self.name,
                    to_agent="marketing",
                    message_type="result",
                    payload=spec
                )
                message_bus.send_message(
                    from_agent=self.name,
                    to_agent="ceo",
                    message_type="confirmation",
                    payload=spec
                )
                
                print(f"✅ PRODUCT AGENT: Spec generated and sent")
            
            # ADD THIS NEW PART (START)
            elif msg["message_type"] == "revision_request":
                print(f"\n🔄 PRODUCT AGENT: Received revision request")
                feedback = msg["payload"].get("feedback", "")
                print(f"   Feedback: {feedback}")
                
                # Generate improved spec based on feedback
                improved_spec = self.generate_mock_spec(msg["payload"].get("original_spec", {}))
                # Add more features based on feedback
                improved_spec["features"].append({"name": "New Feature", "description": feedback, "priority": 3})
                
                message_bus.send_message(
                    from_agent=self.name,
                    to_agent="engineer",
                    message_type="result",
                    payload=improved_spec
                )

                message_bus.send_message(
                    from_agent=self.name,
                    to_agent="marketing",
                    message_type="result",
                    payload=improved_spec
                )
                message_bus.send_message(
                    from_agent=self.name,
                    to_agent="ceo",
                    message_type="confirmation",
                    payload=improved_spec
                )
                
                print(f"✅ PRODUCT AGENT: Improved spec sent")
            # ADD THIS NEW PART (END)
        
        message_bus.clear_queue(self.name)
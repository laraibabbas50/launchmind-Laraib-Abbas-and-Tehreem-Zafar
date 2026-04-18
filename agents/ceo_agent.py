from message_bus import message_bus

class CEOAgent:
    def __init__(self):
        self.name = "ceo"
        self.review_count = 0
    
    def run(self, startup_idea):
        print("\n" + "="*50)
        print(f"🚀 CEO AGENT STARTING")
        print(f"📝 Idea: {startup_idea}")
        print("="*50)
        
        task = {"idea": startup_idea, "focus": "Define user personas and top features"}
        message_bus.send_message(self.name, "product", "task", task)
        print("\n✅ CEO: Task sent to Product Agent")
    
    def review_product_spec(self, spec):
        """Review product spec and decide if it needs revision"""
        self.review_count += 1
        
        print(f"\n🔍 CEO: Reviewing Product Spec (Attempt {self.review_count})")
        
        # Mock review logic - replace with LLM later
        features = spec.get("features", [])
        if len(features) < 3:
            return False, "Need at least 3 features. Please add more."
        
        personas = spec.get("personas", [])
        if len(personas) < 2:
            return False, "Need at least 2 user personas."
        
        return True, "Spec looks good!"
    
    def process_feedback(self):
        """Check for messages that need review"""
        messages = message_bus.get_messages_for_agent(self.name)
        
        for msg in messages:
            if msg["message_type"] == "confirmation" and msg["from_agent"] == "product":
                spec = msg["payload"]
                is_accepted, feedback = self.review_product_spec(spec)
                
                if is_accepted:
                    print(f"✅ CEO: Spec approved - {feedback}")
                    # Send to engineer and marketing
                    message_bus.send_message(self.name, "engineer", "task", spec)
                    message_bus.send_message(self.name, "marketing", "task", spec)
                else:
                    print(f"🔄 CEO: Spec needs revision - {feedback}")
                    # Send revision request back to product
                    message_bus.send_message(
                        self.name, "product", "revision_request",
                        {"feedback": feedback, "original_spec": spec}
                    )
        
        message_bus.clear_queue(self.name)
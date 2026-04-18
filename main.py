"""
LaunchMind - Main Entry Point
Run this file to start the multi-agent system
"""

import os
from dotenv import load_dotenv
from message_bus import message_bus
from agents.ceo_agent import CEOAgent
from agents.product_agent import ProductAgent
from agents.engineer_agent import EngineerAgent
from agents.marketing_agent import MarketingAgent

# Load API keys from .env file
load_dotenv()

def main():
    """Run the complete system"""
    
    print("\n" + "="*60)
    print("🚀 LAUNCHMIND - Multi-Agent System")
    print("="*60)
    
    # Your startup idea - CHANGE THIS!
    STARTUP_IDEA = "A platform where students can sell second-hand textbooks to each other"
    
    # Create all agents
    ceo = CEOAgent()
    product = ProductAgent()
    engineer = EngineerAgent()
    marketing = MarketingAgent()
    
    print("\n✅ All agents created\n")
    
    # Run the CEO (this starts everything)
    ceo.run(STARTUP_IDEA)
    
    # Process messages in order
    product.process_messages()
    ceo.process_feedback() 
    engineer.process_messages()
    marketing.process_messages()
    
    # Show the complete message history
    message_bus.print_all_messages()
    
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
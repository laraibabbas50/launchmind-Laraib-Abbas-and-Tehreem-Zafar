# LaunchMind - Multi-Agent System

## Startup Idea
A platform where students can sell second-hand textbooks to each other. Features include price comparison, condition ratings, and in-app messaging.

## Agent Architecture

### Flow Diagram
Startup Idea
↓
CEO Agent (Orchestrator)
↓ (task)
Product Agent
↓ (result: product spec)
CEO Agent (reviews)
↓ (revision_request if needs improvement)
Product Agent (improves spec)
↓ (result: improved spec)
CEO Agent (approves)
↓ (task to Engineer + Marketing)
Engineer Agent → GitHub PR
Marketing Agent → Slack + Email


### Agents Description
- **CEO Agent**: Orchestrates all agents, decomposes ideas, reviews outputs using LLM reasoning, sends revision requests
- **Product Agent**: Generates product specifications with value proposition, personas, features, and user stories
- **Engineer Agent**: Creates GitHub branches, commits HTML landing pages, opens Pull Requests
- **Marketing Agent**: Sends cold outreach emails via SendGrid, posts launch messages to Slack

## Setup Instructions

### Prerequisites
- Python 3.8+
- GitHub account
- Slack workspace
- SendGrid account

### Installation

1. Clone the repository:
```bash
git clone https://github.com/laraibabbas50/launchmind-Laraib-Abbas-and-Tehreem-Zafar
cd launchmind-Laraib-Abbas-and-Tehreem-Zafar
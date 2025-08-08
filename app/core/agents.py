#!/usr/bin/env python3
"""
OpenRouter Multi-Agent System
Autonomous agents using free OpenRouter models
"""

import os
import json
import time
import asyncio
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from ai_tools_suite import AIToolsSuite

class AgentRole(Enum):
    """Agent role definitions"""
    COORDINATOR = "coordinator"       # Manages tasks and delegates
    RESEARCHER = "researcher"         # Gathers information and analyzes
    CODER = "coder"                  # Writes and reviews code
    WRITER = "writer"                # Creates documentation and content
    ANALYST = "analyst"              # Processes data and provides insights
    REVIEWER = "reviewer"            # Reviews and validates work
    EXECUTOR = "executor"            # Executes tasks and operations

class AgentStatus(Enum):
    """Agent status states"""
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class Task:
    """Task definition for agents"""
    id: str
    description: str
    type: str
    priority: int = 5  # 1-10, 10 = highest
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    assigned_to: Optional[str] = None
    status: str = "pending"
    result: Optional[Dict] = None
    dependencies: List[str] = field(default_factory=list)
    context: Dict = field(default_factory=dict)

@dataclass
class Message:
    """Inter-agent communication message"""
    id: str
    from_agent: str
    to_agent: str
    content: str
    message_type: str  # 'task_assignment', 'result', 'request', 'response'
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    context: Dict = field(default_factory=dict)

class Agent:
    """Base autonomous agent class"""
    
    def __init__(self, agent_id: str, role: AgentRole, ai_suite: AIToolsSuite):
        self.id = agent_id
        self.role = role
        self.ai_suite = ai_suite
        self.status = AgentStatus.IDLE
        self.current_task: Optional[Task] = None
        self.inbox: List[Message] = []
        self.outbox: List[Message] = []
        self.completed_tasks: List[Task] = []
        self.capabilities: List[str] = []
        self.memory: Dict = {}
        self.stats = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'messages_sent': 0,
            'messages_received': 0,
            'total_tokens': 0,
            'start_time': datetime.now().isoformat()
        }
        self._setup_capabilities()
    
    def _setup_capabilities(self):
        """Setup agent capabilities based on role"""
        base_capabilities = ['communicate', 'analyze', 'report']
        
        role_capabilities = {
            AgentRole.COORDINATOR: ['delegate', 'prioritize', 'orchestrate', 'monitor'],
            AgentRole.RESEARCHER: ['search', 'gather_info', 'synthesize', 'fact_check'],
            AgentRole.CODER: ['write_code', 'debug', 'refactor', 'test'],
            AgentRole.WRITER: ['create_docs', 'edit', 'format', 'explain'],
            AgentRole.ANALYST: ['process_data', 'identify_patterns', 'generate_insights'],
            AgentRole.REVIEWER: ['validate', 'quality_check', 'provide_feedback'],
            AgentRole.EXECUTOR: ['execute_tasks', 'run_operations', 'handle_errors']
        }
        
        self.capabilities = base_capabilities + role_capabilities.get(self.role, [])
    
    def can_handle_task(self, task: Task) -> bool:
        """Check if agent can handle a specific task type"""
        task_capability_map = {
            'code_analysis': ['analyze', 'write_code'],
            'code_generation': ['write_code'],
            'documentation': ['create_docs', 'write', 'explain'],
            'research': ['search', 'gather_info', 'analyze'],
            'coordination': ['delegate', 'orchestrate', 'monitor'],
            'review': ['validate', 'quality_check'],
            'data_analysis': ['process_data', 'analyze', 'identify_patterns']
        }
        
        required_capabilities = task_capability_map.get(task.type, ['analyze'])
        return any(cap in self.capabilities for cap in required_capabilities)
    
    def receive_message(self, message: Message):
        """Receive a message from another agent"""
        self.inbox.append(message)
        self.stats['messages_received'] += 1
    
    def send_message(self, to_agent: str, content: str, message_type: str, context: Dict = None):
        """Send a message to another agent"""
        message = Message(
            id=f"msg_{len(self.outbox)}_{int(time.time())}",
            from_agent=self.id,
            to_agent=to_agent,
            content=content,
            message_type=message_type,
            context=context or {}
        )
        self.outbox.append(message)
        self.stats['messages_sent'] += 1
        return message
    
    def process_inbox(self):
        """Process incoming messages"""
        for message in self.inbox.copy():
            try:
                if message.message_type == 'task_assignment':
                    # Handle task assignment
                    task_data = message.context.get('task')
                    if task_data:
                        task = Task(**task_data)
                        if self.can_handle_task(task):
                            self.accept_task(task)
                            self.send_message(
                                message.from_agent,
                                f"Task {task.id} accepted",
                                'response',
                                {'status': 'accepted'}
                            )
                        else:
                            self.send_message(
                                message.from_agent,
                                f"Cannot handle task {task.id}",
                                'response',
                                {'status': 'declined', 'reason': 'insufficient_capabilities'}
                            )
                
                elif message.message_type == 'request':
                    # Handle information requests
                    self.handle_request(message)
                
                # Remove processed message
                self.inbox.remove(message)
                
            except Exception as e:
                print(f"Agent {self.id}: Error processing message {message.id}: {e}")
    
    def accept_task(self, task: Task):
        """Accept and start working on a task"""
        self.current_task = task
        self.status = AgentStatus.WORKING
        task.assigned_to = self.id
        task.status = "in_progress"
    
    def handle_request(self, message: Message):
        """Handle information requests from other agents"""
        request_type = message.context.get('request_type')
        
        if request_type == 'status_check':
            response = {
                'agent_id': self.id,
                'status': self.status.value,
                'current_task': self.current_task.id if self.current_task else None,
                'capabilities': self.capabilities
            }
            
            self.send_message(
                message.from_agent,
                "Status update",
                'response',
                response
            )
    
    async def execute_task(self, task: Task) -> Dict:
        """Execute a task using AI capabilities"""
        try:
            print(f"Agent {self.id} ({self.role.value}): Executing task {task.id}")
            
            # Generate appropriate prompt based on role and task
            prompt = self._generate_task_prompt(task)
            
            # Use AI to complete the task
            if task.type == 'code_analysis':
                result = self.ai_suite.code_analyzer(task.context.get('code', ''), 
                                                  task.context.get('language', 'python'))
            elif task.type == 'documentation':
                result = self.ai_suite.documentation_generator(task.context.get('content', ''),
                                                            task.context.get('doc_type', 'readme'))
            elif task.type == 'research':
                result = self.ai_suite.smart_request(prompt, 'reasoning')
            else:
                result = self.ai_suite.smart_request(prompt, 'general')
            
            if result['success']:
                # Update stats
                if result.get('usage'):
                    self.stats['total_tokens'] += result['usage'].get('total_tokens', 0)
                
                task_result = {
                    'task_id': task.id,
                    'agent_id': self.id,
                    'status': 'completed',
                    'result': result['response'],
                    'model': result.get('model'),
                    'tokens_used': result.get('usage', {}).get('total_tokens', 0),
                    'completed_at': datetime.now().isoformat()
                }
                
                self.stats['tasks_completed'] += 1
                task.result = task_result
                task.status = "completed"
                self.completed_tasks.append(task)
                self.current_task = None
                self.status = AgentStatus.IDLE
                
                print(f"Agent {self.id}: Task {task.id} completed successfully")
                return task_result
                
            else:
                raise Exception(result.get('error', 'AI request failed'))
                
        except Exception as e:
            print(f"Agent {self.id}: Task {task.id} failed: {e}")
            
            self.stats['tasks_failed'] += 1
            task.status = "failed"
            self.current_task = None
            self.status = AgentStatus.ERROR
            
            return {
                'task_id': task.id,
                'agent_id': self.id,
                'status': 'failed',
                'error': str(e),
                'failed_at': datetime.now().isoformat()
            }
    
    def _generate_task_prompt(self, task: Task) -> str:
        """Generate AI prompt based on role and task"""
        role_context = {
            AgentRole.COORDINATOR: "You are a project coordinator. Focus on planning, organization, and delegation.",
            AgentRole.RESEARCHER: "You are a researcher. Focus on gathering information, analysis, and insights.",
            AgentRole.CODER: "You are a software developer. Focus on code quality, best practices, and functionality.",
            AgentRole.WRITER: "You are a technical writer. Focus on clarity, documentation, and communication.",
            AgentRole.ANALYST: "You are a data analyst. Focus on patterns, insights, and recommendations.",
            AgentRole.REVIEWER: "You are a quality reviewer. Focus on validation, feedback, and improvement.",
            AgentRole.EXECUTOR: "You are a task executor. Focus on implementation and getting things done."
        }
        
        context = role_context.get(self.role, "You are an AI assistant.")
        return f"{context}\n\nTask: {task.description}\n\nProvide a comprehensive response based on your role."
    
    def get_status(self) -> Dict:
        """Get current agent status"""
        return {
            'id': self.id,
            'role': self.role.value,
            'status': self.status.value,
            'capabilities': self.capabilities,
            'current_task': self.current_task.id if self.current_task else None,
            'completed_tasks': len(self.completed_tasks),
            'inbox_size': len(self.inbox),
            'stats': self.stats
        }

class MultiAgentSystem:
    """Multi-agent system orchestrator"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.message_queue: List[Message] = []
        self.ai_suite = AIToolsSuite()
        self.system_stats = {
            'start_time': datetime.now().isoformat(),
            'total_tasks': 0,
            'completed_tasks': 0,
            'active_agents': 0,
            'total_messages': 0
        }
        self.running = False
    
    def create_agent(self, agent_id: str, role: AgentRole) -> Agent:
        """Create a new agent"""
        if agent_id in self.agents:
            raise ValueError(f"Agent {agent_id} already exists")
        
        agent = Agent(agent_id, role, self.ai_suite)
        self.agents[agent_id] = agent
        self.system_stats['active_agents'] = len(self.agents)
        
        print(f"Created agent: {agent_id} ({role.value})")
        return agent
    
    def create_task(self, task_id: str, description: str, task_type: str, 
                   priority: int = 5, context: Dict = None) -> Task:
        """Create a new task"""
        if task_id in self.tasks:
            raise ValueError(f"Task {task_id} already exists")
        
        task = Task(
            id=task_id,
            description=description,
            type=task_type,
            priority=priority,
            context=context or {}
        )
        
        self.tasks[task_id] = task
        self.system_stats['total_tasks'] += 1
        
        print(f"Created task: {task_id} ({task_type})")
        return task
    
    def assign_task(self, task_id: str, agent_id: str = None) -> bool:
        """Assign task to agent (or find suitable agent)"""
        if task_id not in self.tasks:
            print(f"Task {task_id} not found")
            return False
        
        task = self.tasks[task_id]
        
        if agent_id:
            # Assign to specific agent
            if agent_id not in self.agents:
                print(f"Agent {agent_id} not found")
                return False
            
            agent = self.agents[agent_id]
            if not agent.can_handle_task(task):
                print(f"Agent {agent_id} cannot handle task {task_id}")
                return False
            
            agent.accept_task(task)
            print(f"Task {task_id} assigned to {agent_id}")
            return True
        
        else:
            # Find suitable agent
            suitable_agents = [
                agent for agent in self.agents.values()
                if agent.can_handle_task(task) and agent.status == AgentStatus.IDLE
            ]
            
            if not suitable_agents:
                print(f"No suitable agent found for task {task_id}")
                return False
            
            # Select best agent (could be based on workload, capabilities, etc.)
            selected_agent = suitable_agents[0]  # Simple selection
            selected_agent.accept_task(task)
            
            print(f"Task {task_id} auto-assigned to {selected_agent.id}")
            return True
    
    def route_message(self, message: Message):
        """Route message between agents"""
        if message.to_agent in self.agents:
            self.agents[message.to_agent].receive_message(message)
            self.system_stats['total_messages'] += 1
        else:
            print(f"Agent {message.to_agent} not found for message routing")
    
    async def run_system(self, duration: int = 60):
        """Run the multi-agent system"""
        print(f"Starting multi-agent system for {duration} seconds...")
        self.running = True
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration:
            try:
                # Process agent inboxes
                for agent in self.agents.values():
                    agent.process_inbox()
                    
                    # Route outgoing messages
                    for message in agent.outbox:
                        self.route_message(message)
                    agent.outbox.clear()
                
                # Execute tasks for working agents
                active_tasks = []
                for agent in self.agents.values():
                    if agent.status == AgentStatus.WORKING and agent.current_task:
                        task_future = asyncio.create_task(agent.execute_task(agent.current_task))
                        active_tasks.append(task_future)
                
                # Wait for task completion
                if active_tasks:
                    await asyncio.gather(*active_tasks, return_exceptions=True)
                
                # Update system stats
                completed = sum(1 for task in self.tasks.values() if task.status == "completed")
                self.system_stats['completed_tasks'] = completed
                
                # Short pause to prevent overwhelming
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"System error: {e}")
        
        self.running = False
        print("Multi-agent system stopped")
    
    def stop_system(self):
        """Stop the multi-agent system"""
        self.running = False
    
    def get_system_status(self) -> Dict:
        """Get overall system status"""
        agent_statuses = {agent_id: agent.get_status() for agent_id, agent in self.agents.items()}
        
        task_statuses = {}
        for task_id, task in self.tasks.items():
            task_statuses[task_id] = {
                'id': task.id,
                'type': task.type,
                'status': task.status,
                'assigned_to': task.assigned_to,
                'priority': task.priority
            }
        
        return {
            'system_stats': self.system_stats,
            'agents': agent_statuses,
            'tasks': task_statuses,
            'running': self.running
        }
    
    def create_default_team(self) -> Dict[str, Agent]:
        """Create a default team of agents"""
        team = {}
        
        # Create different types of agents
        team['coordinator'] = self.create_agent('coord_001', AgentRole.COORDINATOR)
        team['researcher'] = self.create_agent('research_001', AgentRole.RESEARCHER)
        team['coder'] = self.create_agent('coder_001', AgentRole.CODER)
        team['writer'] = self.create_agent('writer_001', AgentRole.WRITER)
        team['reviewer'] = self.create_agent('reviewer_001', AgentRole.REVIEWER)
        
        print(f"Created default team with {len(team)} agents")
        return team

def demo_multi_agent_system():
    """Demonstration of the multi-agent system"""
    print("OpenRouter Multi-Agent System Demo")
    print("=" * 50)
    
    # Create system
    system = MultiAgentSystem()
    
    # Create team
    team = system.create_default_team()
    
    # Create sample tasks
    tasks = [
        {
            'id': 'task_001',
            'description': 'Analyze the provided Python code for potential improvements',
            'type': 'code_analysis',
            'context': {
                'code': '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Generate first 10 fibonacci numbers
for i in range(10):
    print(fibonacci(i))
                ''',
                'language': 'python'
            }
        },
        {
            'id': 'task_002',
            'description': 'Research best practices for multi-agent systems',
            'type': 'research'
        },
        {
            'id': 'task_003',
            'description': 'Create documentation for the agent system',
            'type': 'documentation',
            'context': {
                'content': 'Multi-agent system with autonomous agents using OpenRouter',
                'doc_type': 'readme'
            }
        }
    ]
    
    # Create and assign tasks
    for task_data in tasks:
        task = system.create_task(**task_data)
        system.assign_task(task.id)  # Auto-assign to suitable agent
    
    # Run system demonstration
    async def run_demo():
        await system.run_system(duration=30)  # Run for 30 seconds
        
        # Print results
        print("\n" + "=" * 50)
        print("DEMO RESULTS")
        print("=" * 50)
        
        status = system.get_system_status()
        
        print(f"Total Tasks: {status['system_stats']['total_tasks']}")
        print(f"Completed Tasks: {status['system_stats']['completed_tasks']}")
        print(f"Active Agents: {status['system_stats']['active_agents']}")
        print(f"Messages Exchanged: {status['system_stats']['total_messages']}")
        
        print("\nAgent Performance:")
        for agent_id, agent_status in status['agents'].items():
            print(f"  {agent_id} ({agent_status['role']}): {agent_status['completed_tasks']} tasks completed")
        
        print("\nTask Status:")
        for task_id, task_status in status['tasks'].items():
            print(f"  {task_id}: {task_status['status']} (assigned to: {task_status.get('assigned_to', 'None')})")
        
        print(f"\nCost: $0.00 (all agents use free models)")
        print("Dashboard: https://openrouter.ai/activity")
    
    # Run the demo
    asyncio.run(run_demo())

def main():
    """Main function for interactive use"""
    print("OpenRouter Multi-Agent System")
    print("=" * 40)
    print("1. Run Demo")
    print("2. Create Custom System")
    print("3. System Documentation")
    print("0. Exit")
    
    choice = input("\nSelect option (0-3): ").strip()
    
    if choice == '1':
        demo_multi_agent_system()
    elif choice == '2':
        print("Custom system creation coming soon...")
    elif choice == '3':
        print("Multi-Agent System Documentation")
        print("-" * 40)
        print("Features:")
        print("- Autonomous agents with different roles")
        print("- Inter-agent communication")
        print("- Task assignment and coordination")
        print("- Uses OpenRouter free models ($0.00 cost)")
        print("- Real-time monitoring and stats")
        print("\nAgent Roles:")
        for role in AgentRole:
            print(f"- {role.value.title()}: Specialized agent type")
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
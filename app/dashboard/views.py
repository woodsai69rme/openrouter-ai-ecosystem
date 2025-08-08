"""
Dashboard views
"""
from flask import render_template_string, session, redirect, url_for
from app.core.config import Config
from app.api.agents import agent_system, init_agent_system
from . import dashboard_bp

@dashboard_bp.route('/')
def index():
    """Main dashboard"""
    init_agent_system()
    
    user_tier = session.get('user_tier', 'free')
    tier_info = Config.PRICING_TIERS[user_tier]
    
    status = agent_system.get_system_status()
    
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>AI Agent Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: #667eea; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .tier-info { background: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #2196f3; }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); flex: 1; min-width: 200px; }
        .stat-value { font-size: 2em; color: #667eea; font-weight: bold; }
        .agents, .tasks { background: white; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .agent-card, .task-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .btn { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #5a6fd8; }
        .btn-pro { background: #ff6b6b; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Agent Dashboard</h1>
        <p>Manage your autonomous AI agents • Current Plan: <strong>{{ user_tier.title() }}</strong></p>
    </div>
    
    <div class="tier-info">
        <h3>{{ tier_info.name }} Plan</h3>
        <p><strong>Agents:</strong> {{ tier_info.agents_limit if tier_info.agents_limit != -1 else 'Unlimited' }} | 
           <strong>Tasks/hour:</strong> {{ tier_info.tasks_per_hour if tier_info.tasks_per_hour != -1 else 'Unlimited' }} | 
           <strong>Cost:</strong> ${{ tier_info.price }}/month</p>
        {% if user_tier == 'free' %}
        <a href="/billing/upgrade/pro" class="btn btn-pro">Upgrade to Pro - $29/month</a>
        {% endif %}
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{{ status.agents|length }}</div>
            <div>Active Agents</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ status.system_stats.total_tasks }}</div>
            <div>Total Tasks</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ status.system_stats.completed_tasks }}</div>
            <div>Completed</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">$0.00</div>
            <div>OpenRouter Cost</div>
        </div>
    </div>
    
    <div class="agents">
        <h3>Your Agents</h3>
        {% for agent_id, agent in status.agents.items() %}
        <div class="agent-card">
            <h4>{{ agent.id }} ({{ agent.role }})</h4>
            <p>Status: {{ agent.status }} | Completed: {{ agent.completed_tasks }} tasks</p>
        </div>
        {% endfor %}
        
        {% if status.agents|length < tier_info.agents_limit or tier_info.agents_limit == -1 %}
        <button class="btn" onclick="createAgent()">Create Agent</button>
        {% endif %}
    </div>
    
    <div class="tasks">
        <h3>Tasks</h3>
        {% for task_id, task in status.tasks.items() %}
        <div class="task-card">
            <h4>{{ task.id }}</h4>
            <p>{{ task.status }} | Type: {{ task.type }}</p>
        </div>
        {% endfor %}
        
        <button class="btn" onclick="createTask()">Create Task</button>
    </div>
    
    <script>
        function createAgent() {
            const agentId = prompt("Agent ID:");
            const role = prompt("Role (coordinator/researcher/coder/writer/analyst/reviewer/executor):");
            if (agentId && role) {
                fetch('/api/agents', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({agent_id: agentId, role: role})
                }).then(() => location.reload());
            }
        }
        
        function createTask() {
            const taskId = prompt("Task ID:");
            const description = prompt("Description:");
            const type = prompt("Type (research/code_analysis/documentation):");
            if (taskId && description && type) {
                fetch('/api/tasks', {
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({task_id: taskId, description: description, task_type: type})
                }).then(() => location.reload());
            }
        }
    </script>
</body>
</html>
    """, 
    status=status,
    user_tier=user_tier,
    tier_info=tier_info)
"""
Agent API endpoints
"""
from flask import request, jsonify, session
from app.core import MultiAgentSystem, AgentRole
from app.core.config import Config
from . import api_bp

# Global system instance
agent_system = MultiAgentSystem()

def init_agent_system():
    """Initialize the agent system with demo agents"""
    try:
        agent_system.create_agent('demo_coordinator', AgentRole.COORDINATOR)
        agent_system.create_agent('demo_researcher', AgentRole.RESEARCHER)
        agent_system.create_agent('demo_coder', AgentRole.CODER)
    except:
        pass  # Agents might already exist

@api_bp.route('/agents', methods=['POST'])
def create_agent():
    """Create a new agent"""
    init_agent_system()
    
    try:
        data = request.json
        user_tier = session.get('user_tier', 'free')
        tier_limits = Config.PRICING_TIERS[user_tier]
        
        # Check limits
        current_agents = len(agent_system.agents)
        if tier_limits['agents_limit'] != -1 and current_agents >= tier_limits['agents_limit']:
            return jsonify({'error': 'Agent limit reached. Please upgrade.'}), 403
        
        agent_id = data['agent_id']
        role = AgentRole[data['role'].upper()]
        
        agent = agent_system.create_agent(agent_id, role)
        return jsonify({'success': True, 'agent_id': agent_id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/agents', methods=['GET'])
def list_agents():
    """List all agents"""
    init_agent_system()
    status = agent_system.get_system_status()
    return jsonify({
        'agents': [{
            'id': agent.id,
            'role': agent.role.value,
            'status': agent.status,
            'completed_tasks': agent.completed_tasks
        } for agent in status.agents.values()]
    })

@api_bp.route('/status', methods=['GET'])
def get_status():
    """Get system status"""
    init_agent_system()
    status = agent_system.get_system_status()
    return jsonify({
        'agents': len(status.agents),
        'tasks': status.system_stats.total_tasks,
        'completed': status.system_stats.completed_tasks,
        'cost': 0.00
    })
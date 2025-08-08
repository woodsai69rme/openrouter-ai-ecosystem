"""
Task API endpoints
"""
from flask import request, jsonify
from app.api.agents import agent_system, init_agent_system
from . import api_bp

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    init_agent_system()
    
    try:
        data = request.json
        task = agent_system.create_task(
            data['task_id'],
            data['description'],
            data['task_type']
        )
        
        # Auto-assign task
        agent_system.assign_task(task.id)
        
        return jsonify({'success': True, 'task_id': task.id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/tasks', methods=['GET'])
def list_tasks():
    """List all tasks"""
    init_agent_system()
    status = agent_system.get_system_status()
    return jsonify({
        'tasks': [{
            'id': task.id,
            'status': task.status,
            'type': task.type,
            'description': task.description
        } for task in status.tasks.values()]
    })
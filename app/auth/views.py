"""
Authentication views
"""
from flask import render_template_string, session, request, redirect, url_for, jsonify
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login form"""
    if request.method == 'POST':
        # Simple demo login - in production use proper authentication
        email = request.form.get('email')
        if email:
            session['user_email'] = email
            session['user_tier'] = 'free'
            return redirect('/dashboard')
    
    return render_template_string("""
    <h2>Login</h2>
    <form method="POST">
        <input type="email" name="email" placeholder="Email" required>
        <button type="submit">Login</button>
    </form>
    <p><a href="/">Back to Home</a></p>
    """)

@auth_bp.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect('/')
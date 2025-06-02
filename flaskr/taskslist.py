from flask_login import login_required, current_user

@tasklists_bp.route('/tasklists')
@login_required
def list_tasklists():

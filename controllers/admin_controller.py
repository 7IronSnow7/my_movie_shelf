# controllers/admin_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.user import User
from models import db
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with user statistics"""
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    regular_users = total_users - admin_users
    
    return render_template('admin/admin_dashboard.html', 
                         total_users=total_users,
                         admin_users=admin_users,
                         regular_users=regular_users)

@admin_bp.route('/users')
@login_required
@admin_required
def view_users():
    """View all users with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of users per page
    
    users = User.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>')
@login_required
@admin_required
def view_user_details(user_id):
    """View detailed information about a specific user"""
    user = User.query.get_or_404(user_id)
    
    # Get user's movie statistics
    total_movies = len(user.movies) if hasattr(user, 'movies') else 0
    watched_movies = len([m for m in user.movies if m.watched]) if hasattr(user, 'movies') else 0
    
    return render_template('admin/user_details.html', 
                         user=user,
                         total_movies=total_movies,
                         watched_movies=watched_movies)

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.view_users'))
    
    try:
        # Delete the user
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'User "{username}" has been deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin.view_users'))

@admin_bp.route('/users/bulk-delete', methods=['POST'])
@login_required
@admin_required
def bulk_delete_users():
    """Delete multiple users at once"""
    user_ids = request.form.getlist('user_ids')
    
    if not user_ids:
        flash('No users selected for deletion.', 'error')
        return redirect(url_for('admin.view_users'))
    
    # Convert to integers and filter out current user
    user_ids = [int(uid) for uid in user_ids if int(uid) != current_user.id]
    
    if not user_ids:
        flash('Cannot delete your own account or no valid users selected.', 'error')
        
    try:
        # Check usernames for confirmation message
        users_to_delete = User.query.filter(User.id.in_(user_ids)).all()
        usernames = [user.username for user in users_to_delete]\
        
        # Delete users
        User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
        db.session.commit()
        flash(f'Successfully deleted {len(usernames)} users: {", ".join(usernames)}','success' )
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting users: {str(e)}', 'error')
    
    return redirect(url_for('admin.view_users'))
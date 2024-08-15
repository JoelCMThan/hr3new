from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import User, Complaint
from app.blueprints.admin import admin

@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_users = User.query.count()
    total_complaints = Complaint.query.count()
    pending_complaints = Complaint.query.filter_by(status='Pending').count()
    return render_template('admin/admin_dashboard.html', total_users=total_users, total_complaints=total_complaints, pending_complaints=pending_complaints)

@admin.route('/admin/manage_users')
@login_required
def manage_users():
    search = request.args.get('search')
    users_query = User.query

    if search:
        users_query = users_query.filter(User.username.ilike(f'%{search}%') | User.email.ilike(f'%{search}%'))

    users = users_query.paginate(page=request.args.get('page', 1, type=int), per_page=10)
    return render_template('admin/manage_users.html', users=users)

@admin.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.role = request.form['role']
        db.session.commit()
        flash('User role updated successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/edit_user.html', user=user)

@admin.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted.', 'success')
    return redirect(url_for('admin.manage_users'))

@admin.route('/admin/manage_complaints')
@login_required
def manage_complaints():
    if current_user.role != 'admin':
        abort(403)
    search = request.args.get('search')
    status = request.args.get('status')
    complaints_query = Complaint.query

    if search:
        complaints_query = complaints_query.filter(Complaint.title.ilike(f'%{search}%') | Complaint.author.has(User.username.ilike(f'%{search}%')))

    if status:
        complaints_query = complaints_query.filter_by(status=status)

    complaints = complaints_query.paginate(page=request.args.get('page', 1, type=int), per_page=10)
    return render_template('admin/manage_complaints.html', complaints=complaints)

@admin.route('/admin/update_complaint_status/<int:complaint_id>', methods=['POST'])
@login_required
def update_complaint_status(complaint_id):
    if current_user.role != 'admin':
        abort(403)
    complaint = Complaint.query.get_or_404(complaint_id)
    new_status = request.form.get('status')
    if new_status in ['In Review', 'Resolved', 'Closed']:
        complaint.status = new_status
        db.session.commit()
        flash(f'Complaint status updated to {new_status}.', 'success')
    else:
        flash('Invalid status update.', 'danger')
    return redirect(url_for('admin.manage_complaints'))

@admin.route('/admin/complaint_detail/<int:complaint_id>')
@login_required
def complaint_detail(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    return render_template('complaint_detail.html', complaint=complaint)

@admin.route('/admin/delete_complaint/<int:complaint_id>', methods=['POST'])
@login_required
def delete_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    db.session.delete(complaint)
    db.session.commit()
    flash('Complaint has been deleted.', 'success')
    return redirect(url_for('admin.manage_complaints'))

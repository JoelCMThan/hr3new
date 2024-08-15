from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from app import db
from app.forms import ComplaintReviewForm
from app.models import Complaint
from app.blueprints.manager import manager

@manager.route('/manager/dashboard')
@login_required
def manager_dashboard():
    total_team_complaints = Complaint.query.filter_by(team_id=current_user.team_id).count()
    pending_reviews = Complaint.query.filter_by(team_id=current_user.team_id, status='Pending').count()
    return render_template('manager_dashboard.html', total_team_complaints=total_team_complaints, pending_reviews=pending_reviews)

@manager.route('/manager/team_complaints')
@login_required
def team_complaints():
    search = request.args.get('search')
    status = request.args.get('status')
    complaints_query = Complaint.query.filter_by(team_id=current_user.team_id)

    if search:
        complaints_query = complaints_query.filter(Complaint.title.ilike(f'%{search}%'))

    if status:
        complaints_query = complaints_query.filter_by(status=status)

    complaints = complaints_query.paginate(page=request.args.get('page', 1, type=int), per_page=10)

    return render_template('team_complaints.html', complaints=complaints)

@manager.route('/manager/complaint_review/<int:complaint_id>', methods=['GET', 'POST'])
@login_required
def complaint_review(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    if complaint.team_id != current_user.team_id:
        abort(403)

    form = ComplaintReviewForm()
    if form.validate_on_submit():
        complaint.status = form.status.data
        complaint.notes = form.notes.data
        db.session.commit()
        flash('The complaint has been updated.', 'success')
        return redirect(url_for('manager.team_complaints'))

    form.status.data = complaint.status
    form.notes.data = complaint.notes
    return render_template('complaint_review.html', form=form, complaint=complaint)

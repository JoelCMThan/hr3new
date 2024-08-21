from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from app import db
from app.forms import ComplaintForm
from app.models import Complaint
from app.blueprints.employee import employee
from app.forms import LeaveApplicationForm
from app.models import Leave

@employee.route('/')
@employee.route('/index')
def index():
    return render_template('index.html')

@employee.route('/dashboard')
@login_required
def dashboard():
    complaints = Complaint.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', complaints=complaints)

@employee.route('/complaint/new', methods=['GET', 'POST'])
@login_required
def new_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(title=form.title.data, description=form.description.data, author=current_user)
        db.session.add(complaint)
        db.session.commit()
        flash('Your complaint has been submitted.', 'success')
        return redirect(url_for('employee.dashboard'))
    return render_template('complaint_form.html', form=form)

@employee.route('/complaint/<int:complaint_id>')
@login_required
def complaint_detail(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    if complaint.author != current_user:
        abort(403)
    return render_template('complaint_detail.html', complaint=complaint)

@employee.route('/apply_leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    form = LeaveApplicationForm()
    if form.validate_on_submit():
        leave = Leave(
            user_id=current_user.id,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            reason=form.reason.data
        )
        db.session.add(leave)
        db.session.commit()
        flash('Your leave application has been submitted!', 'success')
        return redirect(url_for('employee.leave_status'))
    return render_template('apply_leave.html', title='Apply for Leave', form=form)

@employee.route('/leave_status')
@login_required
def leave_status():
    leaves = Leave.query.filter_by(user_id=current_user.id).order_by(Leave.application_date.desc()).all()

    total_applied_days = sum(leave.leave_days for leave in leaves if leave.status in ['Pending', 'Approved', 'Rejected'])
    total_approved_days = sum(leave.leave_days for leave in leaves if leave.status == 'Approved')
    total_rejected_days = sum(leave.leave_days for leave in leaves if leave.status == 'Rejected')
    
    total_leave_entitlement = 30  # Example total leave entitlement per year
    total_remaining_days = total_leave_entitlement - total_approved_days

    return render_template('leave_status.html', 
                           title='My Leave Applications', 
                           leaves=leaves, 
                           total_applied_days=total_applied_days,
                           total_approved_days=total_approved_days,
                           total_rejected_days=total_rejected_days,
                           total_remaining_days=total_remaining_days)

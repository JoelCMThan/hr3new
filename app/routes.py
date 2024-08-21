from flask import render_template, url_for, flash, redirect, request
from app import db
from app.forms import ComplaintForm
from app.models import Complaint
from flask_login import login_required, current_user
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
    return render_template('complaint_form.html', title='New Complaint', form=form)

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

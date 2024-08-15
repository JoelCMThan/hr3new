from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from app import db
from app.forms import ComplaintForm
from app.models import Complaint
from app.blueprints.employee import employee

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

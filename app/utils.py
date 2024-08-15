from flask import url_for
from flask_mail import Message
from app import mail

def send_email(user, subject, template, **kwargs):
    msg = Message(subject, recipients=[user.email])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

def save_file(form_file, folder):
    filename = secure_filename(form_file.filename)
    file_path = os.path.join(current_app.root_path, 'static', folder, filename)
    form_file.save(file_path)
    return filename

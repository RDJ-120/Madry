# save as app.py
from flask import Flask, request, send_from_directory
import smtplib
from email.message import EmailMessage

app = Flask(__name__, static_folder='.')

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "mazen34554@gmail.com"      # ايميلك
SMTP_PASS = "12345678911q"              # باسوردك
TO_EMAIL  = "mazen37667@gmail.com"      # الايميل اللي توصله الرسالة

def send_ip_email(ip, path):
    msg = EmailMessage()
    msg['Subject'] = f'New site visit from {ip}'
    msg['From'] = SMTP_USER
    msg['To'] = TO_EMAIL
    msg.set_content(f'Visitor IP: {ip}\nRequested path: {path}')
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)

@app.route('/', defaults={'p': 'index.html'})
@app.route('/<path:p>')
def serve(p):
    xff = request.headers.get('X-Forwarded-For', '')
    ip = xff.split(',')[0].strip() if xff else request.remote_addr
    try:
        send_ip_email(ip, request.path)
    except:
        pass
    return send_from_directory('.', p)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

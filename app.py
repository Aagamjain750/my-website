from flask import Flask, render_template, request, redirect, url_for, session
import os
import random
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Serve static index.html at root for Fast2SMS verification
@app.route('/')
def home():
    return app.send_static_file('index.html')

# Project form page
@app.route('/project_form', methods=['GET', 'POST'])
def project_form():
    if request.method == 'POST':
        phone = request.form['phone']
        otp = str(random.randint(1000, 9999))
        session['phone'] = phone
        session['otp'] = otp

        # Send OTP via Fast2SMS
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = {
                "variables_values": otp,
                "route": "otp",
                "numbers": phone,
                "message": f"Your OTP is {otp}"
            }
            headers = {
                "authorization": os.getenv("FAST2SMS_API_KEY") or "YOUR_API_KEY",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            response = requests.post(url, data=payload, headers=headers)
            print("Fast2SMS Response:", response.text)
        except Exception as e:
            return f"Error sending SMS: {e}"

        return redirect(url_for('otp_verify'))

    return render_template('project_form.html')

# OTP verification page
@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    phone = session.get('phone')
    otp = session.get('otp')

    if not phone or not otp:
        return redirect(url_for('project_form'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == otp:
            return "✅ OTP Verified Successfully!"
        else:
            return "❌ Invalid OTP, try again."

    return render_template('otp_verify.html')

# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
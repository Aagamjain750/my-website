import os
import random
import requests
from flask import Flask, render_template, request, redirect, url_for, session

# Load Fast2SMS API key from environment variable
FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY") or "tFkXluLIbg4xKep9WyqcPQaBzCZS6j2sOi13oJ0wm5NGnAUfH80SQIALD2l3WxX64km19NMip8vEOZRU"

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Used for session management

# Temporary in-memory OTP store
otp_store = {}

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Project submission form
@app.route('/project_form', methods=['GET', 'POST'])
def project_form():
    if request.method == 'POST':
        phone = request.form['phone']
        otp = str(random.randint(1000, 9999))
        otp_store[phone] = otp
        print(f"OTP for {phone} is {otp}")  # Debugging

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
                "authorization": FAST2SMS_API_KEY,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            response = requests.post(url, data=payload, headers=headers)
            print("Fast2SMS Response:", response.text)
            if response.status_code != 200:
                return f"SMS Error: {response.text}"
        except Exception as e:
            return f"Error sending SMS: {e}"

        session['phone'] = phone
        return redirect(url_for('otp_verify'))

    return render_template('project_form.html')

# OTP verification page
@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    phone = session.get('phone')
    if not phone:
        return redirect(url_for('home'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if otp_store.get(phone) == entered_otp:
            return "✅ OTP Verified Successfully!"
        else:
            return "❌ Invalid OTP, try again."

    return render_template('otp_verify.html')

# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
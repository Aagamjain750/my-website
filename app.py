import os
import random
import requests
from flask import Flask, render_template, request, redirect, url_for, session

FAST2SMS_API_KEY = os.getenv("FAST2SMS_API_KEY") or "tFkXluLIbg4xKep9WyqcPQaBzCZS6j2sOi13oJ0wm5NGnAUfH80SQIALD2l3WxX64km19NMip8vEOZRU"

app = Flask(__name__)
app.secret_key = "supersecretkey"

otp_store = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project_form', methods=['GET', 'POST'])
def project_form():
    if request.method == 'POST':
        phone = request.form['phone']
        otp = str(random.randint(1000, 9999))
        otp_store[phone] = otp
        print(f"OTP for {phone} is {otp}")  # Debugging

        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = {
                "variables_values": otp,
                "route": "otp",
                "numbers": phone
            }
            headers = {
                "authorization": FAST2SMS_API_KEY
            }
            response = requests.post(url, data=payload, headers=headers)
            print("Fast2SMS Response:", response.text)  # Debugging
            if response.status_code != 200:
                return f"SMS Error: {response.text}"
        except Exception as e:
            return f"Error: {e}"

        session['phone'] = phone
        return redirect(url_for('otp_verify'))

    return render_template('project_form.html')

@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    phone = session.get('phone')
    if not phone:
        return redirect(url_for('home'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if phone in otp_store and otp_store[phone] == entered_otp:
            return "✅ OTP Verified Successfully!"
        else:
            return "❌ Invalid OTP, try again."

    return render_template('otp_verify.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
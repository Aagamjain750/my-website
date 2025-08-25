# otp_store.py

otp_data = {}

def store_otp(email, otp):
    otp_data[email] = otp

def get_otp(email):
    return otp_data.get(email)

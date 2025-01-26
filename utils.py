# Removed Twilio OTP sending function
# from twilio.rest import Client
# from flask import current_app

# def send_otp(phone_number, otp):
#     if not phone_number.startswith('+'):
#         phone_number = '+91' + phone_number  # Default to India country code

#     client = Client(current_app.config['TWILIO_ACCOUNT_SID'], current_app.config['TWILIO_AUTH_TOKEN'])
#     message = client.messages.create(
#         body=f"Thank you for signing up to EduPulse. Your OTP is {otp}",
#         from_=current_app.config['TWILIO_PHONE_NUMBER'],
#         to=phone_number
#     )
#     return message.sid

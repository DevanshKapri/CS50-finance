# create smtp session
import math
import smtplib
import random

s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 is a port number
# start TLS for E-mail security
s.starttls()
# Log in to your gmail account
s.login("pythonprojectcse@gmail.com", "python@12@urass")
digits = "0123456789"
OTP = ""
for i in range(6):
    OTP += digits[math.floor(random.random() * 10)]
otp = OTP + " is your OTP"

s.sendmail("pythonprojectcse@gmail.com", "miankitsingh@gmail.com", otp)
print("OTP sent successfully..")
# close smtp session
s.quit()

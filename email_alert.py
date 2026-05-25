import smtplib

def send_email(status,severity):

    sender = "your_email@gmail.com"
    password = "your_password"

    receiver = "emergency@gmail.com"

    message = f"""
    Subject: Accident Alert

    Accident Status: {status}
    Severity Level: {severity}

    Please respond immediately.
    """

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(sender,password)

    server.sendmail(sender,receiver,message)

    server.quit()
import smtplib
import time
import requests
import re
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_time(url, payload, headers):
    req = requests.post(url, data=payload, headers=headers)
    print(req.text)
    return req


def send_time(sender_address, sender_pass, receiver_address, subject, mail_content):
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject  # The subject line
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('', 111)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    # session.sendmail(sender_address, receiver_address2, text)
    session.quit()
    print('Mail Sent')


if __name__ == '__main__':
    today = date.today()
    url_ServiceOntario = "https://eab.services.gov.on.ca/api/availableDays"

    payload_ServiceOntario = {"locationCode": "918", "startDate": today, "numberOfDays": "40", "purposeCodeList": "MM2"}

    headers_ServiceOntario = {
        "Origin": "https://eab.services.gov.on.ca",
        "Referer": "https://www.services.gov.on.ca/sf/"
    }
    dates = []
    sender = ''
    pas = ''
    receiver = ''
    while 1:
        r = get_time(url_ServiceOntario, payload_ServiceOntario, headers_ServiceOntario)
        r_dates = re.sub(r'\[|\]|"', '', r.text).split(",")
        if r_dates != dates:
            for date in r_dates:
                if date not in dates and int(date[5:7]) < 10:
                    print(r_dates)
                    separator = ", "
                    send_time(sender, pas, receiver, "time slot available", "time: " + separator.join(str(item) for
                                                                                                      item in
                                                                                                      r_dates))
                    break
            dates = r_dates
        time.sleep(20)

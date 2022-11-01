import smtplib
import mimetypes
from email.message import EmailMessage
from smtplib import *
import os

##TODO
##Обработка ошибок Сети
##MIME формат письма: присоединить картинки
##Заголовки письма: Subject, From и т. д.
## Что такое сессия и транзакция SMTP, одно и тоже?
## С какой команды начинаются и какой заканчиваются?
## MIME


def attach_file_to_email(message, file_name):
    with open(file_name, 'rb') as file_opened:
        file_data = file_opened.read()
        maintype, _, subtype = (mimetypes.guess_type(file_name)[0] or 'application/octet-stream').partition("/")
        message.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)


def send_mail_smtp(mail, host, username, password):
    s = smtplib.SMTP(host)
    s.starttls()
    s.login(username, password)
    s.send_message(mail)
    s.quit()


host_addr = 'smtp.yandex.ru'
port = 465
user_name = 'NonBandit@yandex.ru'
password = 'wtvaimopvolnptbc'
current_directory = os.getcwd()

with open(current_directory + "\\message\\configurations.txt", encoding='utf-8') as file:
    data = file.read()
lines = data.split("\n")
recipients = lines[0].split(" ")
theme = lines[1]
attachment_names = lines[2].split(" ")

msg = EmailMessage()
msg['From'] = user_name
msg['To'] = ", ".join(recipients)
msg['Subject'] = "Add it later"
with open(current_directory + "\\message\\text.txt", encoding='utf-8') as file:
    data = file.read()
msg.set_content(data)

for a in attachment_names:
    attach_file_to_email(msg, current_directory + "\\message\\" + a)

try:
    send_mail_smtp(msg, host_addr, user_name, password)
except SMTPResponseException as e:
    print(e.smtp_code)
    print(e.smtp_error)

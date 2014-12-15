#!/usr/bin/python
# Match people for secret santa, and email out notifications.


class Santa:

    def __init__(self, santa_name, santa_email):
        self.name = santa_name
        self.email = santa_email
        self.receiver_name = ""
        self.receiver_email = ""


def send_email(from_address, to_address, subject, message):
    # Send emails from your email to the Santas.
    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    msg.attach(MIMEText(message, 'plain'))

    username = "<Your Email Login Username>"
    password = "<Your Email Login Password>"

    server = smtplib.SMTP("<Your Email SMTP Server:Port>")
    server.starttls()
    server.login(username, password)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()

    logging.info(msg)


def get_yn(question):
    # Ask yes/no questions.  Return True if yes, False if no.
    while True:
        yn = raw_input(question + " [y/n]")
        if yn.lower().startswith('y'):
            return True
        elif yn.lower().startswith('n'):
            return False
        else:
            print("Please enter yes or no")


def derange(arranged_list):
    # Take a list, and dearrange it so that no item is in its original place.

    shuffled_list = list(arranged_list)
    import random
    random.shuffle(shuffled_list)

    print('\n')

    while True:
        match = False
        for arranged_santa, shuffled_santa in zip(arranged_list, shuffled_list):
            if arranged_santa == shuffled_santa:
                match = True
        if match:
            print("Finding appropriate matches...")
            random.shuffle(shuffled_list)
        else:
            print('\n')
            print("Done finding matches!")
            return shuffled_list

santa_list = []

while True:
    print("Enter A Secret Santa or Q to quit")

    full_name = str(raw_input("Name : "))
    if full_name.lower() == 'q':

        print('\n')
        for santa_person in santa_list:
            print (santa_person.name, santa_person.email)

        print('\n')
        if get_yn("Is the above list correct?"):
            break

    email_address = str(raw_input("Email: "))

    newSanta = Santa(full_name, email_address)
    santa_list.append(newSanta)

deranged_list = derange(list(santa_list))

print('\n')

import logging
logging.basicConfig(filename="ss.log", level=logging.DEBUG)

print('\n')
print("Sending emails, this may take a minute or two...")

for santas, deranged in zip(santa_list, deranged_list):
    santas.receiver_name = deranged.name
    santas.receiver_email = deranged.email

    email_subject = "<Your Email Subject>"
    email_message = "Hello %s, Your Secret Santa is %s.  Get them an awesome present!" \
        % (santas.name, santas.receiver_name)

    send_email("<Your Email From Address>", santas.email, email_subject, email_message)

print('\n')
print("Emails sent!  Goodbye!")

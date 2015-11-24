#!/usr/bin/python

import sys
import random
import csv
import getpass

#####NOTES######
# if using gmail, need to sign on to your account and allow
# less secure apps to send mail
# https://myaccount.google.com/security
################

# this code is a modified version of gmail python code found at
# http://stackoverflow.com/questions/10147455/trying-to-send-email-gmail-as-mail-provider-using-python
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print "Email successfully sent for {}".format(recipient)
        return True
    except:
        print "Failed to sent email to {}".format(recipient)
        return False


def main():
    # Variable definitions
    emails = {}
    givers = []
    
    # Parse CSV (get emails as dict and names as list)
    with open('participants.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] is not '':
                emails[row['Name']] = row['Email']
                givers.append(row['Name'])
    
    # Create a list of receivers
    receivers = list(givers)
    
    # Shuffle receivers list.
    random.shuffle(receivers)

    # Loop through and make sure no one has themselves.
    for i in range(0,len(givers)):
        if (givers[i] == receivers[i]):
            if (i == len(givers)-1):
                receivers[i] = receivers[0]
                receivers[0] = givers[i]
            else:
                receivers[i] = receivers[i+1]
                receivers[i+1] = givers[i]
    
    # Get program user's email and password to send emails to participants
    user_email = raw_input("Please enter your gmail: ")
    password = getpass.getpass("Password: ")
    
    # Email users their person they are giving
    for person in range(len(givers)):
        if (givers[person] in emails):
            message = "You are giving a gift to %s" % receivers[person]
            if not send_email(user_email, password, emails[givers[person]], "Secret Santa", message):
                print "Email failed for %s's email %s" % (givers[person], emails[givers[person]])
                print "Information stored in %s.txt. Please send at a later time" % givers[person]
                f = open(givers[person]+'.txt', 'w') 
                f.write(message)
                f.close()
                

if (__name__ == '__main__'):
    main()









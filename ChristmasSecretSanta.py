#!/usr/bin/python

import sys
import random
import csv
import getpass


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

def print_to_file(giver, msg):
    print "Information stored in %s.txt. Please send at a later time" % giver
    f = open(giver+'.txt', 'w') 
    f.write(msg)
    f.close()
 
# this code is from a stackoverflow answer
# http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = raw_input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    return choice.strip().lower() in values


def main():
    # Variable definitions
    emails = {}
    givers = []

    # Get csv file from user
    csvname = raw_input("Please enter the name (including path) of CSV file: ")
    
    # Parse CSV (get emails as dict and names as list)
    with open(csvname) as csvfile:
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
   
    # If user chooses, create string for checking by third party
    yn_ans = yn_choice("Do you want a 3rd party checker? ")
    if yn_ans:
        checker_email = raw_input("Please enter the third party checker's email: ")
        checker_msg = ""

    # Email users their person they are giving
    for person in range(len(givers)):
        message = "You are giving a gift to %s" % receivers[person]
        if (givers[person] in emails):
            if not send_email(user_email, password, emails[givers[person]], "Secret Santa", message):
                print "Email failed for %s's email %s" % (givers[person], emails[givers[person]])
                print_to_file(givers[person], message)
        else:
            print "%s email does not match." % givers[person]
            print_to_file(givers[person], message)
        message = "%s is giving a gift to %s" % (givers[person], receivers[person])
        checker_msg += (message+"\n")

    if yn_ans:
        print "\nSending email to third party checker for sanity"
        send_email(user_email, password, checker_email, "Please check that there is nothing wrong!", checker_msg)

                

if (__name__ == '__main__'):
    main()









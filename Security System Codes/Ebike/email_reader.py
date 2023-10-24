import imaplib
import email
import time
import security_functions as security
import gps_functions as gps
import email_functions
import io_functions as io
import prog


SENDER = "myrpitesting2001@gmail.com" 
PASSWORD = "kghlfejsikandmjp"

prog.start()
while prog.isRunning():
    email_messages = []

    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com') #set up connection for reading email
        mail.login(SENDER, PASSWORD)
        mail.select("INBOX")
        #check FROM "+12035836086@mailmymobile.net"
        _, selected_mails = mail.search(None, 'UNSEEN',
                                        '(FROM "+12035836086@mailmymobile.net")') #'(FROM "chenchangkai2003@gmail.com")'
        for num in selected_mails[0].split():
            _, data = mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
            email_message = email.message_from_bytes(bytes_data) #convert the byte data to message
            for part in email_message.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    message = part.get_payload(decode=True)
                    prog.namePrint('Email received')
                    email_messages.append(message.decode().upper())
                    break
        #check FROM "chenchangkai2003@gmail.com"
        _, selected_mails = mail.search(None, 'UNSEEN',
                                        '(FROM "chenchangkai2003@gmail.com")')
        for num in selected_mails[0].split():
            _, data = mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
            email_message = email.message_from_bytes(bytes_data) #convert the byte data to message
            for part in email_message.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    message = part.get_payload(decode=True)
                    prog.namePrint('Email received')
                    email_messages.append(message.decode().upper())
                    break
        #check FROM "chc038@ucsd.edu"
        _, selected_mails = mail.search(None, 'UNSEEN',
                                        '(FROM "chc038@ucsd.edu")')
        for num in selected_mails[0].split():
            _, data = mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
            email_message = email.message_from_bytes(bytes_data) #convert the byte data to message
            for part in email_message.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    message = part.get_payload(decode=True)
                    prog.namePrint('Email received')
                    email_messages.append(message.decode().upper())
                    break
        mail.close()
        mail.logout()
    except Exception as e:
        print('read_emails: ' + repr(e))

    #check the email messages
    for msg_up in email_messages:
        if 'UNLOCK' in msg_up:
            security.unlockSequence()
        elif 'LOCK' in msg_up:
            security.lockSequence()
        elif 'HOME' in msg_up:
            security.homeSequence()
        elif 'GPS' in msg_up:
            email_functions.sendPhotoEmail(subject='Ebike Information',
                                           message=gps.getGPSLocation() +'\nAge: ' +
                                           gps.strfGPSAge() + '\n' +
                                           time.strftime('%c'))
        elif 'INFO' in msg_up or 'INFORMATION' in msg_up:
            info = "\n" + '-'*30 + "\n" + time.strftime('%c') + "\n" + '-'*30 + "\n"
            info += gps.strfGPSInfo()
            info += io.strfOutputs() + io.strfInfos() + io.strfInfosADC() + io.strfInfosVESC()
            info += security.securityInfo()
            email_functions.sendPhotoEmail(subject="Ebike Information", message=info)
    
    #wait 10 seconds before next check
    prog.sleep(10)


prog.end()


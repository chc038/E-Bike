import yagmail #sudo pip install yagmail
import email_functions as email
import prog
import time


SENDER = "myrpitesting2001@gmail.com" 
RECEIVER = "chenchangkai2003@gmail.com"
PASSWORD = "utujjnboixlyklae"


email.sendEmail(subject="Ebike Operations", message=__file__ + " started")

prog.start()
while prog.isRunning():
    #get emails from list and send them
    email_messages = email.getEmails()
    if email_messages != None and len(email_messages) > 0:
        try:
            with yagmail.SMTP(SENDER, PASSWORD) as yag:
                for email_message in email_messages:
                    #send each email meaasge
                    yag.send(
                        to=RECEIVER,
                        subject=email_message['subject'],
                        contents=email_message['message'], 
                        attachments=email_message['attatchments'],
                    )
                    time.sleep(1)
            #clear the email messages if sent successfully
            email.clearEmails()
        except Exception as e:
            prog.timePrint(repr(e))
    
    time.sleep(0.1)


prog.end()

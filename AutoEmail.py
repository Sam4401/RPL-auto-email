#Sam Nath Version 0.0.1 3/24/2022
#Mostly stolen from the internet
#troubleshooting: mess with the apispreadsheets
#https://www.apispreadsheets.com/upload
#it will be unhappy if the titles or format is changed

import requests
import smtplib

modifyEmail = True  #set to true if you want the option of customizing emails
askApprovalBeforeSend = False # must be on if modify is on
your_name = "Project Test"
your_email = "projecttest4401@gmail.com"
your_password = "Strong@4000" #must update if password is changed
yes = ['y','Yes','(Y)', 'Y', 'yes', 'YES']
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(your_email, your_password)

# Read the google sheet from api spreadsheets
print('Retrieving Data (may take up to a minute) \n ... \n ...')
r = requests.get("https://api.apispreadsheets.com/data/y4gi6UvdW0u8Vo2Q/")

if r.status_code == 200:
	# SUCCESS
	data = r.json()["data"]
	print("Data Retrieval: SUCCESS \n")
else:
	# ERROR
	data=None
	print("Data Retrieval: ERROR")



idx = int(input("Row number of email recepient: \n"))-1

while idx != "EXIT":
    # Get target name, email adress, and generate email.
    name = data[idx]["1"].strip()
    firstname = name[:name.index(' ')]
    email = data[idx]["43"].strip()
    #subject = data[idx]["Subject"].strip()
    subject = "RPL part Ready for Pickup"
    #modify if u dont like the email
    message = "Hi "+ firstname+ ", \n \n" \
        "Your part(s) are ready for pickup outside the RPL." \
        " Let us know if you have any questions or concerns. \n  \nRPL Staff"

    # Create the email to send
    full_email = ("From: {0} <{1}>\n"
                  "To: {2} <{3}>\n"
                  "Subject: {4}\n\n"
                  "{5}"
                  .format(your_name, your_email, name, email, subject, message))

    if askApprovalBeforeSend == True:
        print(full_email)
        #optional modify email setting
        if modifyEmail == True:
            change = input('would you like to change the email (Y)/(N):\n ')
            unhappy = True
            while unhappy == True:
                if yes.count(change) > 0:
                    greeting = input('Greeting: \n')
                    messageBody = input('Enter Message body: \n')
                    Signature = input('Enter signature: \n')
                    message = greeting + '\n\n' + messageBody + '\n\n' + Signature
                    full_email = ("From: {0} <{1}>\n"
                                  "To: {2} <{3}>\n"
                                  "Subject: {4}\n\n"
                                  "{5}"
                                  .format(your_name, your_email, name, email, subject, message))
                    print(full_email)

                    doneYet = input('would you like to change the email again? (Y)/(N):\n ')
                    if yes.count(doneYet) > 0:
                        unhappy = True
                    else:
                        unhappy = False
                else:
                    unhappy = False





        # In the email field, you can add multiple other emails if you want
        # all of them to receive the same text
    try:
        if askApprovalBeforeSend == True:
            approve = input('Send? (Y)/(N): \n' )
            if yes.count(approve) > 0:
                server.sendmail(your_email, [email], full_email)
                print('Email to {} successfully sent!\n\n'.format(email))
            else:
                print('Email not sent')
        else:
            server.sendmail(your_email, [email], full_email)
            print('Email to {} successfully sent!\n\n'.format(email))

    except Exception as e:
        print('Email to {} could not be sent :( because {}\n\n'.format(email, str(e)))
    idx = input("Row number of email recepient or EXIT to quit: \n")
    if idx != "EXIT":
        idx = int(idx)-1
# Close the smtp server
server.close()

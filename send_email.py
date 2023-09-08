import os
import re
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def convert_email_list(emails):
    if isinstance(emails,str):
        emails = emails.replace(";",",")
        emails = emails.split(",")
    return emails


def send_email(user, password,message_type,server,from_address,to,cc,bcc, subject,body,files_path):
    
    if from_address == None or from_address == '':
        return "from_address is mandatory!"
    
    if to == None or to == '' or to == []:
        return "to is mandatory!"
    
    if server == None or server == '':
        return "server is mandatory!"
    
    try:
        to = convert_email_list(to)
        cc = convert_email_list(cc)
        bcc = convert_email_list(bcc)

        EMAIL_LIST = to + cc + bcc
        EMAIL_LIST.append(from_address)
        # validate emails
        for email in EMAIL_LIST:
            if validate_email(email) == False:
                return f"invalide email! {email}"
        EMAIL_LIST.remove(from_address)

        FROM = from_address
        TO = ",".join(to)
        CC = ",".join(cc)
        BCC = ",".join(bcc)
        SUBJECT = subject
        BODY = body
        USER = user
        PASS = password
        SERVER = server
        MSG_TYPE = message_type
        
        # mime init
        msg = MIMEMultipart()

        msg['From'] = FROM
        msg['To'] = TO
        msg['CC'] = CC
        msg['BCC'] = BCC
        msg['Subject'] = SUBJECT
        msg.attach(MIMEText(BODY, MSG_TYPE))
    
        total_file_size = 0
        if files_path != None and files_path != []:
            try:
                for file_path in files_path:
                    with open(file_path, "rb") as fp:
                        total_file_size = total_file_size + os.path.getsize(fp.name)
                        if total_file_size <= 26214400: # 25MB
                            part = MIMEBase('application', "octet-stream")
                            part.set_payload((fp).read())
                            # Encoding payload is necessary if encoded (compressed) file has to be attached.
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition', "attachment; filename= %s" % os.path.basename(file_path))
                            msg.attach(part)
                        else:
                            body =  f"""attachements total size must be max 25MB! Current size is {total_file_size/1048576} MB and files are {files_path}. 
                            {body}"""
            except Exception as e:
                print("something went wrong!", e)    
        
        if SERVER == 'localhost':   # send mail from local server
            # Start local SMTP server
            server = smtplib.SMTP(SERVER)
        else:
            # Start SMTP server at port 587
            server = smtplib.SMTP(SERVER, 25)
            server.starttls()
            # Enter login credentials for the email you want to sent mail from
            if USER and PASS: 
                server.login(USER, PASS)
        
        text = msg.as_string()
        server.sendmail(FROM, EMAIL_LIST, text)

        server.quit()
        return "Sent"
    except Exception as e:
        return e


if __name__ == "__main__":

    send = send_email(
        user = "nagarjuna.a@fadv.com",
        password = None,
        message_type="plain",
        server="mail.fadv.com",
        from_address = "nagarjuna.a@fadv.com",
        to = "manish.mishra@fadv.com;nagarjuna.a@fadv.com",
        cc = ["karuna.anakarla@fadv.com"],
        bcc = [],
        subject = "SMTP mail test",
        body = "Hello from SMTP",
        files_path = []
    )

    print(send)

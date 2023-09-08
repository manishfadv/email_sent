from send_email import send_email


def test_mandatory_fields():
    
    response = send_email(
        user = None,
        password = "xxxxx",
        message_type="plain",
        server="localhost",
        from_address = "manish.mishra@fadv.com",
        to = "manish.mishra@fadv.com;nagarjuna.a@fadv.com",
        cc = [],
        bcc = [],
        subject = "SMTP mail test",
        body = "Hello from SMTP",
        files_path = []
    )
    assert response == "user is mandatory!"


def test_send_email():
    response = send_email(
        user = "manish.mishra@fadv.com",
        password = "xxxxx",
        message_type="plain",
        server="localhost",
        from_address = "manish.mishra@fadv.com",
        to = "manish.mishra@fadv.com;nagarjuna.a@fadv.com",
        cc = [],
        bcc = [],
        subject = "SMTP mail test",
        body = "Hello from SMTP",
        files_path = []
    )
    assert response == 'Sent'
    
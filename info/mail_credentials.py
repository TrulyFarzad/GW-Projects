# these will be used in the main.py file as the parameters of the send_mail function.
SENDER = 'sender email address'
RECIPIENT = 'receiver email address'
PASSWORD = r"sender email password"

"""
NOTE: due to google's policy regarding Less Secure App Access, this won't work with a gmail as the sender.
i used this with an Outlook email as the sender.
if you want to use another email client for the sender, you'll need to change some properties in the send_mail function
of the exporter.py file accordingly.
"""

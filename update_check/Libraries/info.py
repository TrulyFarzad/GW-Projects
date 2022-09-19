# this path will be used in the exporter.py file as the path used to read from and write to the CSV database in the
# update_csv and save_csv functions.
PATH = r''
# PATH = r'/home/farzad/work/Greenweb/GreenWeb_Project/data.csv'


# these will be used in the main.py file as the parameters of the send_mail function.
SENDER = ''
RECIPIENT = ''
SENDER_PASSWORD = r""
"""
NOTE: due to google's policy regarding Less Secure App Access, this won't work with a gmail as the sender.
i used this with an Outlook email as the sender.
if you want to use another email client for the sender, you'll need to change some properties in the send_mail function
of the exporter.py file accordingly.
"""


# used in the main.py file to connect to the MySQL database.
HOST = ''
USER = ''
MYSQL_PASSWORD = ''
PORT = ''
DATABASE = ''

"""
the purpose of this script is to receive the list of new update for Directadmin packages and the time the check
has been made and return them in CSV and Email formats.
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pandas import DataFrame
from info import csv_database
from typing import Tuple, List
import pandas as pd
import smtplib


def to_dataframe(check_update_results: List) -> DataFrame:
    # turn the result of the check_update operation into a dataframe
    result_dict =\
        {
            'package_list': check_update_results[0],
            'Time': check_update_results[1]
        }
    result = pd.DataFrame(result_dict, index=[num for num in range(len(check_update_results[0]))])
    return result


def update_csv(check_ip_results: List) -> Tuple[DataFrame, str]:
    # import the CSV database. concat it with new check_update data and return the results.
    # returns the check_update dataframe itself if there is an error in the process. for first-time runs
    # when CSV database doesn't exist.
    new_data = to_dataframe(check_ip_results)
    try:
        csv_db: DataFrame = pd.read_csv(csv_database.PATH)
        result = pd.concat([csv_db, new_data], ignore_index=True)
        return result, 'imported CSV database and updated it successfully!'
    except Exception as error:
        return new_data, f'Error in update_csv function: {error}'


def save_csv(df: DataFrame) -> str:
    try:
        df.to_csv(csv_database.PATH)
        return 'saved the updated CSV file successfully!'
    except Exception as error:
        return f'Error in save_csv function: {error}'


def send_mail(df: DataFrame, sender: str, recipient: str, password: str) -> str:
    try:
        message = MIMEMultipart()
        message['Subject'] = 'new ip check query'
        message['From'] = sender
        message['To'] = recipient

        html = MIMEText(df.to_html(index=False), 'html')
        message.attach(html)

        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, message.as_string())
            print('sent email successfully!')
        return 'sent email successfully'
    except Exception as error:
        return f'Error in send_mail function: {error}'

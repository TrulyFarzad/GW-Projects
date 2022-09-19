"""
this script's purpose is to receive the results of the spamCheck operation and save it to aCSV file.
and email it to a specified email.
"""

try:
    from info import PATH
except ModuleNotFoundError:
    from Libraries.info import PATH
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pandas import DataFrame
from typing import List
import pandas as pd
import smtplib


def to_dataframe(check_ip_results: List) -> DataFrame:
    # turn the result of the check_ip operation into a dataframe
    result_dict =\
        {
            'ip': check_ip_results[0],
            'Time': check_ip_results[3],
            'BlackListed': check_ip_results[1],
            'TimeOut': check_ip_results[2],
        }
    # result = pd.DataFrame(result_dict, index=[0])
    result = pd.DataFrame(result_dict)
    return result


# def update_csv(check_ip_results: List) -> Tuple[DataFrame, str]:
#     print('update csv')
#     # import the CSV database. concat it with new check_ip data and return the results.
#     # returns the check_ip dataframe itself if there is an error in the process. for first runs when CSV database
#     # doesn't exist.
#     new_data = to_dataframe(check_ip_results)
#     try:
#         csv_db: DataFrame = pd.read_csv(PATH)
#         result = pd.concat([csv_db, new_data], ignore_index=True)
#         print('done\n', result)
#         return result, 'imported CSV database and updated it successfully!'
#     except Exception as error:
#         print('done with error\n')
#         return new_data, f'Error in update_csv function: {error}'


def save_csv(df: DataFrame) -> str:
    print('save csv')
    try:
        df.to_csv(rf'{PATH}/{df["ip"][0]}.csv')
        print('done\n')
        return 'saved the updated CSV file successfully!'
    except Exception as error:
        print('done with error\n')
        return f'Error in save_csv function: {error}'


def send_mail(df: DataFrame, sender: str, recipient: str, password: str, subject: str) -> str:
    print('send mail')
    try:
        message = MIMEMultipart()
        message['Subject'] = subject
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

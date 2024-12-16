import pandas as pd
from sqlalchemy import create_engine
import openpyxl
from pandas import ExcelWriter
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# variables
DB_URL = 'mysql+pymysql://username:password@mysql/sales_db'
SENDER_EMAIL = "sender@abc.com"
SENDER_PASSWORD = "GgYaP9921"
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587
CREDENTIALS_FILE = 'credentials.json'

# retrieve data from database
def retrieve_data():

    # connect to the database
    engine = create_engine(DB_URL)
    
    # retrieve data from sales, product, and store tables
    sales_df = pd.read_sql('SELECT * FROM sales', engine)
    product_df = pd.read_sql('SELECT * FROM product', engine)
    store_df = pd.read_sql('SELECT * FROM store', engine)
    
    return sales_df, product_df, store_df

# merge and filter the data
def process_data(sales_df, product_df, store_df, region=None, category=None):

    # merge three dataframes
    merged_data = pd.merge(pd.merge(sales_df, product_df, on='product_code'), store_df, on='store_code')
    
    if region:
        merged_data = merged_data[merged_data['store_region'] == region]
    if category:
        merged_data = merged_data[merged_data['product_category'] == category]
        
    return merged_data

# aggregate sales data by region and category
def aggregate_sales(data, group_by):
    
    # calculate the sales amount and profit
    data['sales_amount'] = data['sales_qty'] * data['price']
    data['sales_cost'] = data['sales_qty'] * data['cost']
    data['profit'] = data['sales_amount'] - data['sales_cost']
    
    aggregated_data = data.groupby(group_by)[['sales_qty', 'sales_amount', 'sales_cost', 'profit']].sum().reset_index()
    
    return aggregated_data

# export to excel file
def export_to_excel(report_by_region, report_by_category):

    # create unique filename with timestamp appended
    file_name = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # save data to excel
    with ExcelWriter(file_name, engine='openpyxl') as writer:
        report_by_region.to_excel(writer, sheet_name='By Region', index=False)
        report_by_category.to_excel(writer, sheet_name='By Category', index=False)
    
    # adjusting column width
    wb = openpyxl.load_workbook(file_name)
    
    for sheet_name in ['By Region', 'By Category']:
        sheet = wb[sheet_name]
        sheet.column_dimensions['A'].width = 20
        
    wb.save(file_name)
    return file_name

# upload to google drive
def upload_to_drive(file_name, folder_id):
    
    # authenticate using credentials file
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/drive.file'])
    creds = flow.run_local_server(port=0)
    
    # create a Google Drive API service
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_name, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    # upload file
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    return file['id']

# send email notification
def send_email(file_link, recipient_email):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = 'Sales report ready for download'
    body = f"Hello,\n\nYour sales report is ready. You can download it from:\n{file_link}"
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        
    print(f"Email sent to {recipient_email}")

# main function
def main():
    # retrieve data
    sales_data, product_data, store_data = retrieve_data()
    
    # data processing
    processed_data = process_data(sales_data, product_data, store_data, region='South', category='Retail')
    
    # generate report
    report_by_region = aggregate_sales(processed_data, 'store_region')
    report_by_category = aggregate_sales(processed_data, 'product_category')
    
    # export to excel
    file_name = export_to_excel(report_by_region, report_by_category)
    
    # upload to google drive
    file_link = upload_to_drive(file_name, '1AbQ123826XyZ29')
    
    # send email notification
    send_email(file_link, "recipient@abc.com")

if __name__ == "__main__":
    main()
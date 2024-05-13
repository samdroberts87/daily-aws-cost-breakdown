import boto3
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Set up AWS Cost Explorer client
    cost_explorer = boto3.client('ce')

    # Calculate start and end dates for the cost report (last 24 hours)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Fetch costing information for the last 24 hours
    response = cost_explorer.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost']
    )

    # Extract and format cost information
    cost_details = extract_cost_details(response)

    # Format the information into an email message
    email_message = format_email_message(cost_details)

    # Send the email notification
    send_email_notification(email_message)

def extract_cost_details(response):
    cost_details = []
    # Parse the response to extract cost details
    for result_by_time in response['ResultsByTime']:
        for group in result_by_time['Groups']:
            keys = group['Keys']
            cost = group['Metrics']['UnblendedCost']['Amount']
            service = keys[0]  # Assuming service is the first key
            region = keys[1]  # Assuming region is the second key
            cost_details.append({'Service': service, 'Region': region, 'Cost': float(cost)})
    return cost_details

def format_email_message(cost_details):
    # Format the cost details into an email message
    email_message = "AWS Cost Details (Last 24 Hours):\n\n"
    for cost_detail in cost_details:
        service = cost_detail['Service']
        region = cost_detail['Region']
        cost = cost_detail['Cost']
        email_message += f"Service: {service}\nRegion: {region}\nCost: ${cost}\n\n"
    return email_message

def send_email_notification(email_message):
    # Email configuration
    sender_email = 'EMAIL'
    recipient_email = 'EMAIL'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'EMAIL' 
    smtp_password = 'PASSWORD'

    # Create email message
    msg = MIMEText(email_message)
    msg['Subject'] = 'AWS Cost Notification'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully.")

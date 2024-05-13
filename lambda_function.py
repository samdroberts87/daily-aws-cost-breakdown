import boto3
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Set up Boto3 Cost Explorer client
        cost_explorer = boto3.client('ce')

        # Calculate start and end dates for the cost report (last 24 hours)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        # Convert dates to string format
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Query for total costs by service
        response = cost_explorer.get_cost_and_usage(
            TimePeriod={
                'Start': start_date_str,
                'End': end_date_str
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                },
            ]
        )

        # Extract cost details
        cost_details = extract_cost_details(response)
        
        # Debugging: Print cost details
        print("Cost Details:")
        print(json.dumps(cost_details, indent=2))

        # Format the information into an email message
        email_message = format_email_message(cost_details)

        # Debugging: Print email message
        print("Email Message:")
        print(email_message)

        # Send the email notification
        send_email_notification(email_message)

        return {
            'statusCode': 200,
            'body': 'Costing information retrieved and email sent successfully.'
        }

    except Exception as e:
        logger.error(f"Error - {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }

def extract_cost_details(response):
    cost_details = []
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            service_name = group['Keys'][0]
            cost_amount = group['Metrics']['UnblendedCost']['Amount']
            cost_details.append({'Service': service_name, 'Cost': float(cost_amount)})
    return cost_details

def format_email_message(cost_details):
    email_message = "AWS Cost Details (Last 24 hrs):\n\n"
    for cost_detail in cost_details:
        service = cost_detail['Service']
        cost = cost_detail['Cost']
        email_message += f"Service: {service}\nCost: ${cost}\n\n"
    return email_message

def send_email_notification(email_message):
    sender_email = 'EMAIL'
    recipient_email = 'EMAIL'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'EMAIL'
    smtp_password = 'PASSWORD'

    msg = MIMEText(email_message)
    msg['Subject'] = 'AWS Cost Notification'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        logger.info("Email sent successfully.")

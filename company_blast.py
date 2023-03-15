import base64
import csv
import json
import os.path
import secrets_vault
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime


"""
1. Run "pip3 install -r requirements.txt" to install all requirements globally or in a virtual environment.

2. To set up your Google Cloud Platform account and enable the Gmail API, follow these steps: Go to the Google Cloud Console at https://console.cloud.google.com/ and sign in to your Google account.

3. Create a new project by clicking on the "Select a project" dropdown in the top navigation bar and selecting "New Project". Give your project a name and click "Create".

4. Once your project is created, go to the APIs & Services Dashboard by clicking on the hamburger menu in the top left corner and selecting APIs & Services > Dashboard.

5. Click on the "+ ENABLE APIS AND SERVICES" button at the top of the page.

6. Search for "Gmail" in the search bar and select the "Gmail API" from the list of results.

7. Click the "Enable" button to enable the Gmail API for your project.

8. Next, you need to create an OAuth 2.0 client ID and secret. To do this, click on "Create Credentials" on the APIs & Services Dashboard and select "OAuth client ID".

9. Fill out the forms and assign names and email addresses where necessary. Make sure you select user data.

10. Select "Desktop App" as the application type and give your client ID a name when on the "OAuth Credentials" step.

11. Click "Create" to generate your client ID and secret.

12 .Download the JSON file containing your client ID and secret by clicking the "Download" button on the right side of your client ID entry in the "OAuth 2.0 Client IDs" section of the Credentials page.

13. Move the downloaded JSON file to the same directory as your Python script and rename it to "client_secret.json". You can make a new folder as well.

14. Replace all the parameters with your specific user information, credentials, filepaths, email messages, etc. Credentials can be found in the APIs & Services Dashboard. Keep these in a separate file in the directory called "secrets_vault.py" Make sure attachment is a PDF and email addresses are valid.
"""

# 'your client-id'
CLIENT_ID = secrets_vault.CLIENT_ID
# 'your client-secret'
CLIENT_SECRET = secrets_vault.CLIENT_SECRET
REDIRECT_URI = secrets_vault.REDIRECT_URI
# 'your email address'
MY_EMAIL = 'nithanth.ram@gmail.com'
# 'Your full name'
MY_NAME = 'Nithanth Ram'
# 'filepath to csv of recruiter information'
CSV_FILEPATH = 'companyblastertest.csv'
# 'subject of email'
SUBJECT = 'Test'
# body of email - Ex. 'Dear [FIRST NAME],\n\nI am writing to express my interest in the Software Engineering position at [COMPANY NAME].\n\nPlease find attached my resume.\n\nBest regards,\n[YOUR NAME]'
BODY = 'Test123'
# 'filepath to resume/other attachment'
ATTACHMENT_FILEPATH = 'companyblasterresumetest.pdf'

def get_gmail_service():
    """Authorize and create a Gmail API service object."""
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.modify']
    
    # check if credentials already exist and are not expired
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            creds = None
    
    # refresh credentials if need be and write to a token file within script directory 
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=SCOPES, redirect_uri=REDIRECT_URI)
        auth_url, _ = flow.authorization_url(prompt='consent')
        print(f'Please visit this URL to authorize the application: {auth_url}')
        code = input('Enter the authorization code: ')
        flow.fetch_token(code=code)
        creds = flow.credentials
        creds_json = creds.to_json()

        with open(token_path, 'w') as token_file:
            token_file.write(creds_json)

    
    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message_with_attachment(to, subject, body, file_path):
    """Create an email message with an attachment."""
    # Using the Python email library, create a messasge template using the content
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    message.attach(MIMEText(body))

    # Access the PDF attachment file and add it to the message
    with open(file_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        message.attach(attachment)

    # Return the message content as a dictionary with base64 encoded raw data
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def main():
    # Start the Gmail API service 
    service = get_gmail_service()

    # Read the csv file with the list of recruiters
    with open(CSV_FILEPATH, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header row
        next(csv_reader)  
        # process the CSV
        for row in csv_reader:
            # Extract the data from the row
            company_name, name, email = row
            # Construct the "To" field for the email
            to = f'{name} <{email}>'
            # Replace the placeholders in the body of the email with actual values
            body = BODY.replace('[COMPANY NAME]', company_name).replace('[FIRST NAME]', name).replace('[YOUR NAME]', MY_NAME)
            # Create the message object with the attachment
            message = create_message_with_attachment(to, SUBJECT, body, ATTACHMENT_FILEPATH)
            try:
                # Send the message
                message = (service.users().messages().send(userId='me', body=message).execute())
                print(f'Message sent to {to}. Message Id: {message["id"]}')
            except HttpError as error:
                # Handle any errors that occur during sending
                print(f'An error occurred: {error}')
                message = None
    print('All messages sent successfully')

if __name__ == '__main__':
    main()




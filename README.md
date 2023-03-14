# Resume Blaster
Resume Blaster is a program to mass send emails attached with a resume to individuals at companies you want to reach out to. To use this prgogram, make sure you have a valid email address, a school/work resume, and a CSV file with columns "Company Name", "Recipient's Name", "Email Address" which contains all the respective contact information of the individuals you want to reach out to

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

12. Download the JSON file containing your client ID and secret by clicking the "Download" button on the right side of your client ID entry in the "OAuth 2.0 Client IDs" section of the Credentials page.

13. Move the downloaded JSON file to the same directory as your Python script and rename it to "client_secret.json". You can make a new folder as well.

14. Replace all the parameters with your specific user information, credentials, filepaths, email messages, etc. Credentials can be found in the APIs & Services Dashboard. Keep these in a separate file in the directory called "secrets_vault.py" Make sure attachment is a PDF and email addresses are valid.


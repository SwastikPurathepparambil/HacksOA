#randomimports:::
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes


#Google defined python script:

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#sendmessage/othercommanddefinitions(this one is customizable for attachments)
#from Google import Create_Service(leaving this here in case something goes wrong)

def sendmessage(listoftargets, textmessage, subject, filelist=0):
    #Enter your secret file here
    CLIENT_SECRET_FILE = '/Users/sandeep/Downloads/cli.json'
    API_NAME = 'gmail',
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
 
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    for i in listoftargets:
 
        file_attachments = filelist
 
        emailMsg = 'Hi ' + str(i[0]) + ', ' + str(textmessage)
 
        # create email message
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = str(i[1])
        mimeMessage['subject'] = subject
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))

        if filelist == 0:
            print('nofile')

        else:
            # Attach files
            for attachment in file_attachments:
                content_type, encoding = mimetypes.guess_type(attachment)
                main_type, sub_type = content_type.split('/', 1)
                file_name = os.path.basename(attachment)
 
                f = open(attachment, 'rb')
 
                myFile = MIMEBase(main_type, sub_type)
                myFile.set_payload(f.read())
                myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
                encoders.encode_base64(myFile)
 
                f.close()
 
                mimeMessage.attach(myFile)
 
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
 
        message = service.users().messages().send(
            userId='me',
            body={'raw': raw_string}).execute()
 
        print(message)



    


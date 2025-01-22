import os
from sendgrid import SendGridAPIClient # type: ignore
from datetime import datetime
from supabase import create_client, Client
from data import extrac_from_db

def make_report():
    try:
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        if SUPABASE_URL is not None and SUPABASE_KEY is not None:
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Scrapping data...")
        encoded_file = extrac_from_db(marketplace="All", supabase=supabase, isSendingByEmail=True)
        
        print("Building email...")
        sendgrid_client = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        dataEmail = {
            "from": {"email": "marcelo@kiranalabs.mx"},
            "personalizations": [
                {
                    "to": [
                        {"email": "marco.castaneda@kiranalabs.mx"},
                        {"email": "marcelo@kiranalabs.mx"},
                        {"email": "montse.villa@kiranalabs.mx"},
                    ],
                    "dynamic_template_data": {
                        "title": "Test imporey scrapper with file",
                    },
                }
            ],
            "template_id": "d-8f9fb5969dd64cc1bc52fd0a2071d89d",
            "attachments": [
                {
                    "content": encoded_file,  
                    "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "filename": f"results_{current_date}.xlsx",
                    "disposition": "attachment"
                }
            ]
        }
        print("Sending email...")
        response = sendgrid_client.client.mail.send.post(request_body=dataEmail)
        
        if 200 <= response.status_code < 300:
            print("Email send successfully")
        else:
            print("Error when send email.")
            print(f"Status: {response.status_code}, Details: {response.body.decode()}")
    except Exception as e:
        print(f"Error when making report: {str(e)}")



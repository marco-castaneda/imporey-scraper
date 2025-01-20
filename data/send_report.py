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

        encoded_file = extrac_from_db(marketplace="HomeDepot", supabase=supabase, isSendingByEmail=True)
        sendgrid_client = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        dataEmail = {
            "from": {"email": "marcelo@kiranalabs.mx"},
            "personalizations": [
                {
                    "to": [
                        {"email": "marco_pascual410@hotmail.com"},
                    ],
                    "dynamic_template_data": {
                        "title": "Test imporey scrapper with file",
                    },
                }
            ],
            "template_id": "d-c17ab97bebf04d08a6d0a5ff2f30e98b",
            "attachments": [
                {
                    "content": encoded_file,  
                    "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "filename": f"resultados_{current_date}.xlsx",
                    "disposition": "attachment"
                }
            ]
        }
        print("Sending email...")
        response = sendgrid_client.client.mail.send.post(request_body=dataEmail)
        
        if 200 <= response.status_code < 300:
            print("Correo enviado exitosamente.")
            print(f"Estado: {response.status_code}, Detalles: {response.body.decode()}")
        else:
            print("Error al enviar el correo.")
            print(f"Estado: {response.status_code}, Detalles: {response.body.decode()}")
    
    except Exception as e:
        print("Ocurrió un error al intentar enviar el correo:")
        print(str(e))


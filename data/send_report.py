import os
from sendgrid import SendGridAPIClient # type: ignore
from datetime import datetime

from data import extrac_from_db

def make_report(supabase):
    try:
        
        encoded_file = extrac_from_db(marketplace="HomeDepot", supabase=supabase, isSendingByEmail=True)
        sendgrid_client = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        dataEmail = {
            "from": {"email": "rodrigo@kiranalabs.mx"},
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
            "template_id": "d-a748551b6cb24b70b4b76cd0bcbed86b",
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


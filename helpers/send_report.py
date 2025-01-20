import os
from sendgrid import SendGridAPIClient # type: ignore


def make_report():
    try:
        sendgrid_client = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        
        data = {
            "from": {"email": "marcelo@kiranalabs.mx"},
            "personalizations": [
                {
                    "to": [
                        {"email": "marco_pascual410@hotmail.com"},
                    ],
                    "dynamic_template_data": {
                        "title": "Se creó una nueva solicitud de facturación marketplace por parte de cliente.",
                    },
                }
            ],
            "template_id": "d-c17ab97bebf04d08a6d0a5ff2f30e98b",
        }
        
        response = sendgrid_client.client.mail.send.post(request_body=data)
        
        if 200 <= response.status_code < 300:
            print("Correo enviado exitosamente.")
            print(f"Estado: {response.status_code}, Detalles: {response.body.decode()}")
        else:
            print("Error al enviar el correo.")
            print(f"Estado: {response.status_code}, Detalles: {response.body.decode()}")
    
    except Exception as e:
        print("Ocurrió un error al intentar enviar el correo:")
        print(str(e))


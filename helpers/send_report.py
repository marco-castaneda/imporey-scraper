import os
from sendgrid import SendGridAPIClient # type: ignore


def make_report():
    try:
        sendgrid_client = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        data = {
            "from": {"email": "marco.castaneda@kiranalabs.mx"},
            "personalizations": [
                {
                    "to": [
                        {"email": "marco_pascual410@hotmail.com"},
                    ],
                    "dynamic_template_data": {
                        "title": "Se creo una nueva solicitud de facturación marketplace por parte de cliente.",
                    },
                }
            ],
            "template_id": "d-c17ab97bebf04d08a6d0a5ff2f30e98b",
        }

        response = sendgrid_client.client.mail.send.post(request_body=data)

        print("Report finished")
        print("response")
        print(response)
    except Exception as e:
        print("An error")
        print(e)

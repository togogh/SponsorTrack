from sponsortrack.backend.core.config import settings
import resend

resend.api_key = settings.RESEND_API_KEY

params: resend.Emails.SendParams = {
    "from": f"Acme <onboarding@{settings.EMAIL_DOMAIN}>",
    "to": [f"no-reply@{settings.EMAIL_DOMAIN}"],
    "subject": "hello world",
    "html": "<strong>it works!</strong>",
}

email = resend.Emails.send(params)
print(email)

from typing import List, Optional

from django.core.mail import EmailMultiAlternatives
from django.http import QueryDict
from django.template import loader


def send_mail(recipients: List[str], subject: str, body: str, cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None):
    email_message = EmailMultiAlternatives(subject, body, None, recipients, cc=cc, bcc=bcc)
    email_message.attach_alternative(body, "text/html")
    email_message.send()


def send_mail_template(recipients: List[str], subject: str, body_template: str, context, cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None):
    body = loader.render_to_string(body_template, context)
    send_mail(recipients, subject, body, cc, bcc)


def get_mailto_url(recipients: List[str], subject: str, body: str, cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None) -> str:
    query = QueryDict(mutable=True)
    query["subject"] = subject
    query["body"] = body
    if cc is not None:
        query.setlist("cc", cc)
    if bcc is not None:
        query.setlist("bcc", bcc)
    return f"mailto:{','.join(recipients)}?{query.urlencode()}"


def get_mailto_url_template(recipients: List[str], subject: str, body_template: str, context, cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None) -> str:
    body = loader.render_to_string(body_template, context)
    return get_mailto_url(recipients, subject, body, cc, bcc)

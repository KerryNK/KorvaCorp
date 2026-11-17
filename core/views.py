import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactSubmissionForm

logger = logging.getLogger(__name__)


def home(request):
    if request.method == "POST":
        form = ContactSubmissionForm(request.POST)
        if form.is_valid():
            # Quietly accept honeypot submissions without storing them.
            if not form.cleaned_data.get("website"):
                submission = form.save()
                message_body = "\n".join(
                    [
                        f"Name: {submission.full_name}",
                        f"Organization: {submission.organization or 'Not provided'}",
                        f"Email: {submission.email}",
                        f"Inquiry type: {submission.get_inquiry_type_display()}",
                        "",
                        "Message:",
                        submission.message,
                    ]
                )
                try:
                    sent_count = send_mail(
                        subject=f"Korva Global inquiry: {submission.get_inquiry_type_display()}",
                        message=message_body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                        fail_silently=False,
                        reply_to=[submission.email],
                    )
                    if sent_count != 1:
                        raise RuntimeError("Inquiry email backend did not confirm delivery.")
                except Exception:
                    logger.exception("Unable to email contact inquiry %s", submission.pk)
                    messages.error(
                        request,
                        "Your inquiry was saved, but we couldn't email it right now. Please contact kkcorp524@gmail.com.",
                    )
                else:
                    messages.success(request, "Thank you. Your inquiry has been received.")
            else:
                messages.success(request, "Thank you. Your inquiry has been received.")
            return redirect(f"{reverse('home')}#contact")
    else:
        form = ContactSubmissionForm()

    return render(request, "index.html", {"contact_form": form})


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def terms_of_use(request):
    return render(request, "core/terms_of_use.html")


def page_not_found(request, exception):
    return render(request, "core/404.html", status=404)


def server_error(request):
    return render(request, "core/500.html", status=500)

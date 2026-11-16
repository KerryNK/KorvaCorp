from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactSubmissionForm


def home(request):
    if request.method == "POST":
        form = ContactSubmissionForm(request.POST)
        if form.is_valid():
            # Quietly accept honeypot submissions without storing them.
            if not form.cleaned_data.get("website"):
                form.save()
            messages.success(request, "Thank you. Your inquiry has been received.")
            return redirect(f"{reverse('home')}#contact")
    else:
        form = ContactSubmissionForm()

    return render(request, "index.html", {"contact_form": form})


def page_not_found(request, exception):
    return render(request, "core/404.html", status=404)


def server_error(request):
    return render(request, "core/500.html", status=500)

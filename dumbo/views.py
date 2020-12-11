from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages


def landing_page(request):
    return render(request, 'landingpage.html', {})


def about(request):
    return render(request, 'aboutpage.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            print(name, email, subject, message)
            send_mail (
                subject,# subject
                f'Hi founder \nYou got a message from {name} \nThe message is \n{message} \ncontact info: {email}',# message
                'noreply.farmx@gmail.com', # from email
                ['o.taruntejaa@gmail.com', 'lokesh.7.8.kl@gmail.com', 'srichu.kattamuru@gmail.com',
                 'jayachand2001@gmail.com'],
            )
            messages.success(request, f'thanks for contacting {name}.\nWe wil get back to you soon.')
            return redirect('contact_page')
    context = {
        'form': ContactForm()
    }
    return render(request, 'contactpage.html', context)

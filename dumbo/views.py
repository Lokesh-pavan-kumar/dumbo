from django.shortcuts import render, redirect


def landing_page(request):
    return render(request, 'landingpage.html', {})


def about(request):
    # This view should take care of the about page
    pass


def contact(request):
    # This view should take care of the contact page
    pass

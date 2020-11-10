from django.shortcuts import redirect, render


def redirect_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('my_documents')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

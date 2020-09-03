from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def permission_error(request, *args, **kwargs):
    return render(request, 'error_pages/403.html')


@requires_csrf_token
def page_not_found(request, *args, **kwargs):
    return render(request, 'error_pages/404.html')


@requires_csrf_token
def server_error(request,*args, **kwargs):
    return render(request, 'error_pages/500.html')

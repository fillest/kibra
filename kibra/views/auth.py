from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget


def login (request):
    referrer = request.url
    if referrer == request.route_url('login'):
        referrer = request.route_url('entries.list')
    redirect_url = request.POST.get('redirect_url', referrer)
    
    if request.method.lower() == 'post':
        username = request.POST['username']

        real_password = request.registry.settings['users'].get(username)
        if request.POST['password'] == real_password:
            return HTTPFound(location = redirect_url, headers = remember(request, username))
        else:
            auth_failed = True
    else:
        auth_failed = False

        username = ''

    return {
        'auth_failed': auth_failed,
        'redirect_url': redirect_url,
        'username': username,
    }


def logout (request):
    return HTTPFound(location = request.route_url('entries.list'), headers = forget(request))

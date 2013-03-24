import logging
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .db import init
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .auth import group_finder, ACL
from .resources import RootFactory
from pyramid.security import authenticated_userid
from pyramid.settings import asbool
from kibra import weberror_formatter_patch


def _setup_views(config):
    config.add_static_view('static', 'kibra:static')

#    config.add_view(lambda context, _request: context, context='pyramid.exceptions.NotFound')

    config.add_route('entries.list', '/')
    config.add_view('kibra.views.entries.show_list',
                    route_name='entries.list',
                    renderer='list.mako',
                    permission='edit')

    config.add_route('login', '/login')
    config.add_view('kibra.views.auth.login', route_name='login',
                    renderer='login.mako')

    config.add_view('kibra.views.auth.login',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer='login.mako')

    config.add_route('logout', '/logout')
    config.add_view('kibra.views.auth.logout', route_name='logout',
                    permission='edit')

    config.add_route('entries.edit', '/edit')
    config.add_view('kibra.views.entries.edit',
                    route_name='entries.edit',
                    renderer='edit.mako',
                    permission='edit')

    config.add_route('entries.delete', '/delete/{id}')
    config.add_view('kibra.views.entries.delete', route_name='entries.delete',
                    permission='edit')

    config.add_route('entries.rename_tag', '/rename_tag')
    config.add_view('kibra.views.entries.rename_tag', route_name='entries.rename_tag',
                    permission='edit', renderer='string')


def _add_renderer_globals(event):
    event['authenticated_userid'] = authenticated_userid


def main(global_config, **settings):
    if asbool(settings.get('enable_weberror_formatter_hack')):
        weberror_formatter_patch.patch_lib()

    engine = engine_from_config(settings, 'sqlalchemy.')
    init(engine)


    settings['users'] = {'admin': settings['auth.admin_password']}


    config = Configurator(
        settings = settings,
        root_factory = 'kibra.resources.RootFactory',
        authentication_policy = AuthTktAuthenticationPolicy(settings['auth.secret'], callback=group_finder),
        authorization_policy = ACLAuthorizationPolicy(),
    )


    config.add_subscriber(_add_renderer_globals, 'pyramid.events.BeforeRender')


    _setup_views(config)


    return config.make_wsgi_app()

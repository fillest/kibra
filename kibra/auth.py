from pyramid.security import Allow, Everyone, ALL_PERMISSIONS


GROUPS = {'admin': ['group:admins']}
ACL = [
    (Allow, 'group:admins', ALL_PERMISSIONS)
]


def group_finder(userid, request):
    if userid in request.registry.settings['users']:
        return GROUPS.get(userid, [])

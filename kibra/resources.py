from auth import ACL

class RootFactory(object):
    __acl__ = ACL
    
    def __init__(self, request):
        pass

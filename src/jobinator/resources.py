from horus.resources import BaseFactory
from jobinator.models import UserFilter
from pyramid.security import Authenticated, Allow, ALL_PERMISSIONS


class RootFactory(BaseFactory):
    """ Root factory """

    @property
    def __acl__(self):
        defaultlist = [
            (Allow, 'group:admin', ALL_PERMISSIONS),
            (Allow, Authenticated, 'filter_add'),
            (Allow, Authenticated, 'filter_edit'),
            (Allow, Authenticated, 'filter_list'),
        ]

        return defaultlist

    def __init__(self, request):
        super(RootFactory, self).__init__(request)
        self.is_root = True


class UserFilterFactory(RootFactory):
    """ UserFilter factory """

    def __getitem__(self, key):
        filter = UserFilter.get_all(self.request).filter(UserFilter.user == self.request.user).filter(UserFilter.pk == key).first()

        if filter:
            filter.__parent__ = self
            filter.__name__ = key

            return filter
        raise KeyError(key)

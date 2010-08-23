from Products.Five import BrowserView


class RemoveFavourite(BrowserView):
    """Removes an favorite"""

    def __call__(self, *args, **kwargs):

        uid = self.request.get('uid', None)
        if uid is None:
            raise
        uid = uid.replace('uid_', '')
        obj = self.context.reference_catalog.lookupObject(uid)
        favFolder = self.get_fav_folder()

        favFolder.manage_delObjects([obj.id, ])

        return 'OK'

    def get_fav_folder(self):
        """returns the favorite folder in a userhome"""
        homeFolder = self.context.portal_membership.getHomeFolder()
        if not homeFolder:
            return None
        return getattr(homeFolder, 'Favorites', None)

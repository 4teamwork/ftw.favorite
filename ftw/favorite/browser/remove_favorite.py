from Products.Five import BrowserView


class RemoveFavourite(BrowserView):
    """Removes an favorite"""

    def __call__(self, *args, **kwargs):

        favid = self.request.get('favid', '')
        if not favid:
            raise Exception('"id" not found in request')
        favFolder = self.get_fav_folder()
        favFolder.manage_delObjects([favid, ])

        return 'OK'

    def get_fav_folder(self):
        """returns the favorite folder in a userhome"""
        homeFolder = self.context.portal_membership.getHomeFolder()
        if not homeFolder:
            return None
        return getattr(homeFolder, 'Favorites', None)

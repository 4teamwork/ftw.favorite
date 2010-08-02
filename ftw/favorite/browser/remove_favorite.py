from Products.Five import BrowserView


class RemoveFavourite(BrowserView):
    """Removes an favorite"""

    def __call__(self, *args, **kwargs):

        id = self.request.get('id')
        favFolder = self.get_fav_folder()

        favFolder.manage_delObjects([id, ])

        return 'OK'

    def get_fav_folder(self):
        """returns the favorite folder in a userhome"""
        homeFolder = self.context.portal_membership.getHomeFolder()
        if not homeFolder:
            return None
        return getattr(homeFolder, 'Favorites', None)

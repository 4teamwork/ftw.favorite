from Products.Five import BrowserView


class RemoveFavourite(BrowserView):
    """Removes an favorite"""

    def __call__(self, *args, **kwargs):

        favuid = self.request.get('uid', '').replace('uid_', '')
        if favuid is None:
            raise Exception('"id" not found in request')
        favFolder = self.get_fav_folder()
        favid = self.context.reference_catalog.lookupObject(favuid).id
        favFolder.manage_delObjects([favid, ])

        return 'OK'

    def get_fav_folder(self):
        """returns the favorite folder in a userhome"""
        homeFolder = self.context.portal_membership.getHomeFolder()
        if not homeFolder:
            return None
        return getattr(homeFolder, 'Favorites', None)

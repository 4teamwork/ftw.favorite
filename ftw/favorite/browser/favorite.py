from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class FavoritesView(BrowserView):
    """Favorits folder default view"""

    template = ViewPageTemplateFile('templates/favorite.pt')

    def __call__(self):
        return self.template()

    def favorites(self):
        """return a list of favorites"""

        # get home folder
        mtool = getToolByName(self.context, 'portal_membership')
        homefolder = mtool.getAuthenticatedMember().getHomeFolder()
        if not homefolder:
            return []

        #check if Favorite folder exists
        if 'Favorites' not in [item.id for item in
            homefolder.getFolderContents()]:
            return []
        return homefolder.Favorites.getFolderContents(full_objects=True)

from Products.Five.browser import BrowserView
from ftw.favorite import favoriteMessageFactory as _
from Products.CMFPlone.utils import base_hasattr


class AddToFavorites(BrowserView):
    """creates a favorite object in the $UserHome/Favorite folder"""
     
    def __call__(self):
        """
        """
        context = self.context
        response = context.REQUEST.response
        homeFolder=context.portal_membership.getHomeFolder()
        state = context.restrictedTraverse("@@plone_context_state")
        view_url = '%s/%s' % (context.absolute_url(), state.view_template_id())
        if not homeFolder:
            context.plone_utils.addPortalMessage(_(u'Can\'t access home folder. Favorite is not added.'), 'error')
            return response.redirect(view_url)

        if not base_hasattr(homeFolder, 'Favorites'):
            homeFolder.invokeFactory('Folder', id='Favorites', title='Favorites')
            addable_types = ['Link']
            favs = homeFolder.Favorites
            if base_hasattr(favs, 'setConstrainTypesMode'):
                favs.setConstrainTypesMode(1)
                favs.setImmediatelyAddableTypes(addable_types)
                favs.setLocallyAllowedTypes(addable_types)
                favs.manage_addProperty('layout','favorites_view',type='string')

        targetFolder = homeFolder.Favorites
        new_id='fav_' + str(int( context.ZopeTime()))
        myPath=context.portal_url.getRelativeUrl(context)
        fav_id = targetFolder.invokeFactory('Link', id=new_id, title=context.TitleOrId(), remote_url=myPath)
        if fav_id:
            favorite = getattr(targetFolder, fav_id, None)
        else:
            favorite = getattr(targetFolder, new_id, None)

        if favorite:
            favorite.reindexObject()

            msg = _(u'${title} has been added to your Favorites.',
                    mapping={u'title' : context.title_or_id().decode('utf-8') or None})
            context.plone_utils.addPortalMessage(msg)
        else:
            msg = _(u'There was a problem adding ${title} to your Favorites.',
                    mapping={u'title' : context.title_or_id().decode('utf-8')})

        return response.redirect(view_url)
    



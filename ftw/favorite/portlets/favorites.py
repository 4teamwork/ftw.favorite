from ftw.favorite import favoriteMessageFactory as _
from plone.app.portlets.browser.formhelper import AddForm, EditForm
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements


class IFavoritePortlet(IPortletDataProvider):
    count = schema.Int(title=_(u"Number of items to display"),
                       description=_(u"How many items to list."),
                       required=True,
                       default=5)


class Assignment(base.Assignment):
    implements(IFavoritePortlet)

    def __init__(self, count=5):
        self.count = count

    @property
    def title(self):
        return _(u"Favorites", default="Favorites")


def _render_cachekey(fun, self):
    return render_cachekey(fun, self)


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/favorites.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def items(self):
        return self._data()

        def favObjects(self):
            return self.getObject()

    #XXX: @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def _data(self):
        homeFolder=self.context.portal_membership.getHomeFolder()
        if homeFolder is None:
            return []

        count = getattr(self.data, 'count', 10)
        favFolder = self.get_fav_folder()
        if favFolder:
            return favFolder.getFolderContents()[:count]

        return []

    def get_fav_folder(self):
        """ Returns the the favorite folder"""

        homeFolder = self.context.portal_membership.getHomeFolder()
        if not homeFolder:
            return None
        return getattr(homeFolder, 'Favorites', None)


class AddForm(AddForm):
    form_fields = form.Fields(IFavoritePortlet)
    label = _(u"Add Favorite Portlet")
    description = _(u"This portlet displays your Favorites")

    def create(self, data):
        return Assignment(count=data.get('count', 5))


class EditForm(EditForm):
    form_fields = form.Fields(IFavoritePortlet)
    label = _(u"Edit Favorite Portlet")
    description = _(u"This portlet displays your Favorites")

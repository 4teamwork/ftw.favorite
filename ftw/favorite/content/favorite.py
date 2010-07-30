from zope.interface import implements

from ftw.favorite.interfaces import IFavorite
from ftw.favorite.config import PROJECTNAME
from ftw.favorite import favoriteMessageFactory as _

import urlparse

from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from ZODB.POSException import ConflictError

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent

from Products.Archetypes import atapi

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema


FavoriteSchema = ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField('remoteUrl',
                required=True,
                searchable=True,
                accessor='getRemoteUrl',
                primary=True,
                validators = (),
                widget = atapi.StringWidget(
                        description=_(u'help_url', default=u'Add http:// to link outside the site.'),
                        label = _(u'label_url', default=u'URL')
                        )),
    ))

class Favorite(ATCTContent):
    """A placeholder item linking to a favorite object in the site.
    90% are copied from Products.ATContentTypes-1.3.4 favorite module

    """
    implements(IFavorite)
    schema = FavoriteSchema
    security = ClassSecurityInfo()

    security.declareProtected(ModifyPortalContent, 'setRemoteUrl')
    def setRemoteUrl(self, remote_url):
        """Set url relative to portal root
        """
        utool  = getToolByName(self, 'portal_url')
        # strip off scheme and machine from URL if present
        tokens = urlparse.urlparse(remote_url, 'http')
        if tokens[1]:
            # There is a nethost, remove it
            t=('', '') + tokens[2:]
            remote_url = urlparse.urlunparse(t)
        # if URL begins with site URL, remove site URL
        portal_url = utool.getPortalPath()
        i = remote_url.find(portal_url)
        if i==0:
            remote_url=remote_url[len(portal_url):]
        # if site is still absolute, make it relative
        if remote_url[:1]=='/':
            remote_url=remote_url[1:]

        self.getField('remoteUrl').set(self, remote_url)

    security.declareProtected(View, 'getIcon')
    def getIcon(self, relative_to_portal=0):
        """Instead of a static icon, like for Link objects, we want
        to display an icon based on what the Favorite links to.
        """
        obj =  self.getObject()
        if obj is not None:
            return obj.getIcon(relative_to_portal)
        else:
            return 'favorite_broken_icon.gif'

    security.declareProtected(View, 'getObject')
    def getObject(self):
        """Return the actual object that the Favorite is
        linking to
        """
        utool  = getToolByName(self, 'portal_url')
        portal = utool.getPortalObject()
        relative_url = self.getRemoteUrl()
        try:
            obj = portal.restrictedTraverse(relative_url)
        except ConflictError:
            raise
        except (KeyError, AttributeError, Unauthorized, 'Unauthorized', ):
            obj = None
        return obj


atapi.registerType(Favorite, PROJECTNAME)

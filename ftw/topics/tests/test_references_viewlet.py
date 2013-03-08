from ftw.topics.interfaces import ITopicBrowserLayer
from ftw.topics.testing import SIMPLELAYOUT_TOPICS_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.Five.browser import BrowserView
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager


class TestReferencesViewlet(TestCase):

    layer = SIMPLELAYOUT_TOPICS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def _get_viewlet(self, context):
        alsoProvides(context.REQUEST, ITopicBrowserLayer)

        view = BrowserView(context, context.REQUEST)
        manager_name = 'plone.belowcontent'
        manager = queryMultiAdapter(
            (context, context.REQUEST, view),
            IViewletManager,
            manager_name)
        self.failUnless(manager)

        # Set up viewlets
        manager.update()
        name = 'ftw.topics.references'
        return [v for v in manager.viewlets if v.__name__ == name]

    def test_registered(self):
        # Only Registered for ITopicSupport
        self.assertFalse(self._get_viewlet(self.portal))

        page = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'page'))
        self.assertTrue(self._get_viewlet(page))

    def test_references(self):
        tree = self.portal.get(
            self.portal.invokeFactory('ftw.topics.TopicTree', 'tree'))

        topic1 = tree.get(
            tree.invokeFactory('ftw.topics.Topic', 'topic1',
                               title="A topic"))
        topic2 = tree.get(
            tree.invokeFactory('ftw.topics.Topic', 'topic2',
                               title="B topic"))

        page = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'page'))
        viewlet = self._get_viewlet(page)[0]
        # No references
        self.assertFalse(viewlet.available())

        page.Schema()['topics'].set(page, (topic2.UID(), topic1.UID()))

        viewlet = self._get_viewlet(page)
        result = [
            dict(title='A topic',
                 description='',
                 url=topic1.absolute_url()),
            dict(title='B topic',
                 description='',
                 url=topic2.absolute_url()), ]
        self.assertEquals(viewlet[0].get_references(), result)

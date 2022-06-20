from ftw.testbrowser import browsing
from ftw.topics.testing import EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest import TestCase


class TestViewlet(TestCase):

    layer = EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.tree = self.portal.get('topics')

    @browsing
    def test_viewlet_shows_topics(self, browser):
        document = self.portal.get('manufacturing-processes')
        browser.login().visit(document)

        # first link is the topci and the seconds link is the paren object
        self.assertEqual(
            [
                'Manufacturing', 'Topics',
                'Technology', 'Topics'
            ],
            browser.css('#viewlet-below-content-body .topics ul a').text
        )

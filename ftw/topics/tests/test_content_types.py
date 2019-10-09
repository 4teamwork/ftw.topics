from ftw.testbrowser import browsing
from ftw.topics.interfaces import ITopic
from ftw.topics.interfaces import ITopicTree
from ftw.topics.testing import TOPICS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from unittest2 import TestCase
import transaction


class TestContentTypeCreation(TestCase):

    layer = TOPICS_FUNCTIONAL_TESTING

    @browsing
    def setUp(self, browser):
        self.portal = self.layer['portal']

        # setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.grant('Manager')
        browser.login(self.portal, TEST_USER_NAME)
        transaction.commit()

        #self.browser = Browser(self.layer['app'])
        #self.browser.addHeader('Authorization', 'Basic %s:%s' % (
        #        TEST_USER_NAME, TEST_USER_PASSWORD,))
        #self.browser.handleErrors = False

    @browsing
    def test_create_topic_tree(self, browser):
        browser.open(self.portal.portal_url())
        browser.getLink(id='ftw-topics-topictree').click()

        self.assertTrue(
            browser.url.endswith('++add++ftw.topics.TopicTree'),
            'Should be on the topic tree add view, but url is: %s' % (
                browser.url))

        browser.getControl(label='Title').value = 'Topical'
        browser.getControl(label='Save').click()

        self.assertTrue(
            browser.url.endswith('topical/view'),
            'Should be on "topical" view, but url is: %s' % (
                browser.url))
        self.assertIn('Topical', browser.contents)

        tree = self.portal.get('topical')
        self.assertTrue(ITopicTree.providedBy(tree))

    @browsing
    def test_create_topic(self, browser):
        # first create a tree
        browser.open('http://nohost/plone/++add++ftw.topics.TopicTree')
        browser.getControl(label='Title').value = 'Topical'
        browser.getControl(label='Save').click()

        self.assertEqual(browser.url,
                         'http://nohost/plone/topical/view')

        factory_link = browser.getLink(id='ftw-topics-topic')
        self.assertTrue(
            factory_link,
            'There is no "Topic" factory link on the topic tree view.')
        factory_link.click()

        self.assertEqual(
            browser.url,
            'http://nohost/plone/topical/++add++ftw.topics.Topic')
        browser.getControl(label='Title').value = 'Manufacturing'
        browser.getControl(label='Save').click()

        self.assertEqual(browser.url,
                         'http://nohost/plone/topical/manufacturing/view')
        self.assertIn('Manufacturing', browser.contents)

        topic = self.portal.get('topical').get('manufacturing')
        self.assertTrue(ITopic.providedBy(topic))

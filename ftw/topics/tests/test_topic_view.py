from Products.CMFCore.utils import getToolByName
from ftw.topics.testing import EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
from ftw.topics.testing import EXAMPLE_CONTENT_SIMPLELAYOUT_FUNCTIONAL
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from plone.uuid.interfaces import IUUID
from pyquery import PyQuery
from unittest2 import TestCase
import transaction


def links_to_text(pq_resultset):
    return map(lambda node: node.text.strip(), pq_resultset)


class TestDefaultTopicView(TestCase):

    layer = EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
    viewname = 'topic_view'

    def setUp(self):
        self.portal = self.layer['portal']
        self.subsite = self.portal.get('foo').get('subsite')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.tree = self.portal.get('topics')
        self.node = self.tree.get('manufacturing')
        self.subnode = self.node.get('agile-manufacturing')

        self.subsite_tree = self.subsite.get('topics')
        self.subsite_node = self.subsite_tree.get('manufacturing')

        self.browser = Browser(self.layer['app'])
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.handleErrors = False

    def test_default_topic_view(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        fti = portal_types.get('ftw.topics.Topic')
        self.assertEqual(
            fti.default_view, self.viewname,
            'Expected default view to be %s on "ftw.topics.Topic"'
            ' since only the default GS profile was installed' % (
                self.viewname))

    def test_subnode_listed(self):
        self.browser.open(self.node.absolute_url() + '/' + self.viewname)
        doc = PyQuery(self.browser.contents)

        # there should be a heading "Topics"
        self.assertEqual(doc('h3').text(), 'Topics')

        # on node (Manufacturing) should be subnode (Agile Manufacturing)
        links = doc('.subelements-listing a')
        self.assertEqual(len(links), 1,
                         'Found more or less links than expected')

        self.assertEqual(links.text(), 'Agile Manufacturing')

    def test_subnode_has_no_children(self):
        self.browser.open(self.subnode.absolute_url() + '/' + self.viewname)
        doc = PyQuery(self.browser.contents)

        self.assertEqual(len(doc('h3')), 0, 'No <h3> expected')

    def test_default_section_filter_selection(self):
        self.browser.open(self.node.absolute_url() + '/' + self.viewname)
        doc = PyQuery(self.browser.contents)

        self.assertEquals(doc('.topic-filter li b').text().strip(),
                          'Plone site',
                          'Expected section "Plone site" to be ' + \
                              'selected by default.')

        filter_links = links_to_text(doc('.topic-filter li a'))
        self.assertIn('Sub Site', filter_links,
                      'Missing awailable section filter "Sub Site"')

        reference_links = links_to_text(doc('.topic-reference-listings a'))
        self.assertIn(
            'Manufacturing processes', reference_links,
            'Link "Manufacturing processes" should be shown')

        self.assertNotIn(
            'Theories', reference_links,
            'Link "Theories" should not be shown, it is in'
            ' the section "Sub Site", not "Plone site"')

    def test_other_section_filter(self):
        self.browser.open(self.node.absolute_url() + '/' + self.viewname)
        self.browser.getLink('Sub Site').click()
        doc = PyQuery(self.browser.contents)

        self.assertEquals(doc('.topic-filter li b').text().strip(),
                          'Sub Site',
                          'Expected section "Sub Site" to be ' + \
                              'selected by default.')

        filter_links = links_to_text(doc('.topic-filter li a'))
        self.assertIn('Plone site', filter_links,
                      'Missing awailable section filter "Plone site"')

        reference_links = links_to_text(doc('.topic-reference-listings a'))
        self.assertNotIn(
            'Manufacturing processes', reference_links,
            'Link "Manufacturing processes" should not be shown, it is in'
            ' the section "Sub Site", not "Plone site"')

        self.assertIn(
            'Theories', reference_links,
            'Link "Theories" should be shown')

    def test_SUBSITE_default_section_filter_selection(self):
        self.browser.open(self.subsite_node.absolute_url() + '/' +
                          self.viewname)
        doc = PyQuery(self.browser.contents)

        self.assertEquals(doc('.topic-filter li b').text().strip(),
                          'Sub Site',
                          'Expected section "Sub Site" to be ' + \
                              'selected by default.')

        filter_links = links_to_text(doc('.topic-filter li a'))
        self.assertIn('Plone site', filter_links,
                      'Missing awailable section filter "Plone site"')

        reference_links = links_to_text(doc('.topic-reference-listings a'))
        self.assertNotIn(
            'Manufacturing processes', reference_links,
            'Link "Manufacturing processes" should not be shown, it is in'
            ' the section "Sub Site", not "Plone site"')

        self.assertIn(
            'Theories', reference_links,
            'Link "Theories" should be shown')


class TestSimplelayoutTopicView(TestDefaultTopicView):

    layer = EXAMPLE_CONTENT_SIMPLELAYOUT_FUNCTIONAL
    viewname = 'simplelayout'

    def setUp(self):
        super(TestSimplelayoutTopicView, self).setUp()

        self.page = self.portal.get(self.portal.invokeFactory(
            'ContentPage', 'page', title="Page 1"))

        self.folder = self.portal.get(
            self.portal.invokeFactory('Folder', 'folder', title="Folder"))
        transaction.commit()

    def test_representation_contentpage(self):
        self.page.Schema()['topics'].set(self.page, IUUID(self.subnode))
        self.page.reindexObject()
        transaction.commit()

        self.browser.open(self.subnode.absolute_url())
        doc = PyQuery(self.browser.contents)

        self.assertEquals(
            len(doc('.referenceRepresentationListing ul li a')), 1,
            'Found more or less links than expected')

        self.assertEquals(
            len(doc('.referenceRepresentationTitle')), 1,
            'Found more or less links than expected')

    def test_representation_default(self):
        self.folder.Schema()['topics'].set(self.folder, IUUID(self.subnode))
        self.folder.reindexObject()
        transaction.commit()

        self.browser.open(self.subnode.absolute_url())
        doc = PyQuery(self.browser.contents)

        self.assertEquals(
            len(doc('.referenceRepresentationListing ul li a')), 1,
            'Found more or less links than expected')

        self.assertEquals(
            len(doc('.referenceRepresentationTitle')), 1,
            'Found more or less links than expected')

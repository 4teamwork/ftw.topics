from ftw.testbrowser import browsing
from ftw.topics.tests import FunctionalTesting


class TestViewlet(FunctionalTesting):

    def setUp(self):
        super().setUp()
        self.grant('Manager')
        self.createContent()

    @browsing
    def test_viewlet_shows_topics(self, browser):
        browser.login().visit(self.document)

        # first link is the topci and the seconds link is the paren object
        self.assertEqual(
            [
                'Manufacturing', 'Topics',
                'Technology', 'Topics'
            ],
            browser.css('#viewlet-below-content-body .topics ul a').text
        )

from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.topics.behavior import ITopicSupportSchema


class TopicViewlet(ViewletBase):
    index = ViewPageTemplateFile("templates/viewlet.pt")

    def update(self):
        super(TopicViewlet, self).update()
        self.topics = self.get_topics()

    def get_topics(self):
        topic_support = ITopicSupportSchema(self.context, None)
        if topic_support is None:
            return []

        topic_relations = topic_support.topics

        if not topic_relations:
            return []

        topics = []
        for relation in topic_relations:
            obj = relation.to_object
            if not obj:
                continue

            topics.append(
                {
                    'title': obj.Title(),
                    'url': obj.absolute_url(),
                    'description': obj.Description(),
                    'parent_title': obj.aq_parent.Title(),
                    'parent_url': obj.aq_parent.absolute_url(),
                }
            )
        return topics

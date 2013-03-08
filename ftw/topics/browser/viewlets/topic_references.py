from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.interfaces import IBaseObject


class TopicReferences(ViewletBase):
    """Shows all topic references"""

    render = ViewPageTemplateFile('topic_references.pt')

    def get_references(self):
        result = []
        refs = sorted(self.context.Schema()['topics'].get(self.context),
                      key=lambda item: item.title_or_id())
        for obj in refs:
            result.append(dict(title=obj.title_or_id(),
                               description=obj.Description(),
                               url=obj.absolute_url(), ))
        return result

    def available(self):
        # XXX Only Archtypes support, implement DX support
        if not IBaseObject.providedBy(self.context):
            return False
        return bool(self.get_references())
from Products.Archetypes.interfaces.referenceable import IReferenceable
from Products.CMFCore.utils import getToolByName
from copy import deepcopy
from ftw.topics.interfaces import IBackReferenceCollector
from ftw.topics.interfaces import ITopic
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize import instance
from zope.component import adapts
from zope.component.hooks import getSite
from zope.interface import Interface
from zope.interface import implements


class DefaultCollector(object):
    implements(IBackReferenceCollector)
    adapts(ITopic, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.group_by = INavigationRoot

    def __call__(self, group_by=INavigationRoot):
        self.group_by = group_by
        return self._get_brefs_per_section()

    @instance.memoize
    def _get_sections(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        site = getSite()

        result = [{'label': site.Title(),
                   'path': '/'.join(site.getPhysicalPath()),
                   'UID': 'root'}]

        def brain_to_item(brain):
            return {'label': brain.Title,
                    'path': brain.getPath(),
                    'UID': brain.UID}

        brains = catalog(object_provides=self.group_by.__identifier__)
        result.extend(map(brain_to_item, brains))
        return result

    def _get_brefs_per_section(self):
        """Returns all back references per section.
        """

        section_paths = sorted(
            map(lambda sec: sec['path'], self._get_sections()),
            key=len, reverse=True)

        mapping = dict(map(lambda path: (path, []), section_paths))
        for obj in self._get_merged_brefs():
            path = '/'.join(obj.getPhysicalPath())
            possible_sec_paths = [spath for spath in section_paths
                                  if path.startswith(spath)]

            # use the longest section path
            spath = sorted(possible_sec_paths, key=len, reverse=True)[0]
            mapping[spath].append(obj)

        result = []
        for section in map(deepcopy, self._get_sections()):
            if mapping[section['path']]:
                section['objects'] = mapping[section['path']]
                result.append(section)

        return result

    def _get_merged_brefs(self):
        """Returns all backrefrences to the current context and its
        similar topic objects (see _get_similar_topic_objects docstring).
        """
        return reduce(list.__add__,
                      map(lambda obj: IReferenceable(obj).getBRefs(),
                          self._get_similar_topic_objects()))

    def _get_similar_topic_objects(self):
        """Returns all objects which have the same relative path to the
        nearest parent providing self.group_by (INavigationRoot by default)
        as the current context.
        The current context is included.
        """
        topic_path = '/'.join(self.context.getPhysicalPath())

        section_paths = sorted(map(lambda item: item.get('path'),
                                   self._get_sections()),
                               key=len, reverse=True)
        section_path = [spath for spath in section_paths
                        if topic_path.startswith(spath)][0]

        # path of context relative to next subsite or site root
        relative_path = topic_path.replace(section_path + '/', '', 1)

        # possibile similar paths
        similar_paths = map(lambda path: '/'.join((path, relative_path)),
                            section_paths)

        # similar brains, including the current context
        query = {'path': {'query': similar_paths,
                          'depth': 0}}
        catalog = getToolByName(self.context, 'portal_catalog')
        return map(lambda brain: brain.getObject(), catalog(query))
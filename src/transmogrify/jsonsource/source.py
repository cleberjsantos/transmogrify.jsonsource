# -*- coding: utf-8 -*-

from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import Expression, Condition
from collective.transmogrifier.utils import resolvePackageReferenceOrFile
try:
    import simplejson as json
except ImportError:
    import json
import logging
import os
import re
from pprint import pprint, pformat
from zope.interface import classProvides, implements




class JsonFilesystemSource(object):
    """Read JSON objects from the file system.
    """
    classProvides(ISectionBlueprint)
    implements(ISection)


    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        self.key = Expression(options['key'], transmogrifier, name, options)
        self.value = Expression(options['value'], transmogrifier, name,
                                options)

        self.condition = Condition(options.get('condition', 'python:True'),
                                   transmogrifier, name, options)

        self.debug = options.get('debug', False)
        self.filename = options.get('filename','data.json')
        path = resolvePackageReferenceOrFile(options.get('path',''))
        types = options.get('types',[]).strip('\n').rsplit('\n')
        sections = options.get('sections',[]).strip('\n').rsplit('\n')
        self.results = self._unjsonify(path, types, sections)

        self.logger = logging.getLogger(name)

    def __iter__(self):
        for item in self.previous:
            key = self.key(item)
            if self.condition(item, key=key):
                item[key] = self.value(item, key=key)
            yield item

        i = 0
        for item in self.results:
            i += 1
            if self.debug:
                self.logger.debug(pformat(item))
            yield item

        print i

    def _files(self,root):
        """Return a list of jsonified files that we need to import.
        """
        filename = self.filename
        files = (p for p, d, f in os.walk(root) if filename in f)
        f = [f for f in files]
        f.sort()
        files = [os.path.join(path, filename) for path in f]
        return files

    def _unjsonify(self, root, filter_types=None, filter_sections=None):
        """Load a list of jsonified objects.
        """
        for f in self._files(root):
            with open(f) as fp:
                try:
                    data = json.loads(fp.read())
                except:
                    continue
                if filter_sections:
                    for sec in filter_sections:
                        if re.search(sec, data['_path']):
                            if filter_types and data['_type'] in filter_types:
                                yield data
                else:
                    if filter_types and data['_type'] in filter_types:
                        yield data

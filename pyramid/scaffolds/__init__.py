import binascii
import os

from pyramid.compat import native_

from pyramid.scaffolds.template import Template

class PyramidTemplate(Template):
    def pre(self, command, output_dir, vars):
        vars['random_string'] = native_(binascii.hexlify(os.urandom(20)))
        package_logger = vars['package']
        if package_logger == 'root':
            # Rename the app logger in the rare case a project is named 'root'
            package_logger = 'app'
        vars['package_logger'] = package_logger
        return Template.pre(self, command, output_dir, vars)

    def post(self, command, output_dir, vars): # pragma: no cover
        self.out('Welcome to Pyramid.  Sorry for the convenience.')
        return Template.post(self, command, output_dir, vars)

    def out(self, msg): # pragma: no cover (replaceable testing hook)
        print(msg)

class StarterProjectTemplate(PyramidTemplate):
    _template_dir = 'starter'
    summary = 'Pyramid starter project'

class ZODBProjectTemplate(PyramidTemplate):
    _template_dir = 'zodb'
    summary = 'Pyramid ZODB project using traversal'

class AlchemyProjectTemplate(PyramidTemplate):
    _template_dir = 'alchemy'
    summary = 'Pyramid SQLAlchemy project using url dispatch'
    def post(self, command, output_dir, vars): # pragma: no cover
        val = PyramidTemplate.post(self, command, output_dir, vars)
        self.out('')
        self.out('Please run the "populate_%(package)s" script to set up the '
                 'SQL database before starting the application (e.g. '
                 '"$myvirtualenv/bin/populate_%(package)s development.ini".)'
                 % vars)
        return val

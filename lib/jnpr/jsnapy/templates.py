"""
template renderers
"""

import os
import imp
import jinja2
import yaml

from jnpr.junos.factory.factory_loader import FactoryLoader
from jnpr.jsnapy.exceptions import JsnapyRenderError

class TemplateRenderer():
    """
    Jsnapy template renderer

    The default rendering engine is yaml.
    """
    def __init__(self):
        pass

    def load(self, tpl_file, dev=None):
        try:
            with open(tpl_file, 'r') as f:
                tpl = f.read()
        except EnvironmentError:
            raise JsnapyRenderError(
                    "Unable to load template file: {} ".format(tpl_file))

        # extract the first line from the template
        # to see if it's any of the supported rendering
        # formats
        header = tpl.split("\n")[0]

        if header.startswith("#!py"):
            return render_py(tpl_file, dev)

        # default rendering process is jinja then yaml
        data = render_jinja(tpl, dev)
        return render_yaml(data)

def render_jinja(tpl, dev=None):
    jinja_env = jinja2.Environment(block_start_string='<%',
            block_end_string='%>',
            variable_start_string='%%',
            variable_end_string='%%',
            comment_start_string='<#',
            comment_end_string='#>',
            extensions=['jinja2.ext.do','jinja2.ext.loopcontrols'],)
    try:
        template = jinja_env.from_string(tpl)
        output = template.render(dev=dev, loader=FactoryLoader())
    except Exception, e:
        raise JsnapyRenderError("problem rendering jinja template: {}".format(str(e)))

    return output

def render_yaml(tpl):
    return yaml.load(tpl)

def render_py(src, dev=None):
    m = imp.load_source(
            os.path.basename(src).split('.')[0],
            src)
    data = m.run(dev, FactoryLoader())
    return data


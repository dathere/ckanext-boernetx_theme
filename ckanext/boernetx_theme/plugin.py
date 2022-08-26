import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.boernetx_theme.helpers as h


class BoernetxThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('webassets',
            'boernetx_theme')

    # ITemaplateHelpers

    def get_helpers(self):
        return {"get_banner_image": h.get_banner_image}
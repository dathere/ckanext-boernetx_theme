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
        toolkit.add_resource('webassets','boernetx_theme')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "boerne_get_showcases": h.get_showcases,
            "boerne_recent_datasets": h.recent_dataset,
            "get_value_from_showcase_extras": h.get_value_from_showcase_extras,
            "get_popular_datasets": h.get_popular_datasets,
            "get_package_metadata": h.get_package_metadata,
            "get_thumbnail": h.get_thumbnail
        }

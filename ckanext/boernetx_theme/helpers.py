import ckan.plugins.toolkit as toolkit

def get_banner_image():
    # breakpoint()
    banner_img = toolkit.config.get("ckan.site_logo")

def get_showcases(num=6):
    '''Return a list of showcases'''
    # breakpoint()
    showcases = toolkit.get_action("ckanext_showcase_list")()
    return showcases


def recent_dataset(num=5):
    sorted_datasets = []

    datasets = toolkit.get_action("current_package_list_with_resources")({}, {"limit": num})

    if datasets:
        sorted_datasets = sorted(datasets, key=lambda k: k["metadata_modified"], reverse=True)

    return sorted_datasets[:num]
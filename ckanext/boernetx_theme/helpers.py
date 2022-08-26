import ckan.plugins.toolkit as toolkit

def get_banner_image():
    # breakpoint()
    banner_img = toolkit.config.get("ckan.site_logo")
import os
import logging

from PIL import Image

import ckan.plugins.toolkit as toolkit


log = logging.getLogger(__name__)


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


def get_value_from_showcase_extras(extras, key):
    value = ''
    for item in extras:
        if item.get('key') == key:
            value = item.get('value', '')
    return value


def get_popular_datasets(num=5):
    """Return a list of popular datasets."""
    datasets = []
    search = toolkit.get_action('package_search')({},{'rows': num, 'sort': 'views_recent desc'})
    if search.get('results'):
        datasets = search.get('results')
    return datasets[:num]


def get_package_metadata(package):
    """Return the metadata of a dataset"""
    # breakpoint()
    try:
        result = toolkit.get_action('package_show')({}, {'id': package.get('name'), 'include_tracking': True})
    except:
        print("Error in retrieving dataset metadata: {}".format(package.get('id', '')))
        package_metadata = package
        package_metadata['tracking_summary'] = {}
        package_metadata['tracking_summary']['total'] = 0
        return package_metadata
    return result


def create_thumbnail( image_path ):
    """
    Create a thumbnail image in the samee directory the original image exists in
    thumbnail for image.png will be called image-thumbnail.png
    """

    thumb_path =  "{0}-{2}.{1}".format(*image_path.rsplit('.', 1) + ['thumbnail'])

    try:
        image = Image.open(image_path)
    except IOError:
        #if an image can't be parsed from the response...
        log.debug( IOError )
        return None

    width = int( toolkit.config.get('ckan.thumbnail_width', 200) )
    height = int( toolkit.config.get('ckan.thumbnail_height', 200) )

    image.thumbnail( ( width, height ) )
    image.save( thumb_path )

    return True


def get_thumbnail( image_url ):
    """
    Given a URL of an existing image, return the thumbnail
    If a thumbnail doesn't exist, create one on the fly
    """

    #log.debug( 'retrieving thumbnail for ' + image_url)

    # check to see if image is remote, if so just return image since we can't make a thumbnail of a remote image
    site_url = toolkit.config.get("ckan.site_url") 
    if image_url.startswith( 'http' ) and not image_url.startswith( site_url ): 
        return image_url

    thumb_url = ""
    image_path = ""
    storage_path = toolkit.config.get("ckan.storage_path") + '/storage'

    #log.debug( 'storage_path = ' + storage_path)

    if image_url != None and "." in image_url:

        # handle fully qualified URL
        if image_url.startswith( 'http' ):
            image_path =  "/{3}".format( *image_url.split('/', 3) )

        # image is relative path
        else:
            image_path = image_url

        # convert image_fp to thumb_fp by adding -thumbnail before the file extension
        thumb_url =  "{0}-{2}.{1}".format(*image_path.rsplit('.', 1) + ['thumbnail'])


    thumb_path = storage_path + thumb_url
    #log.debug( 'thumb_path =  ' + thumb_path)

    if not os.path.exists( thumb_path ):
        #log.debug( 'thumbnail does not exist, trying to create one for ' + storage_path + image_path)
        create_thumbnail( storage_path + image_path )

    if os.path.exists( thumb_path ):
        #log.debug(  'returning thumb image ' + thumb_url );
        return thumb_url
    else:
        #log.debug(  'returning non-thumb image ' + image_url );
        return image_url
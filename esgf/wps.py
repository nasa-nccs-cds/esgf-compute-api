""" A WPS Client """

import json

from owslib.wps import WebProcessingService

_IDENTIFICATION = (
    'title',
    'abstract',
    'keywords',
    'accessconstraints',
    'fees',
    'type',
    'service',
    'version',
    'profiles'
)

_PROVIDER = (
    'name',
    'contact',
    'url'
)

_CONTACT = (
    'name',
    'organization',
    'site',
    'position',
    'phone',
    'fax',
    'address',
    'city',
    'region',
    'postcode',
    'country',
    'email',
    'url',
    'hours',
    'instructions'
)

class WPS(object):
    """ WPS client.

    A WPS client built around owslib.wps.WebProcessingService.
    Provides access to WPS GetCapabilities and Execute requests.

    """

    def __init__(self, url, username=None, password=None):
        """ Inits WebProcessingService """
        self._service = WebProcessingService( \
            url, \
            username=username, \
            password=password, \
            verbose=False,  \
            skip_caps=True)

    def init(self):
        """ Executes WPS GetCapabilites request.

        Retrieves a servers description data (identification and provider)
        and its processes.

        """
        self._service.getcapabilities()

    @property
    def identification(self):
        """ Returns identification data as JSON. """
        ident = self._service.identification

        return dict((x, getattr(ident, x)) for x in _IDENTIFICATION)

    @property
    def provider(self):
        """ Returns provider data as JSON. """
        prov = self._service.provider

        prov_dict = dict((x, getattr(prov, x)) for x in _PROVIDER)

        contact = prov_dict['contact']

        prov_dict['contact'] = dict((x, getattr(contact, x)) for x in _CONTACT)

        return prov_dict

    def __str__(self):
        """ Returns pretty metadata. """
        data = {
            'identification': self.identification,
            'provider': self.provider
        }

        return json.dumps(data, indent=4)

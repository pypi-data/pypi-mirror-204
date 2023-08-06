'''
Access Free Open Source License information on the command line

:copyright: (c) 2022 Ralf Luetkemeier
:license: MIT License, see LICENSE for more details.
'''

from datetime import datetime

import requests


__all__ = ['get_license_info', 'get_license_text',
           'GitHubApiRateLimitExceeded', 'LicenseNotFoundError']
__version__ = '0.11.0'

TIMEOUT = 2


# Uses GitHub's REST API to obtain Open Source license information
# See https://developer.github.com/v3/licenses/
_URL = "https://api.github.com/licenses"
_URL_RATE_LIMIT = "https://api.github.com/rate_limit"


class LicenseNotFoundError(ValueError):
    '''An exception raised when information on an unknown license is
       requested.'''
    def __init__(self, spdx_id):
        '''Constructor'''
        super().__init__(f'Unkown license {spdx_id}')
        self.spdx_id = spdx_id


class GitHubApiRateLimitExceeded(Exception):
    '''Exception to be raised when the GitHub REST API has been accessed
       too often i.e. the rate limit has been exceeded. The exception
       informs at which time the rate limit will be reset.'''
    def __init__(self, rate_info):
        super().__init__()
        datm = datetime.fromtimestamp(rate_info['reset'])
        self.reset_at = datm.strftime('at %H:%M:%S on %Y-%m-%d')
        self.remaining = rate_info['remaining']
        self.limit = rate_info['limit']
        self.used = rate_info['used']
        self.message = ('The GitHub REST API rate limit has been exceeded. '
                       f'It will be reset {self.reset_at}.')   # noqa: E128

    def __str__(self):
        return self.message


def check_api_rate_exceeded():
    '''Tests whether the API rate limit was exceeded or not.'''
    response = requests.get(_URL_RATE_LIMIT, timeout=TIMEOUT)
    # To see the full response enter
    # curl \
    #   -H "Accept: application/vnd.github.v3+json" \
    #   https://api.github.com/rate_limit
    core = response.json()['resources']['core']
    if core['remaining'] == 0:
        raise GitHubApiRateLimitExceeded(core)


def get_license_info(*spdx_ids):
    '''
    :param: spdx_ids
    :raises: GitHubApiRateLimitExceeded
    :raises: LicenseNotFoundError
    '''
    if not spdx_ids:
        response = requests.get(_URL, timeout=TIMEOUT)
        if response.status_code == 403:
            check_api_rate_exceeded()
        licenses = response.json()
    else:
        licenses = []
        for spdx_id in spdx_ids:
            response = requests.get(_URL + f'/{spdx_id}', timeout=TIMEOUT)
            if response.status_code == 404:
                raise LicenseNotFoundError(spdx_id)
            if response.status_code == 403:
                check_api_rate_exceeded()
            licenses.append(response.json())
    return licenses


def get_license_text(spdx_id):
    '''Returns the license text for the SPDX ID in the argument.'''
    license_info = get_license_info(spdx_id)[0]
    return license_info['body']


# Additional resources:
# Fetching license types
# https://api.github.com/licenses
# Returned JSON contains a list of dicts, 'key' contains the short name for
# each license.
# https://api.github.com/licenses/{license}
# Example:
# https://api.github.com/licenses/apache-2.0

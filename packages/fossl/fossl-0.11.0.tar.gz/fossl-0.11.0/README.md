# fossl

[![Python versions](https://img.shields.io/pypi/pyversions/fossl.svg)](https://pypi.org/project/fossl/)
[![PyPI version](https://img.shields.io/pypi/v/fossl.svg)](https://pypi.org/project/fossl/)
[![License](https://img.shields.io/pypi/l/fossl.svg)](https://pypi.org/project/fossl/)

fossl provides descriptions of the most common free open source (FOSS) licenses. Instructions on how to apply a license to the source code are included. The information is obtained from GitHub i.e. is always up-to-date. The license texts for "LICENSE" files can also be downloaded.

```sh
% fossl list
AGPL-3.0     - GNU Affero General Public License v3.0
Apache-2.0   - Apache License 2.0
BSD-2-Clause - BSD 2-Clause "Simplified" License
BSD-3-Clause - BSD 3-Clause "New" or "Revised" License
CC0-1.0      - Creative Commons Zero v1.0 Universal
EPL-2.0      - Eclipse Public License 2.0
GPL-2.0      - GNU General Public License v2.0
GPL-3.0      - GNU General Public License v3.0
LGPL-2.1     - GNU Lesser General Public License v2.1
LGPL-3.0     - GNU Lesser General Public License v3.0
MIT          - MIT License
MPL-2.0      - Mozilla Public License 2.0
Unlicense    - The Unlicense
```

```sh
% fossl show Apache-2.0
SPDX ID:            │ Apache-2.0
Name:               │ Apache License 2.0
Description:        │ A permissive license whose main conditions require
                    │ preservation of copyright and license notices.
                    │ Contributors provide an express grant of patent rights.
                    │ Licensed works, modifications, and larger works may be
                    │ distributed under different terms and without source
                    │ code.
Implementation:     │ Create a text file (typically named LICENSE or
                    │ LICENSE.txt) in the root of your source code and copy
                    │ the text of the license into the file.
Permissions:        │ commercial-use, modifications, distribution, patent-use,
                    │ private-use
Conditions          │ include-copyright, document-changes
Limitations:        │ trademark-use, liability, warranty
HTML URL:           │ http://choosealicense.com/licenses/apache-2.0/
GitHub API URL:     │ https://api.github.com/licenses/apache-2.0
Featured on GitHub: │ Yes
```

Finally,

```sh
% fossl show MIT -text > LICENSE
```

creates a LICENSE file for a new project.

`fossl` can also be used as a Python package, allowing Python code to access license information.

## Limitations

GitHub limits the number of queries a user may make per hour. For unauthenticated users like `fossl`, that [rate limit](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting) is 60 / hour.

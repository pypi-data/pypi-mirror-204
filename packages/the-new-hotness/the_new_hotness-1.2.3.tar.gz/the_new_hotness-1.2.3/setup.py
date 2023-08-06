# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hotness',
 'hotness.builders',
 'hotness.common',
 'hotness.databases',
 'hotness.domain',
 'hotness.exceptions',
 'hotness.notifiers',
 'hotness.patchers',
 'hotness.requests',
 'hotness.responses',
 'hotness.use_cases',
 'hotness.validators']

package_data = \
{'': ['*']}

install_requires = \
['anitya-schema>=2.0.1,<3.0.0',
 'fedora-messaging-the-new-hotness-schema>=1.1.2,<2.0.0',
 'fedora-messaging>=3.1.0,<4.0.0',
 'koji>=1.30.0,<2.0.0',
 'python-bugzilla>=3.2.0,<4.0.0',
 'redis>=4.3.4,<5.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'the-new-hotness',
    'version': '1.2.3',
    'description': 'A fedora messaging consumer that files bugzilla bugs for upstream releases',
    'long_description': ".. image:: https://img.shields.io/pypi/v/the-new-hotness.svg\n  :target: https://pypi.org/project/the-new-hotness/\n\n.. image:: https://readthedocs.org/projects/the-new-hotness/badge/?version=latest\n  :alt: Documentation Status\n  :target: https://the-new-hotness.readthedocs.io/en/latest/?badge=latest\n\nthe-new-hotness\n---------------\n\n`Fedora-messaging <https://github.com/fedora-infra/fedora-messaging>`_ consumer that listens to `release-monitoring.org\n<http://release-monitoring.org>`_ and files bugzilla bugs in response (to\nnotify packagers that they can update their packages).\n\nFor additional information see `documentation <https://the-new-hotness.readthedocs.io/en/stable/>`_.\n\nSeeing it in action\n^^^^^^^^^^^^^^^^^^^\n\nTo see recent messages from the-new-hotness:\n\n* Check Fedora's `datagrepper\n  <https://apps.fedoraproject.org/datagrepper/raw?category=hotness&delta=2592000>`_\n\n* Or join #fedora-fedmsg IRC channel on `libera <https://libera.chat/>`_ and watch for ``hotness``\n  messages.\n\nTo see recent koji builds started by the-new-hotness:\n\n* Check Fedora's `koji builds\n  <https://koji.fedoraproject.org/koji/tasks?owner=the-new-hotness/release-monitoring.org&state=all>`_\n\nDevelopment\n^^^^^^^^^^^\n\nContributions are welcome, check out `contribution guidelines <https://the-new-hotness.readthedocs.io/en/stable/dev-guide.html#contribution-guidelines>`_.\n",
    'author': 'Ralph Bean',
    'author_email': 'rbean@redhat.com',
    'maintainer': 'Michal Konecny',
    'maintainer_email': 'mkonecny@redhat.com',
    'url': 'https://github.com/fedora-infra/the-new-hotness',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)

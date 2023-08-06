# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cfgs']
setup_kwargs = {
    'name': 'cfgs',
    'version': '0.12.0',
    'description': '🍇 XDG standard config files 🍇',
    'long_description': "`cfgs`\n-------------\n\nSimple, correct handling of config, data and cache files\n==================================================================\n\nLike everyone else, I wrote a lot of programs which saved config files\nas dotfiles in the user's home directory like ``~/.my-program-name`` and now\neveryone's home directory has dozens of these.\n\nThen I read\n`this article <https://0x46.net/thoughts/2019/02/01/dotfile-madness/>`_.\n\nGreat was my embarrasment to discover that there was a\n`neat little specification <https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_\nfor data, config and cache directories in Linux that prevents this problem, and\nthat I was not using it:\n\nSo I implemented a small and simple Python API as a single file, ``cfgs.py``.\n\nIt works on all versions of Python from 2.7 to 3.7, has complete test coverage,\nand all the functionality is reachable from a single class, ``cfgs.App``\n\nHow it works in one sentence\n===========================================\n\nCreate a ``cfgs.App`` for your application, project, or script which\nhandles finding, reading and writing your data and config files, and\nmanaging your cache directories.\n\nHow to install\n=====================\n\nYou can either use pip:\n\n.. code-block:: bash\n\n    pip install cfgs\n\nOr if you don't like dependencies (and who does?), you can drop the source file\n`cgfs.py <https://raw.githubusercontent.com/timedata-org/cfgs/master/cfgs.py>`_\nright into your project.\n\n\nUsage examples\n==================\n\n.. code-block:: python\n\n    import cfgs\n    app = cfgs.App('my-project')\n    print(app.xdg.XDG_CACHE_HOME)\n    #   /home/tom/.cache/my-project\n\n    app.xdg.XDG_CONFIG_DIRS\n    #   /etc/xdg\n\n    with app.config.open() as f:\n        f.update(name='oliver', species='dog')\n        f['description'] = {'size': 'S', 'fur': 'brown'}\n        print(f.filename)\n    #    /home/tom/.cache/my-project/my-project.json\n\n    # Later:\n    with app.config.open() as f:\n        print(f['name'])\n    #    oliver\n\n        print(f.as_dict())\n    #     {'name': 'oliver', 'species': 'dog',\n    #      'description': {'size': 'S', 'fur': 'brown'}\n\n\nCache\n======\n\n.. code-block:: python\n\n    import cfgs\n    cache_size = 0x10000000\n    app = cfgs.App('my-project')\n    directory = app.cache.directory(cache_size=cache_size)\n    # TODO: rewrite cache or add features.\n\n\nUsing ``cfgs`` In legacy code\n=============================\n\nIf you already have code to handle your config, data and cache files, then you\ncan just use ``cgfs`` to get the\n`XDG variables <https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_\n\n.. code-block:: python\n\n    from cfgs import XDG\n\n    xdg = XDG()\n    config_dir = xdg.XDG_CONFIG_HOME\n\n    # Your code here - eg:\n    my_config_file = os.path.join(config_dir, 'my-file.json')\n    with open(my_config_file) as f:\n        legacy_write_my_file(f)\n\n\n``cfgs`` automatically handles data and config files, and independently, cache\ndirectories.\n\n\nAPI Documentation\n======================\n\nAPI documentation is `here <https://timedata-org.github.io/cfgs/cfgs.html>`_.\n\n--------------------------------------\n\n====== ======\n|pic1| |pic2|\n====== ======\n\n\n.. |pic2| image::\n          https://img.shields.io/travis/timedata-org/cfgs/master.svg?style=flat\n\n.. |pic1| image:: https://img.shields.io/pypi/pyversions/cfgs.svg?style=flat\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

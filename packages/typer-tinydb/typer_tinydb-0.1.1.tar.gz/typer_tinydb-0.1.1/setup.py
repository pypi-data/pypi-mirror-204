# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typer_tinydb']

package_data = \
{'': ['*']}

install_requires = \
['tinydb>=4.7.1,<5.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tcfg = typer_tinydb.typerdb:cfg',
                     'typer-configure = typer_tinydb.typerdb:config',
                     'typer-tinydb-config = typer_tinydb.typerdb:config']}

setup_kwargs = {
    'name': 'typer-tinydb',
    'version': '0.1.1',
    'description': 'A Python Typer CLI subcommand boilerplate to manage config files using tinydb',
    'long_description': '# A Typer config file get/set boilerplate\n\n# Using the boilerplate\n\n## Aliases and subcommands\n\nWe recommand the following aliases, which are readily available out of the box.\n\n- `config`\n- `cfg`\n- `c`\n\nThis way, if your app is named `super-app`\n\nAnd is defined in `super_app.py` roughly as follows:\n\n```python\n\nimport typer\n\n# ... some imports\n\napp = typer.Typer(\n    name=\'super-app\',\n    # ... other args\n)\n```\n\nYou just have to add the following below:\n\n```python\nfrom typer_tinydb import cfg, config # those are typer apps\n\napp.add_typer(cfg) # the cfg app\napp.add_typer(config) # the config app\n```\n\nYou can rename them however you like by using\n\n```python\napp.add_typer(cfg, name=\'my-super-config\')\n```\n\n## Using it on the command line\n\nWith the same configuration as above, your new app can now run the commands:\n\n```bash\nsuper-app cfg list # list config key:value pairs\nsuper-app cfg get some-key # get the values linked to the key \'some-key\'\nsuper-app cfg set some-key \'20-hS407zuqYKQ8tPP2r5\' # store some hash or token into your settings file\nsuper-app cfg set some-key \'20-hS407zuqYKQ8tPP2r5\'\n```\n\nYou can obviously use `super-app config get` and others, or any name you attribute to it.\n\n## Using it within python modules\n\nThe CLI key-values are stored in a tinydb instance that is available by just importing the table named `globals`:\n\n```python\nfrom typer_tinydb import db, globals, where\n```\n\nYou can create any table using the database object `db`, please [check out the tinydb docs !](https://tinydb.readthedocs.io/)\n\nTo get the key just use `where` :\n\n```python\nreturns = globals.search(where(\'param\') == param)\n```\n\nTo insert new values or update existing, use the `upsert` function:\n\n```python\nParam = Query()\n\nglobals.upsert({\n    "param": param,\n    "value": value,\n    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),\n    "machine": socket.gethostname(),\n    },\n    Param.param == param\n)\n```\n\n# Commands\n\n## Command `typer-tinydb-config`\n\nConfigure the app 🛠️.\n\n**Usage**:\n\n```console\n$ typer-tinydb-config [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `get`: Get a config value.\n* `list`: List all config values.\n* `reset`: Reset all config values.\n* `set`: Set a config value.\n\n### Command `typer-tinydb-config get`\n\nGet a config value.\n\n**Usage**:\n\n```console\n$ typer-tinydb-config get [OPTIONS] PARAM\n```\n\n**Arguments**:\n\n* `PARAM`: The parameter to get.  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### Command `typer-tinydb-config list`\n\nList all config values.\n\n**Usage**:\n\n```console\n$ typer-tinydb-config list [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### Command `typer-tinydb-config reset`\n\nReset all config values.\n\n**Usage**:\n\n```console\n$ typer-tinydb-config reset [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n### Command `typer-tinydb-config set`\n\nSet a config value.\n\n**Usage**:\n\n```console\n$ typer-tinydb-config set [OPTIONS] PARAM VALUE\n```\n\n**Arguments**:\n\n* `PARAM`: The parameter to set.  [required]\n* `VALUE`: The value to set the parameter to.  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n\n# Future updates\n\nThe idea is to add some extra features like\n\n- [ ] Creating your own tables from the CLI\n- [ ] Adding some customization (in terms of colors) for the printing\n- [ ] Adding obfuscation so that your `.json` config file cannot be easily glanced at by bypassers\n\n',
    'author': 'arnos-stuff',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://arnos-stuff.github.io/typer-tinydb/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

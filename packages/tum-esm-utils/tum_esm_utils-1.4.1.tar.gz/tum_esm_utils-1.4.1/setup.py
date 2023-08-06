# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tum_esm_utils']

package_data = \
{'': ['*'],
 'tum_esm_utils': ['ifg_parser/.gitignore',
                   'ifg_parser/.gitignore',
                   'ifg_parser/.gitignore',
                   'ifg_parser/.gitignore',
                   'ifg_parser/.gitignore',
                   'ifg_parser/.gitignore',
                   'ifg_parser/.gitignore',
                   'ifg_parser/glob_OPUSparms.F90',
                   'ifg_parser/glob_OPUSparms.F90',
                   'ifg_parser/glob_OPUSparms.F90',
                   'ifg_parser/glob_OPUSparms.F90',
                   'ifg_parser/glob_OPUSparms.F90',
                   'ifg_parser/glob_OPUSparms.F90',
                   'ifg_parser/glob_OPUSparms.F90',
                   'ifg_parser/glob_prepro4.F90',
                   'ifg_parser/glob_prepro4.F90',
                   'ifg_parser/glob_prepro4.F90',
                   'ifg_parser/glob_prepro4.F90',
                   'ifg_parser/glob_prepro4.F90',
                   'ifg_parser/glob_prepro4.F90',
                   'ifg_parser/glob_prepro4.F90',
                   'ifg_parser/ifg_parser.F90',
                   'ifg_parser/ifg_parser.F90',
                   'ifg_parser/ifg_parser.F90',
                   'ifg_parser/ifg_parser.F90',
                   'ifg_parser/ifg_parser.F90',
                   'ifg_parser/ifg_parser.F90',
                   'ifg_parser/ifg_parser.F90',
                   'ifg_parser/ifg_parser.template.inp',
                   'ifg_parser/ifg_parser.template.inp',
                   'ifg_parser/ifg_parser.template.inp',
                   'ifg_parser/ifg_parser.template.inp',
                   'ifg_parser/ifg_parser.template.inp',
                   'ifg_parser/ifg_parser.template.inp',
                   'ifg_parser/ifg_parser.template.inp',
                   'ifg_parser/refspec.dat',
                   'ifg_parser/refspec.dat',
                   'ifg_parser/refspec.dat',
                   'ifg_parser/refspec.dat',
                   'ifg_parser/refspec.dat',
                   'ifg_parser/refspec.dat',
                   'ifg_parser/refspec.dat',
                   'ifg_parser/refspec2.dat',
                   'ifg_parser/refspec2.dat',
                   'ifg_parser/refspec2.dat',
                   'ifg_parser/refspec2.dat',
                   'ifg_parser/refspec2.dat',
                   'ifg_parser/refspec2.dat',
                   'ifg_parser/refspec2.dat']}

modules = \
['py']
install_requires = \
['filelock>=3.10.0,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'psutil>=5.9.4,<6.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'tum-esm-utils',
    'version': '1.4.1',
    'description': 'Python utilities by the Professorship of Environmental Sensing and Modeling at the Technical University of Munich',
    'long_description': '# 🔬 &nbsp;TUM ESM Python Utilities\n\n**Install the Python library with:**\n\n```bash\npoetry add tum_esm_utils\n# or\npip install tum_esm_utils\n```\n\n<br/>\n\n## For Developers\n\n**Publish the Package to PyPI:**\n\n```bash\npoetry build\npoetry publish\n```\n\n**Serve documentation page:**\n\n```bash\ndocsify serve ./docs\n```\n',
    'author': 'Moritz Makowski',
    'author_email': 'moritz.makowski@tum.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tum-esm/utils',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

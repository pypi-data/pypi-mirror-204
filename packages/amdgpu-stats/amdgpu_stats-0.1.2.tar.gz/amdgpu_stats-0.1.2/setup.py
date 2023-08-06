# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amdgpu_stats']

package_data = \
{'': ['*']}

install_requires = \
['humanfriendly>=10.0', 'textual>=0.10']

entry_points = \
{'console_scripts': ['amdgpu-stats = amdgpu_stats.amdgpu_stats:main']}

setup_kwargs = {
    'name': 'amdgpu-stats',
    'version': '0.1.2',
    'description': 'A simple TUI (using Textual) that shows AMD GPU statistics',
    'long_description': '# amdgpu_stats\n\nSimple TUI _(using [Textual](https://textual.textualize.io/))_ that shows AMD GPU statistics\n\n- GPU Utilization\n- Temperatures _(as applicable)_\n    - Edge\n    - Junction\n    - Memory\n- Core clock\n- Core voltage\n- Memory clock\n- Power consumption\n- Power limits\n    - Default\n    - Configured\n    - Board capability\n - Fan RPM\n    - Current\n    - Target\n\nMain screen:\n![Screenshot of main screen](https://raw.githubusercontent.com/joshlay/amdgpu_stats/master/screens/main.png "Main screen")\n\nLog screen:\n![Screenshot of log screen](https://raw.githubusercontent.com/joshlay/amdgpu_stats/master/screens/logging.png "Logging screen")\n\nStatistics are not logged; only toggling Dark/light mode and the stat names / source files.\n\nTested _only_ on `RX6000` series cards; more may be supported. Please file an issue if finding incompatibility!\n\n## Installation / Usage\n```\npip install amdgpu-stats\n```\nOnce installed, run `amdgpu-stats` in your terminal of choice\n## Requirements\nOnly `Linux` is supported. Information is _completely_ sourced from interfaces in `sysfs`.\n\nIt _may_ be necessary to update the `amdgpu.ppfeaturemask` parameter to enable metrics.\n\nThis is assumed present for *control* over the elements being monitored. Untested without. \n\nSee [this Arch Wiki entry](https://wiki.archlinux.org/title/AMDGPU#Boot_parameter) for context.\n',
    'author': 'Josh Lay',
    'author_email': 'pypi@jlay.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joshlay/amdgpu_stats',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

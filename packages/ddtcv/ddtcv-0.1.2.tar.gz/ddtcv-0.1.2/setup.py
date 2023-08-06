# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ddtcv', 'ddtcv.tests', 'ddtcv.tools']

package_data = \
{'': ['*'],
 'ddtcv': ['static/model/angle_1_rec_en_number_lite/*',
           'static/model/wind_1_rec_en_number_lite/*'],
 'ddtcv.tests': ['image/*']}

install_requires = \
['numpy>=1.21.6,<2.0.0',
 'onnxruntime>=1.13.1,<2.0.0',
 'opencv-python>=4.4.0.46,<5.0.0.0']

setup_kwargs = {
    'name': 'ddtcv',
    'version': '0.1.2',
    'description': 'DDT CV.',
    'long_description': 'Examples are as follows.\n```python\nimport ddtcv\n\nwind_value = ddtcv.Wind("your_image_array")\nangle_value = ddtcv.Angle("your_image_array")\n```\nThat\'s all.',
    'author': 'TsangHans',
    'author_email': 'gzzenghan@189.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

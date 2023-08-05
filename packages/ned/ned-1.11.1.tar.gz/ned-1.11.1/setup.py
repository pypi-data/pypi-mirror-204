# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ned',
 'ned.actors',
 'ned.actors.dataset',
 'ned.autodata',
 'ned.candidate_generation',
 'ned.candidate_generation.pyserini',
 'ned.candidate_ranking',
 'ned.candidate_ranking.dataset',
 'ned.candidate_ranking.helpers',
 'ned.candidate_ranking.metrics',
 'ned.data_models',
 'ned.data_models.deprecated',
 'ned.entity_recognition',
 'ned.entity_recognition.model_data',
 'ned.models_and_training']

package_data = \
{'': ['*']}

install_requires = \
['hugedict>=2.9.1,<3.0.0',
 'kgdata>=3.4.2,<4.0.0',
 'nptyping>=2.5.0,<3.0.0',
 'osin>=1.11.3,<2.0.0',
 'pyarrow>=11.0.0,<12.0.0',
 'ream2>=2.2.0,<3.0.0',
 'sem-desc>=4.8.0,<5.0.0',
 'serde2>=1.6.0,<2.0.0',
 'sm-datasets>=1.1.3,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'torchaudio>=0.12.1,<0.13.0',
 'torchvision>=0.13.1,<0.14.0']

setup_kwargs = {
    'name': 'ned',
    'version': '1.11.1',
    'description': 'entity linking, named-entity disambiguation, record linkage',
    'long_description': 'None',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

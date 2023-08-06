# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pit30m', 'pit30m.data', 'pit30m.torch']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.5',
 'fsspec>=2022',
 'geopandas>=0.10',
 'joblib',
 'lz4>=4',
 'matplotlib>=3.4',
 'numpy>=1.20',
 'pillow>=9',
 'pygeos>=0.12',
 'pyyaml>=5',
 's3fs',
 'tqdm>=4',
 'utm>=0.7.0']

setup_kwargs = {
    'name': 'pit30m',
    'version': '0.0.1',
    'description': 'Development kit for the Pit30M large scale localization dataset',
    'long_description': '# Pit30M Development Kit\n\n<!-- TODO(andrei): Add PyPI versions. -->\n[![Python CI Status](https://github.com/pit30m/pit30m/actions/workflows/ci.yaml/badge.svg)](https://github.com/pit30m/pit30m/actions/workflows/ci.yaml)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)\n[![Public on the AWS Open Data Registry](https://shields.io/badge/Open%20Data%20Registry-public-green?logo=amazonaws&style=flat)](#)\n\n## Overview\nThis is the Python software development kit for the Pit30M benchmark for large-scale global localization. The devkit is currently in a pre-release state and many features are coming soon!\n\nConsider checking out [the original paper](https://arxiv.org/abs/2012.12437). If you would like to, you could also follow some of the authors\' social media, e.g., [Andrei\'s](https://twitter.com/andreib) in order to be among\nthe first to hear of any updates!\n\n\n## Getting Started\n\nThe recommended way to interact with the dataset is with the `pip` package, which you can install with:\n\n`pip install pit30m`\n\nThe devkit lets you efficiently access data on the fly. Here is a "hello world" command which renders a demo video from a random log segment. Note that it assumes `ffmpeg` is installed:\n\n`python -m pit30m.cli multicam_demo --out-dir .`\n\nTo preview data more interactively, check out the [tutorial notebook](examples/tutorial_00_introduction.ipynb).\n[![Open In Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/pit30m/pit30m/blob/main/examples/tutorial_00_introduction.ipynb)\n\nMore tutorials coming soon.\n\n### Torch Data Loading\n\nWe provide basic log-based PyTorch dataloaders. Visual-localization-specific ones are coming soon. To see an\nexample on how to use one of these dataloaders, have a look at `demo_dataloader` in `torch/dataset.py`.\n\nAn example command:\n\n```\npython -m pit30m.torch.dataset --root-uri s3://pit30m/ --logs 00682fa6-2183-4a0d-dcfe-bc38c448090f,021286dc-5fe5-445f-e5fa-f875f2eb3c57,1c915eda-c18a-46d5-e1ec-e4f624605ff0 --num-workers 16 --batch-size 64\n```\n\n## Features\n\n * Framework-agnostic multiprocessing-safe log reader objects\n * PyTorch dataloaders\n\n### In-progress\n * More lightweight package with fewer dependencies.\n * Very efficient native S3 support through [AWS-authored PyTorch-optimized S3 DataPipes](https://aws.amazon.com/blogs/machine-learning/announcing-the-amazon-s3-plugin-for-pytorch/).\n * Support for non-S3 data sources, for users who wish to copy the dataset, or parts of it, to their own storage.\n * Tons of examples and tutorials. See `examples/` for more information.\n\n\n## Development\n\nPackage development, testing, and releasing is performed with `poetry`. If you just want to use the `pit30m` package, you don\'t need to care about this section; just have a look at "Getting Started" above!\n\n 1. [Install poetry](https://python-poetry.org/docs/)\n 2. Setup/update your `dev` virtual environments with `poetry install --with=dev` in the project root\n    - If you encounter strange keyring/credential errors, you may need `PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry install --with=dev`\n 3. Develop away\n    - run commands like `poetry run python -m pit30m.cli`\n 4. Test with `poetry run pytest`\n 5. Remember to run `poetry install` after pulling and/or updating dependencies.\n\n\nNote that in the pre-release time, `torch` will be a "dev" dependency, since it\'s necessary for all tests to pass.\n\n## Publishing\n\n 1. [Configure poetry](https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04) with a PyPI account which has access to edit the package. You need to make sure poetry is configured with your API key.\n 2. `poetry publish --build`\n\n\n## Citation\n\n```bibtex\n@inproceedings{martinez2020pit30m,\n  title={Pit30m: A benchmark for global localization in the age of self-driving cars},\n  author={Martinez, Julieta and Doubov, Sasha and Fan, Jack and B{\\^a}rsan, Ioan Andrei and Wang, Shenlong and M{\\\'a}ttyus, Gell{\\\'e}rt and Urtasun, Raquel},\n  booktitle={{IROS}},\n  pages={4477--4484},\n  year={2020},\n  organization={IEEE}\n}\n```',
    'author': 'Andrei Bârsan',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

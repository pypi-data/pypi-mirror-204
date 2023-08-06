# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeno_evals']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.5.0,<0.6.0', 'zenoml>=0.4.10,<0.5.0']

entry_points = \
{'console_scripts': ['zeno-evals = zeno_evals.main:cli']}

setup_kwargs = {
    'name': 'zeno-evals',
    'version': '0.1.10',
    'description': 'Visualize OpenAI evals with Zeno',
    'long_description': '# Zeno 🤝 OpenAI Evals\n\nUse [Zeno](https://github.com/zeno-ml/zeno) to visualize the results of [OpenAI Evals](https://github.com/openai/evals/blob/main/docs/eval-templates.md).\n\nhttps://user-images.githubusercontent.com/4563691/225655166-9fd82784-cf35-47c1-8306-96178cdad7c1.mov\n\n_Example using `zeno-evals` to explore the results of an OpenAI eval on multiple choice medicine questions (MedMCQA)_\n\n### Usage\n\n```bash\npip install zeno-evals\n```\n\nRun an evaluation following the [evals instructions](https://github.com/openai/evals/blob/main/docs/run-evals.md). This will produce a cache file in `/tmp/evallogs/`.\n\nPass this file to the `zeno-evals` command:\n\n```bash\nzeno-evals /tmp/evallogs/my_eval_cache.jsonl\n```\n\n### Example\n\nSingle example looking at US tort law questions:\n\n```bash\nzeno-evals ./examples/example.jsonl\n```\n\nAnd an example of comparison between two models:\n\n```bash\nzeno-evals ./examples/crossword-turbo.jsonl --second-results-file ./examples/crossword-turbo-0301.jsonl\n```\n\nAnd lastly, we can pass additional [Zeno functions](https://zenoml.com/docs/api) to provide more context to the results:\n\n```bash\npip install wordfreq\nzeno-evals ./examples/crossword-turbo.jsonl --second-results-file ./examples/crossword-turbo-0301.jsonl --functions_file ./examples/crossword_fns.py\n```\n',
    'author': 'Alex Cabrera',
    'author_email': 'alex.cabrera@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<=3.11',
}


setup(**setup_kwargs)

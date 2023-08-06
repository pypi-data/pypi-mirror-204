# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['experiment_results_manager']

package_data = \
{'': ['*']}

install_requires = \
['fsspec>=2021.4', 'pydantic>=1.6,<2.0']

setup_kwargs = {
    'name': 'experiment-results-manager',
    'version': '0.1.1',
    'description': 'Light-weight experiment tracker',
    'long_description': '# ERM: Experiment Results Manager\n\n## Get Started\n\n```sh\n\npip install experiment-results-manager \\\n  gcsfs \\\n  s3fs\n# install s3fs if you plan to store data in s3\n# install gcsfs if you plan to store data in google cloud storage\n```\n\n```python\nimport experiment_results_manager as erm\nfrom IPython.display import display, HTML\nimport seaborn as sns\n\n# Creating arbitrary plot to log later\ntips = sns.load_dataset(\'tips\')\nmpl_fig = sns.barplot(x=\'day\', y=\'total_bill\', data=tips)\n\n# Create an experiment run\ner = erm.ExperimentRun(\n    experiment_id="my_experiment",\n    variant_id="main"\n)\n\n# Log relevant data\ner.log_param("objective", "rmse")\ner.log_metric("rmse", "0.9")\ner.log_figure(mpl_fig, "ROC Curve")\ner.log_text("lorem ipsum...", "text")\n\n# Generate HTML\nhtml = erm.compare_runs(er)\ndisplay(HTML(html))\n\n# Save the run to access later\nsaved_path = erm.save_run_to_registry(er, "s3:///erm-registry")\n\n# Load a previous run\ner2 = erm.load_run_from_path(saved_path)\n\n# Compare the current run with a previous one\nhtml = erm.compare_runs(er, er2)\ndisplay(HTML(html))\n```\n\n## Screenshots\n<img width="680" alt="image" src="https://user-images.githubusercontent.com/1297369/233116615-dd85a795-4b73-4be9-bced-42ebad5ea164.png">\n',
    'author': 'sa-',
    'author_email': 'name@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ml-cyclops/experiment-results-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

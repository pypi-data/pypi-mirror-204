# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['locusdb']

package_data = \
{'': ['*']}

install_requires = \
['hnswlib>=0.7.0,<0.8.0', 'numpy>=1.24.2,<2.0.0']

setup_kwargs = {
    'name': 'locusdb',
    'version': '0.2.0',
    'description': 'Local, in-memory vector database',
    'long_description': '# Locus\nLocus is a local, simple, in-memory vector database.\n\nWhy Locus?\n* Easy to use\n* 2 dependencies\n* Store database locally\n\n\n## Installation\n``` bash\npip install locusdb\n```\n## Example Code\nSome example code to illustrate Locus\' functionality.\n\n``` python\nimport numpy as np\nfrom locusdb import Config, Vector, Index\n\n# create a new configuration\nconfig = Config(max_elements=1000, ef_construction=200, M=16, dim=128, space="cosine", storage_location="index.db")\n\n# create a new index instance\nindex = Index(dimensions=config.dim, config=config)\n\n# create some random vectors\nvectors = []\nfor i in range(10):\n    embedding = np.random.randn(config.dim)\n    data = {"id": i, "message": f"test message {i}"}\n    vector = Vector(embedding=embedding, data=data)\n    vectors.append(vector)\n\n# add the vectors to the index\nfor vector in vectors:\n    index.add_vector(vector)\n\n# retrieve the closest vectors to a query embedding\nquery_embedding = np.random.randn(config.dim)\nresults = index.retrieve(query_embedding, number_of_results=3)\nprint(results)\n\n# store the index on disk\nindex._store_on_disk()\n\n# load the index from disk\nnew_index = Index.from_file(config.storage_location)\n```\n\n',
    'author': 'Alex',
    'author_email': '46456279+the-alex-b@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/the-alex-b/Locus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

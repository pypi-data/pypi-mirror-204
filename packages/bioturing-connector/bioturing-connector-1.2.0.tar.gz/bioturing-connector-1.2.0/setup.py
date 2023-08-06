# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bioturing_connector',
 'bioturing_connector.common',
 'bioturing_connector.typing']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.982,<0.983', 'pylint>=2.15.3,<3.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'bioturing-connector',
    'version': '1.2.0',
    'description': 'A set of python modules for accessing BBrowserX on private server',
    'long_description': '## 1. Installation:\n```\n  pip install bioturing_connector --index-url=https://pypi.bioturing.com\n\n  # Username: bioturing\n  # Password: code@bioturing.com\n```\n\n## 2. Usage:\n**The package only allows data submission via Amazon S3 Bucket. Please configure your S3 Bucket credentials in the `Settings` page.**\n### 2.1. Test the connection:\n```\n# example.py\n\nfrom bioturing_connector.connector import BBrowserXConnector\n\nconnector = BBrowserXConnector(\n  host="https://yourcompany/t2d_index_tool/,\n  token="<input your token here>"\n)\n\nconnector.test_connection()\n```\n\nExample output:\n\n```\nConnecting to host at https://yourcompany/t2d_index_tool/api/v1/test_connection\nConnection successful\n```\n\n### 2.2. Get user groups available for your token:\n```\n# example.py\n\nfrom bioturing_connector.connector import BBrowserXConnector\n\nconnector = BBrowserXConnector(\n  host="https://yourcompany/t2d_index_tool/,\n  token="<input your token here>"\n)\n\nuser_groups = connector.get_user_groups()\nprint(user_groups)\n```\n\nExample output:\n\n```\n[{\'id\': \'all_members\', \'name\': \'All members\'}, {\'id\': \'personal\', \'name\': \'Personal workspace\'}]\n```\n\n### 2.3. Submit h5ad (scanpy object):\n```\n# example.py\nfrom bioturing_connector.connector import BBrowserXConnector\nfrom bioturing_connector.typing import InputMatrixType\nfrom bioturing_connector.typing import Species\n\nconnector = BBrowserXConnector(\n  host="https://yourcompany/t2d_index_tool/,\n  token="<input your token here>"\n)\n\n# Call this function first to get available groups and their id.\nuser_groups = connector.get_user_groups()\n# Example: user_groups is now [{\'id\': \'all_members\', \'name\': \'All members\'}, {\'id\': \'personal\', \'name\': \'Personal workspace\'}]\n\n\n# Submitting the scanpy object:\nconnector.submit_h5ad(\n  group_id=\'personal\',\n  study_s3_keys=[\'GSE128223.h5ad\'],\n  study_id=\'GSE128223\',\n  name=\'This is my first study\',\n  authors=[\'Huy Nguyen\'],\n  species=Species.HUMAN.value,\n  input_matrix_type=InputMatrixType.RAW.value\n)\n\n# Example output:\n> [2022-10-10 01:03] Waiting in queue\n> [2022-10-10 01:03] Downloading GSE128223.h5ad from s3: 262.1 KB / 432.8 MB\n> [2022-10-10 01:03] File downloaded\n> [2022-10-10 01:03] Reading batch: GSE128223.h5ad\n> [2022-10-10 01:03] Preprocessing expression matrix: 19121 cells x 63813 genes\n> [2022-10-10 01:03] Filtered: 19121 cells remain\n> [2022-10-10 01:03] Start processing study\n> [2022-10-10 01:03] Normalizing expression matrix\n> [2022-10-10 01:03] Running PCA\n> [2022-10-10 01:03] Running kNN\n> [2022-10-10 01:03] Running spectral embedding\n> [2022-10-10 01:03] Running venice binarizer\n> [2022-10-10 01:04] Running t-SNE\n> [2022-10-10 01:04] Study was successfully submitted\n> [2022-10-10 01:04] DONE !!!\n> Study submitted successfully!\n```\nAvailable parameters for `submit_h5ad` function:\n```\ngroup_id: str\n  ID of the group to submit the data to.\n\nstudy_s3_keys: List[str]\n  List of the s3 key of the studies.\n\nstudy_id: str, default=None\n  Study ID, if no value is specified, use a random uuidv4 string\n\nname: str, default=\'To be detailed\'\n  Name of the study.\n\nauthors: List[str], default=[]\n  Authors of the study.\n\nabstract: str, default=\'\'\n  Abstract of the study.\n\nspecies: str, default=\'human\'\n  Species of the study. Can be: **bioturing_connector.typing.Species.HUMAN.value** or **bioturing_connector.typing.Species.MOUSE.value** or **bioturing_connector.typing.Species.NON_HUMAN_PRIMATE.value**\n\ninput_matrix_type: str, default=\'raw\'\n  If the value of this input is **bioturing_connector.typing.InputMatrixType.NORMALIZED.value**,\n  then the software will\n  use slot \'X\' from the scanpy object and does not apply normalization.\n  If the value of this input is **bioturing_connector.typing.InputMatrixType.RAW.value**,then the software will\n  use slot \'raw.X\' from thescanpy object and apply log-normalization.\n\nmin_counts: int, default=None\n  Minimum number of counts required\n  for a cell to pass filtering.\n\nmin_genes: int, default=None\n  Minimum number of genes expressed required\n  for a cell to pass filtering.\n\nmax_counts: int, default=None\n  Maximum number of counts required\n  for a cell to pass filtering.\n\nmax_genes: int, default=None\n  Maximum number of genes expressed required\n  for a cell to pass filtering.\n\nmt_percentage: Union[int, float], default=None\n  Maximum number of mitochondria genes percentage\n  required for a cell to pass filtering. Ranging from 0 to 100\n```\n',
    'author': 'BioTuring',
    'author_email': 'support@bioturing.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

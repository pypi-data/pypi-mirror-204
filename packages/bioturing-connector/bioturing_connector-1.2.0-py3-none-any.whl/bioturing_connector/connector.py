"""Python package for submitting/getting data from BBrowserX"""

import pandas as pd
from pathlib import Path

from urllib.parse import urljoin
from typing import List
from typing import Union

from .common import get_uuid
from .common import decode_base64_array

from .common.https_agent import HttpsAgent
from .common import common
from .typing import Species
from .typing import StudyType
from .typing import InputMatrixType
from .typing import UNIT_RAW

class BBrowserXConnector:
  """Create a connector object to submit/get data from BBrowserX
  """
  def __init__(self, host: str, token: str, ssl: bool = True):
    """
      Args:
        host:
          The URL of the BBrowserX server, only supports HTTPS connection
          Example: https://bbrowserx.bioturing.com
        token:
          The API token to verify authority. Generated in-app.
    """
    self.__host = host
    self.__token = token
    self.__https_agent = HttpsAgent(self.__token, ssl)


  def test_connection(self):
    """Test the connection with the host
    """
    url = urljoin(self.__host, 'api/v1/test_connection')

    print(f'Connecting to host at {url}')
    res = self.__https_agent.post(url=url)
    if res and 'status' in res and res['status'] == 200:
      print('Connection successful')
    else:
      print('Connection failed')


  def get_user_groups(self):
    """
      Get all the data sharing groups available for the current token
      ------------------
      Returns:
        [{
          'group_id': str (uuid),
          'group_name': str
        }, ...]
    """
    url = urljoin(self.__host, 'api/v1/get_user_groups')

    res = self.__https_agent.post(url=url)
    if res and 'status' in res and res['status'] == 200:
      return res['data']
    raise Exception('''Something went wrong, please contact support@bioturing.com''')


  def _submit_study(
    self,
    group_id: str,
    study_id: str = None,
    name: str = 'To be detailed',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    input_matrix_type: str = InputMatrixType.NORMALIZED.value,
    study_type: int = StudyType.H5AD.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    mt_percentage: Union[int, float] = None,
    skip_dimred: bool = False,
  ):
    if study_id is None:
      study_id = get_uuid()

    if min_counts is None:
      min_counts = 0

    if min_genes is None:
      min_genes = 0

    if max_counts is None:
      max_counts = 1e9

    if max_genes is None:
      max_genes = 1e9

    if mt_percentage is None:
      mt_percentage = 100

    study_info = {
      'study_hash_id': study_id,
      'name': name,
      'authors': authors if authors else [],
      'abstract': abstract
    }

    return {
      'species': species,
      'group_id': group_id,
      'filter_params': {
        'min_counts': min_counts,
        'min_genes': min_genes,
        'max_counts': max_counts,
        'max_genes': max_genes,
        'mt_percentage': mt_percentage / 100
      },
      'study_type': study_type,
      'normalize': input_matrix_type == InputMatrixType.RAW.value,
      'subsample': -1,
      'skip_dimred': skip_dimred,
      'study_info': study_info,
    }


  def submit_study_from_s3(
    self,
    group_id: str,
    batch_info: List[dict] = [],
    study_id: str = None,
    name: str = 'To be detailed',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    input_matrix_type: str = InputMatrixType.NORMALIZED.value,
    study_type: int = StudyType.H5AD.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    mt_percentage: Union[int, float] = None,
    skip_dimred: bool = False
  ):
    """Submit one or multiple scanpy objects.
      Args:
        group_id: ID of the group to submit the data to.
        batch_info: File path and batch name information. Exp: [{"name: "normal": "s3_folder/batch1.h5ad"}, {"name": "cancer": "s3_folder/batch2.h5ad"}]
        study_id: Study ID, if no value is specified, use a random uuidv4 string
        name: Name of the study.
        authors: Authors of the study.
        abstract: Abstract of the study.
        species: Species of the study.
        skip_dirmed: Skip BioTuring pipline if set to True (only appliable when input is a scanpy/seurat object).
        input_matrix_type: If the value of this input is 'normalized',
          then the software will
          use slot 'X' from the scanpy object and does not apply normalization.
          If the value of this input is 'raw',then the software will
          use slot 'raw.X' from thescanpy object and apply log-normalization.
        study_type: The format of the study, supports: mtx, h5, h5ad, rds, tsv/csv.
        min_counts: Minimum number of counts required
          for a cell to pass filtering.
        min_genes: Minimum number of genes expressed required
          for a cell to pass filtering.
        max_counts: Maximum number of counts required
          for a cell to pass filtering.
        max_genes: Maximum number of genes expressed required
          for a cell to pass filtering.
        mt_percentage: Maximum number of mitochondria genes percentage
          required for a cell to pass filtering. Ranging from 0 to 100"""
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      input_matrix_type,
      study_type,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      mt_percentage,
      skip_dimred,
    )

    if study_type == StudyType.MTX_10X.value:
      for i, o in enumerate(batch_info):
        name = o['matrix'].split('/')
        if len(name) == 1:
          o['name'] = f'Batch {i + 1}'
        else:
          o['name'] = name[-2]
    else:
      for i, o in enumerate(batch_info):
        o['name'] = o['matrix'].split('/')[-1]
    data['batch_info'] = {f'Batch_{i}': o for i, o in enumerate(batch_info)}

    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/submit_study_from_s3'),
      body=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return

    common.get_submission_log(
      group_id=group_id, task_id=task_id, https_agent=self.__https_agent, host=self.__host
    )
    return


  def submit_study_from_local(
    self,
    group_id: str,
    batch_info: object,
    study_id: str = None,
    name: str = 'To be detailed',
    authors: List[str] = [],
    abstract: str = '',
    species: str = Species.HUMAN.value,
    input_matrix_type: str = InputMatrixType.NORMALIZED.value,
    study_type: int = StudyType.H5AD.value,
    min_counts: int = None,
    min_genes: int = None,
    max_counts: int = None,
    max_genes: int = None,
    mt_percentage: Union[int, float] = None,
    skip_dimred: bool = False
  ):
    """Submit one or multiple scanpy objects.
      Args:
        group_id: ID of the group to submit the data to.
        batch_info: File path and batch name information. Exp: [{"name: "normal": "local_folder/batch1.h5ad"}, {"name": "cancer": "local_folder/batch2.h5ad"}].
        study_id: Study ID, if no value is specified, use a random uuidv4 string
        name: Name of the study.
        authors: Authors of the study.
        abstract: Abstract of the study.
        species: Species of the study.
        skip_dirmed: Skip BioTuring pipline if set to True (only appliable when input is a scanpy/seurat object).
        input_matrix_type: If the value of this input is 'normalized',
          then the software will
          use slot 'X' from the scanpy object and does not apply normalization.
          If the value of this input is 'raw',then the software will
          use slot 'raw.X' from thescanpy object and apply log-normalization.
        study_type: The format of the study, supports: mtx, h5, h5ad, rds, tsv/csv.
        min_counts: Minimum number of counts required
          for a cell to pass filtering.
        min_genes: Minimum number of genes expressed required
          for a cell to pass filtering.
        max_counts: Maximum number of counts required
          for a cell to pass filtering.
        max_genes: Maximum number of genes expressed required
          for a cell to pass filtering.
        mt_percentage: Maximum number of mitochondria genes percentage
          required for a cell to pass filtering. Ranging from 0 to 100"""

    file_names = []
    files = []
    if study_type == StudyType.MTX_10X.value:
      for o in batch_info:
        file_names.extend([
          f'{o["name"]}matrix.mtx{".gz" if ".gz" in o["matrix"] else ""}',
          f'{o["name"]}features.tsv{".gz" if ".gz" in o["features"] else ""}',
          f'{o["name"]}barcodes.csv{".gz" if ".gz" in o["barcodes"] else ""}'
        ])
        files.extend([
          Path(o['matrix']),
          Path(o['features']),
          Path(o['barcodes'])
        ])
    else:
      for o in batch_info:
        p = Path(o['matrix'])
        o['name'] = p.name
        file_names.append(p.name)
        files.append(p)


    output_dir = common.upload_local(
      file_names, files, group_id, study_type, self.__token, self.__host
    )
    data = self._submit_study(
      group_id,
      study_id,
      name,
      authors,
      abstract,
      species,
      input_matrix_type,
      study_type,
      min_counts,
      min_genes,
      max_counts,
      max_genes,
      mt_percentage,
      skip_dimred,
    )
    data['study_path'] = output_dir
    data['batch_info'] = [o['name'] for o in batch_info]

    submission_status = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/submit_study_from_local'),
      body=data
    )

    task_id = common.parse_submission_status(submission_status)
    if task_id is None:
      return

    common.get_submission_log(
      group_id=group_id, task_id=task_id, https_agent=self.__https_agent, host=self.__host
    )
    return


  def query_genes(
    self,
    species: str,
    study_id: str,
    gene_names: List[str],
    unit: str = UNIT_RAW
  ):
    """
      Query genes expression in study.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study hash ID
        gene_names : list of str
          Querying gene names. If gene_names=[], full matrix will be returned
        unit: str
          Expression unit, UNIT_LOGNORM or UNIT_RAW. Default is UNIT_RAW
      --------------
      Returns
        expression_matrix : csc_matrix
          Expression matrix, shape=(n_cells, n_genes)
    """
    data = {
      'species': species,
      'study_id': study_id,
      'gene_names': gene_names,
      'unit': unit
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/query_genes'),
      body=data
    )
    return common.parse_query_genes_result(result)


  def get_metadata(
    self,
    species: str,
    study_id: str
  ):
    """
      Get full metadata of a study.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study hash ID
      -------------
      Returns
        Metadata: pd.DataFrame
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/get_metadata'),
      body=data
    )
    common.check_result_status(result)
    metadata_dict = result['data']
    metadata_df = pd.DataFrame(metadata_dict)
    return metadata_df


  def get_barcodes(
    self,
    species: str,
    study_id: str
  ):
    """
      Get barcodes of a study.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study hash ID
      -------------
      Returns
        Barcodes: List[str]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/get_barcodes'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def get_features(
    self,
    species: str,
    study_id: str
  ):
    """
      Get features of a study.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study hash ID
      -------------
      Returns
        Features: List[str]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/study/get_features'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def get_all_studies_info_in_group(
    self,
    species: str,
    group_id: str
  ):
    """
      Get info of all studies within group.
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        group_id: str,
          Group hash id (uuid)
      -------------
      Returns
        [
          {
            'uuid': str (uuid),
            'study_hash_id': str (GSE******),
            'study_title': str,
            'created_by': str
          }, ...
        ]
    """
    data = {
      'species': species,
      'group_id': group_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/get_all_studies_info_in_group'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def list_all_custom_embeddings(
    self,
    species: str,
    study_id: str
  ):
    """
      List out all custom embeddings in a study
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study id (uuid)
      -------------
      Returns
        [
          {
          'embedding_id': str,
          'embedding_name': str
          }, ...
        ]
    """
    data = {
      'species': species,
      'study_id': study_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/list_all_custom_embeddings'),
      body=data
    )
    common.check_result_status(result)
    return result['data']


  def retrieve_custom_embedding(
    self,
    species: str,
    study_id: str,
    embedding_id: str
  ):
    """
      List out all custom embeddings in a study
      -------------
      Args:
        species: str,
          Name of species, 'human' or 'mouse' or 'primate'
        study_id: str,
          Study id (uuid)
        embedding_id: str,
          Embedding id (uuid)
      -------------
      Returns
        embedding_arr: np.ndarray
    """
    data = {
      'species': species,
      'study_id': study_id,
      'embedding_id': embedding_id
    }
    result = self.__https_agent.post(
      url=urljoin(self.__host, 'api/v1/retrieve_custom_embedding'),
      body=data
    )
    common.check_result_status(result)
    coord_arr = result['data']['coord_arr']
    coord_shape = result['data']['coord_shape']
    return decode_base64_array(coord_arr, 'float32', coord_shape)
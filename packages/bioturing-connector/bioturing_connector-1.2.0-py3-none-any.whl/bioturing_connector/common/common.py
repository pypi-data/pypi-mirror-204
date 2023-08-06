import time
import requests
import json
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
from scipy import sparse
from urllib.parse import urljoin

from . import decode_base64_array
from . import get_uuid
from .https_agent import HttpsAgent

def check_result_status(result):
  if not result:
    raise ConnectionError('Connection failed')

  if 'status' not in result:
    raise ValueError(result['detail'])

  if result['status'] != 200:
    if 'message' in result:
      raise Exception(f"Something went wrong: {result['message']}")
    else:
      raise Exception('Something went wrong')


def parse_submission_status(submission_status):
  """Parse submission status response
  """
  if not submission_status:
    print('Connection failed')
    return None

  if 'status' not in submission_status:
    print('Internal server error. Please check server log.')
    return None

  if submission_status['status'] != 200:
    if 'message' in submission_status:
      print(f"Submission failed. {submission_status['message']}")
    else:
      print('Submission failed.')
    return None

  return submission_status['data']['id']


def get_submission_log(group_id: str, task_id: str, https_agent: HttpsAgent, host: str):
  last_status = []

  while True:
    submission_log = https_agent.post(
      url=urljoin(host, 'api/v1/get_submission_log'),
      body={'task_id': task_id}
    )
    if not submission_log or 'status' not in submission_log or \
      submission_log['status'] != 200:
      print('Internal server error. Please check server log.')
      break
    if submission_log['data']['status'] == 'ERROR':
      break

    current_status = submission_log['data']['log'].split('\n')[:-1]
    new_status = current_status[len(last_status):]
    if len(new_status):
      print('\n'.join(new_status))

    last_status += new_status
    if submission_log['data']['status'] != 'SUCCESS':
      time.sleep(5)
      continue
    else:
      res = https_agent.post(
        url=urljoin(host, 'api/v1/commit_submission_result'),
        body={
          'group_id': group_id,
          'task_id': task_id
        }
      )
      if not res or 'status' not in res:
        print('Internal server error. Please check server log.')
        break

      if res['status'] != 200:
        if 'message' in res:
          print(f"Connection failed. {res['message']}")
        else:
          print('Connection failed.')
        break

      print('Study submitted successfully!')
      break


def parse_query_genes_result(query_genes_result):
  """Parse query genes result
  """
  check_result_status(query_genes_result)

  indptr = decode_base64_array(query_genes_result['data']['indptr'], 'uint64')
  indices = decode_base64_array(query_genes_result['data']['indices'], 'uint32')
  data = decode_base64_array(query_genes_result['data']['data'], 'float32')
  shape = query_genes_result['data']['shape']
  csc_mtx = sparse.csc_matrix((data, indices, indptr), shape=shape)
  return csc_mtx


def upload_local(file_names, files, group_id, study_type, token, host):
  dir_id = get_uuid()
  output_dir = ''
  for file_name, file in zip(file_names, files):
    total_size = file.stat().st_size
    with tqdm(
      desc=file_name, total=total_size, unit='MB',  unit_scale=True, unit_divisor=1024,
    ) as bar:
      fields = {
        'params': json.dumps({
          'name': file_name,
          'file_id': dir_id,
          'group_id': group_id,
          'study_type': study_type,
        }),
        'file': (file_name, open(file, 'rb'))
      }

      encoder = MultipartEncoder(fields=fields)
      multipart = MultipartEncoderMonitor(
        encoder, lambda monitor: bar.update(monitor.bytes_read - bar.n)
      )
      headers = {
        'Content-Type': multipart.content_type,
        'bioturing-api-token': token
      }
      response = requests.post(
        urljoin(host, 'api/v1/upload'),
        data=multipart,
        headers=headers
      ).json()
      if not response:
        raise Exception('Something went wrong')
      if 'status' not in response or response['status'] != 200:
        raise Exception(response)
      output_dir = response['data']
  return output_dir
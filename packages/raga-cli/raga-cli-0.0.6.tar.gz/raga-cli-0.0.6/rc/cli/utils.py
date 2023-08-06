import logging
import os
from pathlib import Path
from pydoc import stripid
import json
import subprocess
import time
import sys
from rc.utils import DEBUG
from multiprocessing import cpu_count
from pathlib import Path
import pathlib

from rc.utils.request import get_commit_repo, get_config_value_by_key, get_repo_version

logger = logging.getLogger(__name__)

class RctlValidSubprocessError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        logger.error(msg)
        super().__init__(msg, *args)

def fix_subparsers(subparsers):
    subparsers.required = True
    subparsers.dest = "cmd"

def get_git_url(cwd):
    result = subprocess.run('git config --get remote.origin.url', capture_output=True, shell=True, cwd=cwd)    
    stdout = str(result.stdout, 'UTF-8')
    return stripid(stdout)

def get_repo():
    result = subprocess.run('git config --get remote.origin.url', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').split("/")[-1].replace('.git', '')
    return stdout.strip()

def trim_str_n_t(str):
    return ' '.join(str.split())

def get_dvc_data_status(path):
    logger.debug("Compare on PATH : {}".format(path))
    result = subprocess.run('dvc status {}'.format(path), capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8').strip()
    logger.debug(stdout)
    # stdout_line = stdout.splitlines()
    # stdout_line = list(map(trim_str_n_t, stdout_line))
    if stdout.find('modified') != -1:
        return True  
    if stdout.find('Data and pipelines are up to date') != -1:
        return False  
    return False

def get_new_dvc_data_status(path):
    if not get_dvc_data_status(path) and not compare_dot_dvc_file(path):
        return True
    return False

def dataset_current_version(paths, repo):
    current_version = 0 if not get_repo_version(repo) else int(get_repo_version(repo))
    for path in paths:
        if not compare_dot_dvc_file(path):
            return current_version+1
        if get_dvc_data_status(path):
            return current_version+1
    return 1 if not current_version else current_version

def server_repo_commit_status(ids):
    elastic_processes = []
    for id in ids:
        elastic_processes.append(get_commit_repo(id)['check_elastic_process'])
    logger.debug("ELASTIC PROCESS {}".format(elastic_processes))
    return all(elastic_processes)

def current_commit_hash():
    result = subprocess.run('git rev-parse HEAD', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8')
    return stdout.strip()

def current_branch():
    result = subprocess.run('git rev-parse --abbrev-ref HEAD', capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8')
    return stdout.strip()

def branch_commit_checkout(branch,commitId):
    result = subprocess.run('git checkout {0} -b {1}'.format(commitId,branch), capture_output=True, shell=True)    
    stdout = str(result.stdout, 'UTF-8')
    return stdout.strip()



def is_current_version_stable():
    from rc.utils.request import get_commit_version, get_repo_version
    repo = get_repo()
    commit_id = current_commit_hash()
    repo_version = get_repo_version(repo)
    commit_version = get_commit_version(commit_id)
    if not commit_version and not repo_version:
        return True

    if commit_version == repo_version:
        return True
    else:
        logger.debug("Local repo version is not stable")
        print("ERROR: Unable to upload from older version. Please use `rc get` to get the latest version and try again.")
        sys.exit(50)

def get_min_cpu():
    process = 2
    cpu = cpu_count()
    if cpu>4:
        process = int(cpu/4)
    return process        

def get_dir_file(path):
    dvc_file = Path(f'{path}.dvc')
    if not dvc_file.is_file():
        logger.debug("DVC file not found.")
        print("Something went wrong")
        sys.exit(50)
    dvc_read = open(dvc_file, "r")
    md5_dir = ''
    for line in dvc_read.readlines():
        if line.find('- md5') != -1:
            md5_dir = line.split(":")[-1].strip()
    if not md5_dir:
        logger.error(".dir file not found.")
        sys.exit(50)
    return md5_dir

def get_only_valid_dir(dir):
    if not dir.startswith("."):
        return True
    else:
        return False

def trim_slash(str):
    if str.endswith("/"):
        str = str.rsplit("/", 1)[0] 
    return str

def get_all_data_folder():
    directory = os.getcwd()
    dirs = next(os.walk(directory))[1]
    filtered = list(filter(get_only_valid_dir, dirs))
    return filtered

def compare_dot_dvc_file(dir_path):
    dvc_file = Path(f'{dir_path}.dvc')
    if dvc_file.is_file():
        return True
    return False
    
def back_slash_trim(dirs):
    filtered = list(map(trim_slash, dirs))
    return filtered

def valid_git_connection(str, command = None):
    if command and (command.find('git push') != -1 or command.find('git clone')):
        if str.find("Permission denied (publickey)") != -1:            
            print("git@github.com: Permission denied (publickey). Please make sure you have the correct access rights and the repository exists on git.")
            sys.exit(50)   
        elif str.find("ERROR: Repository not found") != -1:            
            print("Repository not found. Please make sure you have the correct access rights and the repository exists on git.")
            sys.exit(50) 
    return True

def run_command_on_subprocess(command, cwd=None, err_skip=False):
    logger.debug(command)
    if cwd:
        result = subprocess.run(command, capture_output=True, shell=True, cwd=cwd)
        stderr = str(result.stderr, 'UTF-8')
        stdout = str(result.stdout, 'UTF-8')        
        if stdout:      
            valid_git_connection(stdout, command)                  
            logger.debug("STD OUT {}".format(stdout)) 

        if stderr:            
            valid_git_connection(stderr, command)    
            logger.debug("STD ERR {}".format(stderr))                
                
    else:
        result = subprocess.run(command, capture_output=True, shell=True)
        stderr = str(result.stderr, 'UTF-8')
        stdout = str(result.stdout, 'UTF-8')        
        if stdout:                        
            valid_git_connection(stdout, command)    
            logger.debug("STD OUT {}".format(stdout)) 

        if stderr:        
            valid_git_connection(stderr, command)        
            logger.debug("STD ERR {}".format(stderr))
                
                

def repo_name_valid(name):
    for c in name:        
        if c == '_':
            raise RctlValidSubprocessError("Error: Bucket name contains invalid characters")
    if len(name) <3 or len(name)>63:
        raise RctlValidSubprocessError("Error: Bucket names should be between 3 and 63 characters long")   
    
def path_to_dict(path):                   
        if path != "./.git":
            d = {'name': os.path.basename(path)}
            if os.path.isdir(path):
                d['type'] = "directory"
                d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir\
        (path)]
            else:
                d['type'] = "file"
            return d 

def upload_model_file_list_json(version):
    import boto3    
    model_file_list = json.loads(json.dumps(path_to_dict('.')))
    CLOUD_STORAGE_BUCKET = get_config_value_by_key('bucket_name')
    CLOUD_STORAGE_DIR = get_config_value_by_key('cloud_storage_dir')
    AWS_SECRET = get_config_value_by_key('remote_storage_secret_key')
    AWS_ACCESS = get_config_value_by_key('remote_storage_access_key')
    repo = get_repo()
    dest = f"{CLOUD_STORAGE_DIR}/{repo}/model_files/{version}.json"
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS, aws_secret_access_key=AWS_SECRET)
    with open(f'{version}.json', 'w', encoding='utf-8') as cred:    
        json.dump(model_file_list, cred, ensure_ascii=False, indent=4)            
    s3.upload_file(f'{version}.json', CLOUD_STORAGE_BUCKET, dest)
    pathlib.Path(f'{version}.json').unlink(missing_ok=True)
    
def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        ExceptionToCheck (Exception): the exception to check. When an exception of this type is raised, the function will be retried.
        tries (int): number of times to try before giving up.
        delay (int): initial delay between retries in seconds.
        backoff (int): backoff multiplier (e.g. value of 2 will double the delay each retry).

    Example Usage:
    ```
    @retry(Exception, tries=4, delay=3, backoff=2)
    def test_retry():
        # code to retry
    ```
    """
    logger.debug("RETRYING")
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    print(f"Got exception '{e}', retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry
    return deco_retry
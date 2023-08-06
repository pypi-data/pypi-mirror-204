from datetime import timedelta
import logging
import threading
import time

from rc.cli.utils import compare_dot_dvc_file, run_command_on_subprocess
from timeit import default_timer as timer
from rc.cli.utils import *
from rc.utils.request import is_repo_lock, update_repo_commit_id, update_repo_lock, insert_repo_commit, get_repository

logger = logging.getLogger(__name__)
repo_commit_ids = []
pool_time = 10

def dir_add(path):
    start = timer()
    if compare_dot_dvc_file(path):
        run_command_on_subprocess("dvc commit {0} -f".format(path))
    else:
        run_command_on_subprocess("dvc add {0}".format(path))
    run_command_on_subprocess("git add {0}.dvc".format(path))
    logger.debug('DVC ADD TIME {0}'.format(timedelta(seconds=timer()-start)))

def dir_upload(paths):
    start = timer()
    run_command_on_subprocess("dvc push {0}".format(' '.join(paths)))
    logger.debug('DVC PUSH TIME {0}'.format(timedelta(seconds=timer()-start)))   

@retry(Exception, tries=4, delay=3, backoff=2)
def dataset_upload(paths,message,repo,current_version):
    is_current_version_stable()   
    print("Files uploading...")   
    paths = back_slash_trim(paths)

    for path in paths:
        dir_add(path)
    dir_upload(paths)
    for path in paths:     
        md5_dir = get_dir_file(path)          
        request_payload = {
            "folder": path,
            "commit_message" : message,
            "repo" : repo,
            "dir_file":md5_dir,
            "version":current_version,
            "commit_id":"",
        }   
        commit_id = insert_repo_commit(json.dumps(request_payload))
        repo_commit_ids.append(commit_id['id'])
        logger.debug("Data upload for {}".format(path))
    
    stop_checking_elastic_process = False
    while not stop_checking_elastic_process:
        stop_checking_elastic_process = server_repo_commit_status(repo_commit_ids)
        if not stop_checking_elastic_process:
            time.sleep(pool_time)
    return True

def model_upload(message, repo):
    update_repo_lock(repo, json.dumps({"locked":True}))
    print("Model files uploading...")
    branchName = current_branch()
    commit_hash = current_commit_hash()
    branchName = current_branch()
    request_payload = {
                "commit_message" : message,
                "repo" : repo,
                "commit_id":commit_hash,
                "branch":branchName
            }  
    upload_model_file_list_json(commit_hash)
    insert_repo_commit(json.dumps(request_payload))
    logger.debug("Data upload for branch {0} and {1} ".format(branchName,commit_hash ))
    print("Model files uploaded successfully")

def make_repo_lock(stop_event):
    logger.debug("START HTTP THREAD")
    repo = get_repo() 
    while not stop_event.is_set():
        logger.debug("REPO LOCKING")
        update_repo_lock(repo, json.dumps({"locked":True}))
        time.sleep(pool_time)

def make_repo_commit(message):
    if len(repo_commit_ids):
        run_command_on_subprocess("git commit -m '{}' -a".format(message), None, True)
        run_command_on_subprocess("git push", None, True)
        for id in repo_commit_ids:     
            commit_hash = current_commit_hash()
            request_payload = {
                "id" : id,
                "commit_id":commit_hash,
            }   
            update_repo_commit_id(json.dumps(request_payload))
            logger.debug("Data committed")
    else:
        logger.debug("Repo IDs not found.")
        print("Server not responding")
        sys.exit()
    print("Files uploaded successfully")

def put(args):
    start = timer()
    message = args.message      
    paths = args.path   
    repo = get_repo()       
    current_version = dataset_current_version(paths, repo)
    # print("VERSION", current_version)
    # print("CHECK ELASTIC PROCESS", server_repo_commit_status(repo_commit_ids))
    # return

    tag = get_repository(repo)
    is_repo_lock(repo)
    
    if tag == "dataset":
        # Create an Event object
        stop_event = threading.Event()
        # Create a thread for making an HTTP request
        http_thread = threading.Thread(target=make_repo_lock, args=(stop_event,))
        http_thread.start() 
        try:
            if dataset_upload(paths,message,repo, current_version):
                # Set the stop event
                stop_event.set()
                update_repo_lock(repo, json.dumps({"locked":False}))
        except Exception as e:
            # Set the stop event
            stop_event.set()
            update_repo_lock(repo, json.dumps({"locked":False}))
            print("Something went wrong.")
            logger.exception(e)
            sys.exit()
        # Start both threads
        
        # Wait for both threads to finish
        http_thread.join()
        make_repo_commit(message)
        
    elif tag == "model":
        model_upload(message, repo)
        
    update_repo_lock(repo, json.dumps({"locked":False}))
    logger.debug('TOTAL UPLOAD TIME {0}'.format(timedelta(seconds=timer()-start)))
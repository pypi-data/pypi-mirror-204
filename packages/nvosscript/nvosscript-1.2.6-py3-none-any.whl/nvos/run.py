import subprocess
from nvos import login, file, utils, remote
import os
import time
import logging
import concurrent.futures
import platform
import json
import shutil

# 导入全局日志记录器
logger = logging.getLogger()
all_workspace_path = {}


def command_init():
    status = login.check_login_status()
    if not status:
        print("Please login first. you could use login command to login this script")
        return
    workspace_path, success = utils.check_workspace_exist(os.getcwd())

    sub_workspace_path, flag = utils.check_subdirectory_workspace_exist(os.getcwd())
    if flag:
        print(
            f"The subdirectory has already bean initialized, don't repeat execute init command, this subdirectory:{sub_workspace_path}")
        try:
            shutil.rmtree(os.path.join(os.getcwd(), ".ndtc"))
        except OSError as e:
            print(f"Error: {os.path.join(os.getcwd(), '.ndtc')} : {e.strerror}")
        return

    print("please wait one minute.........")
    try:
        file.init_work_space(workspace_path)
    except Exception as e:
        logger.exception("command_init")
        print(f"Error: {e}")


def command_async(type=None):
    global all_workspace_path
    workspace_path, success = common_verify()
    if not success:
        return
    all_workspace_path.update({workspace_path: workspace_path})
    if platform.system() == 'Windows':
        with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace")), "w") as f:
            f.write(json.dumps(all_workspace_path))
        return
    # 在运行时执行
    import daemon
    proc1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'ndtc'], stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = proc2.communicate()
    number = 0
    for line in out.splitlines():
        if 'ndtc' in str(line).lower() and 'python' in str(line).lower():
            number = number + 1
    if number > 1:
        return
    preserve_fds = [handler.stream for handler in logger.handlers]
    with daemon.DaemonContext(files_preserve=preserve_fds):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                for temp in all_workspace_path.keys():
                    logger.info("command_async current run workspace is " + temp)
                    executor.submit(execute_async, temp)
                time.sleep(10)


def execute_async(workspace_path):
    file.push_data_to_cloud(workspace_path)
    file.pull_data_from_cloud(workspace_path)


def command_pull():
    workspace_path, success = common_verify()
    if not success:
        return
    print("please wait one minute.........")
    try:
        file.pull_data_from_cloud(workspace_path)
    except Exception as e:
        logger.exception("command_pull")
        print(f"Error: {e}")


def command_push():
    workspace_path, success = common_verify()
    if not success:
        return
    print("please wait one minute.........")
    try:
        file.push_data_to_cloud(workspace_path)
    except Exception as e:
        logger.exception("command_push")
        print(f"Error: {e}")


def common_verify():
    workspace_path, success = utils.check_workspace_exist(os.getcwd())
    if not success:
        print(
            "Please executor this command that your before executor init command of directory or subdirectory, or you can  executor init this directory")
        return workspace_path, False
    status = login.check_login_status()
    if not status:
        print("Please login first. you could use login command to login this script")
        return workspace_path, False
    return workspace_path, True


def command_env(env=None):
    if env is None:
        result = remote.get_current_env()
        print(f"current env:{result['env']} this cloud linked:{result['tip']}")
        return

    remote.switch_env(env)
    workspace_env = []
    if os.path.exists(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace_env"))):
        with open(os.path.expanduser(os.path.join("~", '.ndtcrc', "workspace_env")), 'r') as f:
            for line in f:
                workspace_env.append(line.strip())
        for item in workspace_env:
            try:
                os.remove(os.path.join(item, ".ndtc", 'offset'))
                os.remove(os.path.join(item, ".ndtc", 'project_space'))
                os.remove(os.path.join(item, ".ndtc", 'config'))
            except OSError:
                logger.exception("command_env")


def command_upload():
    file_path = os.path.expanduser(os.path.join('~', 'ndtc.log'))
    remote.upload_logger_file(file_path)
import json
import os
import requests
import time
import platform
import signal
import subprocess
import psutil
from typing import Optional, Dict, Any, List
from multiprocessing import Process

processes = {}
def start(widget_infos):
    for widget_info in widget_infos:
        widget = json.dumps(widget_info)
        p = Process(target=monitor_process, args=(widget,))
        processes[widget_info['widget']] = p
        print("start monitor process");
        p.start()
        print("start monitor process successfully.");


def stop():
    for p in processes.values():
        p.terminate()
def update_progress(widget_info:Dict[str, Any], taskid: int, progress: float):
    widget_info['taskid'] = taskid;
    widget_info['progress'] = progress;
def can_restart(widget_info:Dict[str, Any]):
        return widget_info['last_request_time'] is not None and (time.time() - self.last_request_time) > 20

def monitor_process(widget: str):
    widget_info = json.loads(widget)
    try:
        while True:
            if widget_info['widget'] == 'SD' and 'port' in widget_info:
                task_info = get_sd_task_info(widget_info)
                if task_info is not None:
                    update_progress(widget_info, task_info['taskid'], task_info['progress'])
                    if task_info['state'] != 0:
                        if can_restart(widget_info) and \
                            task_info['taskid'] == widget_info['taskid'] and \
                            task_info['progress'] == widget_info['progress']:
                            kill_process(widget_info)
                            start_process(widget_info)

                            print(f"restart widget:{widget_info['widget']}")
                        else:
                            update_progress(widget_info, task_info['taskid'], task_info['progress'])
                else:
                    pid = get_pid_using_port(widget_info['port'])
                    if pid is not None:
                        kill_process(widget_info)
                        start_process(widget_info)
                        print(f"restart widget:{widget_info['widget']}")
                    else:
                        start_process(widget_info)
                        print(f"start widget:{widget_info['widget']}")
            else:
                if 'pid' in widget_info and widget_info['pid']:
                    pid = widget_info['pid']
                else:
                    pid = find_pid_by_name(widget_info['name'])
                if pid is not None:
                    cpu_percent = get_cpu_percent(pid)
                    status = get_process_status(pid)
                    memory_percent = get_memory_percent(pid)
                    memory_percent *= 100
                    io_counters = get_io_counters(pid)
                    print("PID\tNAME\tSTATUS\tMEMORY(%)")
                    print(f"{pid}\t{widget_info['name']}\t{status}\t{memory_percent}")
                    if cpu_percent is not None and cpu_percent > 90 and \
                        status == "SLEEPING" and memory_percent is not None and memory_percent > 90 and \
                        io_counters is not None and io_counters.read_bytes > 1000000:
                        kill_process(widget_info)
                        start_process(widget_info)

                    elif status == "ZOMBIE" or status == "STOPPED":
                        kill_process(widget_info)
                        start_process(widget_info)
            print(f"{widget_info['widget']} sleep");
            time.sleep(10)
    except Exception as e:
        print(e)
        
def get_sd_task_info(widget_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    url = f"http://localhost:{widget_info['port']}/mecord/state"
    try:
        response = requests.get(url, timeout=15)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    if response.status_code == 200:
        try:
            return json.loads(response.content)
        except json.JSONDecodeError as e:
            print(e)
    else:
        print(f"Failed to get task info from {url}, status code: {response.status_code}")
    return None
        
def start_process(widget_info: Dict[str, Any]):
    if widget_info['path'] is not None and os.path.exists(widget_info['path']):
        launch_path = os.path.join(widget_info['path'], "launch.py")
        if os.path.exists(launch_path):
            print(f"starting widget {widget_info['widget']}...")
            try:
                if platform.system() == 'Windows':
                    subprocess.Popen(['python', launch_path])
                elif platform.system() == 'Linux':
                    subprocess.Popen(['python', launch_path])
                else: # macOS
                    subprocess.run(['python', launch_path])
            except subprocess.CalledProcessError:
                pass
            except Exception as e:
                pass

        else:
            print(f"Failed to find launch script for process {widget_info['name']}")
    else:
        print(f"Invalid path for process {widget_info['name']}")

def kill_process(widget_info: Dict[str, Any]):
    if 'name' in widget_info and widget_info['name']:
        pid = find_pid_by_name(widget_info['name'])
    elif 'port' in widget_info and widget_info['port']:
        pid = get_pid_using_port(widget_info['port'])
    if pid is not None:
        try:
            if platform.system() == 'Windows':
                os.kill(pid, signal.SIGTERM)
            elif platform.system() == 'Linux':
                os.kill(pid, signal.SIGTERM)
            else: # macOS
                subprocess.run(f"kill {pid}", shell=True)
        except OSError:
                    pass
            
def find_pid_by_name(process_name: Optional[str]) -> Optional[int]:
    if process_name is None:
        return None
    processes = list(psutil.process_iter(['name']))
    for proc in processes:
        if proc.info['name'] == process_name:
            return proc.pid
    return None

def get_pid_using_port(port: int):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            try:
                return conn.pid
            except psutil.AccessDenied:
                pass
    return None

def get_cpu_percent(pid: int) -> Optional[float]:
    try:
        process = psutil.Process(pid)
        return process.cpu_percent(interval=1)
    except psutil.NoSuchProcess:
        return None

def get_process_status(pid: int) -> Optional[str]:
    try:
        if OS == 'Linux':
            status = os.stat(f"/proc/{pid}").st_state
            if status == "R":
                return 'RUNNING'
            elif status == "S" or status == 'D':
                return 'SLEEPING'
            elif status == "T":
                return 'STOPPED'
            elif status == "Z":
                return 'ZOMBIE'
            else:
                return 'UNKNOWN'
        else:
            process = psutil.Process(pid)
            pstatus = process.status()
            if pstatus == psutil.STATUS_RUNNING:
                return 'RUNNING'
            elif pstatus == psutil.STATUS_SLEEPING:
                return 'SLEEPING'
            elif pstatus == psutil.STATUS_STOPPED:
                return 'STOPPED'
            elif pstatus == psutil.STATUS_ZOMBIE:
                return 'ZOMBIE'
            else:
                return 'UNKNOWN'
    except (FileNotFoundError, psutil.NoSuchProcess):
        return 'EXITED'
    except Exception as e:
        print(f'Unexpected error while checking process {pid} status: {str(e)}')
        return 'UNKNOWN'

def get_memory_percent(pid: int) -> Optional[float]:
    try:
        process = psutil.Process(pid)
        return process.memory_percent()
    except psutil.NoSuchProcess:
        return None

def get_io_counters(pid: int) -> Optional[psutil._common.snetio]:
    try:
        process = psutil.Process(pid)
        return process.io_counters()
    except psutil.NoSuchProcess:
        return None
            
            
# if __name__ == '__main__':
#     process_infos = [
#         {"widget": "a", "port": 7890, "name": "test_process1", "path": "/path/to/launch1"},
#         {"widget": "SD", "port": 7860, "name": "test_process2", "path": "/path/to/launch2"},
#         {"widget": "b", "port": 7900, "name": "test_process3", "path": "/path/to/launch3"}
#     ]

#     start(process_infos);
#     # monitor = ProcessMonitor(process_infos)
#     # monitor.start()
#     time.sleep(600) # 运行 10 分钟
#     stop()
# -*- coding: utf-8 -*-
"""
@File    : task.py
@Time    : 2024/05/09 09:21:45
@Author  : WHY
@Version : 1.0
@Desc    : 定时任务
"""
from __future__ import annotations

import multiprocessing
from datetime import datetime, timedelta

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler


def job1():
    print('job1')


def job2():
    print('job2')


TASK_DICT: dict = {
    'task1': {
        'switch': True,
        'job1': {
            'switch': True,
            'etc': None,
            'func': job1,
            'args': None,
            'kwargs': None,
            'trigger': 'interval',
            'seconds': 3,
            'max_instances': 3,
            'next_run_time': datetime.now() + timedelta(seconds=3),
            # 'executor': 'process',
        },
        'job2': {
            'switch': True,
            'etc': None,
            'func': job2,
            'args': None,
            'kwargs': None,
            'trigger': 'interval',
            'seconds': 5,
            'max_instances': 3,
            'next_run_time': datetime.now() + timedelta(seconds=5),
            'executor': 'process',
        },
    },
    'task2': {
        'switch': True,
        'job1': {
            'switch': True,
            'etc': None,
            'func': job1,
            'args': None,
            'kwargs': None,
            'trigger': 'interval',
            'seconds': 10,
            'max_instances': 3,
            'next_run_time': datetime.now() + timedelta(seconds=10),
        },
        'job2': {
            'switch': True,
            'etc': None,
            'func': job2,
            'args': None,
            'kwargs': None,
            'trigger': 'interval',
            'seconds': 10,
            'max_instances': 3,
            'next_run_time': datetime.now() + timedelta(seconds=10),
        },
    },
}


def task_run(task_dict: dict[str, str | dict[str]], **kwargs):
    """
    ~: 定时任务启动

    Parameters
    ----------
    - task_dict: dict[str, str | dict[str]] ; 任务字典
    - kwargs: add_job里func部分参数
    """
    # 定时任务调度器字典
    scheduler: dict[str, BackgroundScheduler] = {}
    # 遍历任务字典
    for task_name, task in task_dict.items():
        # 任务调度器开关
        if task.pop('switch'):
            # 添加任务调度器到字典
            scheduler[task_name] = BackgroundScheduler(
                timezone='Asia/Shanghai',
                # 添加进程执行器
                executors={
                    'process': ProcessPoolExecutor(
                        max_workers=multiprocessing.cpu_count()
                    )
                },
            )
            # 遍历作业字典
            for job_name, job in task.items():
                job: dict
                # 作业开关
                if job.pop('switch'):
                    # 添加作业额外参数
                    etc: tuple | None
                    if (etc := job.pop('etc')) is not None:
                        if job.get('kwargs') is None:
                            job['kwargs'] = {e: kwargs[e] for e in etc}
                        else:
                            for e in etc:
                                job['kwargs'][e] = kwargs[e]
                    # 添加作业到调度器
                    scheduler[task_name].add_job(name=job_name, **job)
            # 任务启动
            scheduler[task_name].start()


if __name__ == '__main__':
    import time

    task_run(TASK_DICT)
    while True:
        time.sleep(100)

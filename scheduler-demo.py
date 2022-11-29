# !coding:utf-8

"""
展示定时任务模块 apscheduler 的用法，主要包含以下知识点

1. 定时任务器怎么使用
2. 异步任务怎么添加
3. 同步任务和异步任务线程是否会冲突(不冲突)
"""

import time
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s [line:%(lineno)d  thread:%(thread)d] %(message)s',
                    level=logging.INFO)


async def test1(t):
    await asyncio.sleep(t)
    logging.info(f'Tick! test1 have sleep {t} seconds.')


def test2(t):
    time.sleep(t)
    logging.info(f'Tick! test2 have sleep {t} seconds.')


async def tasks_logic():
    task_list = [
        test1(1),
        # test1(3)
    ]
    tasks = []
    for task in task_list:
        tasks.append(
            asyncio.ensure_future(task)
        )
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tasks_logic, name='异步任务1', trigger='interval', seconds=5, replace_existing=True)
    scheduler.add_job(test2, args=(1,), name='同步任务1', trigger='interval', seconds=10, replace_existing=True)
    scheduler.add_job(test2, args=(1,), name='同步任务2', trigger='interval', seconds=10, replace_existing=True)
    scheduler.start()
    logging.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

# !coding:utf-8
import asyncio
import aiohttp
import functools
import logging

logging.basicConfig(format='%(asctime)s [line:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.DEBUG)

"""
用一个简单的例子来展示 python 的异步操作, 主要包含以下知识点：

1. 如何等待
2. 如何调用多个子任务
3. 如何取得子任务的返回值

注：如果有了异步方法，那么方法中的所有操作都要是异步的，否则会让异步失效。
"""


async def wait_task(second=3):
    await asyncio.sleep(second)


async def get_dog_pic(session, task_id):
    """
    随机获取狗狗图片
    """
    logging.info(f"开始任务 {task_id}")
    url = 'https://shibe.online/api/shibes?count=1'
    async with session.get(url=url) as r:
        json_response = await r.json()
        if r.status != 200:
            return False, f"failed: request {url} return status: {r.status}"
        else:
            return True, json_response


def task_callback(task_id, res):
    logging.info(f"任务 {task_id} 返回的值·{res.result()}")


async def main():
    tasks = []
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=64, ssl=False)
    ) as session:
        for task_id in range(1, 4):
            task = asyncio.create_task(
                get_dog_pic(session, task_id)
            )
            task.add_done_callback(
                functools.partial(task_callback, task_id)
            )
            tasks.append(task)
        # 下面这行没什么意思，就是插入个等待，所有任务执行完的时间长短，取决于最耗时任务的执行时间
        tasks.append(wait_task(3))
        res = await asyncio.gather(*tasks)
        logging.info(f"所有任务完成，一起返回的结果: {res}")


if __name__ == '__main__':
    asyncio.run(main())

    # 上面的 asyncio.run 等价于下面两行
    # future = asyncio.ensure_future(main())
    # asyncio.get_event_loop().run_until_complete(future)
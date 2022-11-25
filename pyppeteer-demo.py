# !coding:utf-8

import asyncio
from pyppeteer import launch
import logging

logging.basicConfig(format='%(asctime)s [line:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.INFO)

"""
pyppeteer 的一个简单示例，包含以下步骤

1. 打开百度首页，获取到今日热搜
2. 在搜索框输入 "卡塔尔"
3. 点击 "搜索" 按钮，进入搜索首页
4. 获取前两页的搜索结果并输出

文档: https://miyakogi.github.io/pyppeteer/reference.html

模糊查找文本  "//a[contains(text(),'糯')]"
模糊查找属性  "//input[contains(@id,'xx')]"
开头查找属性 "//input[starts-with(@id,'xx')]"
"""


async def main():
    browser = await launch(headless=False, slowMo=30)
    try:
        page = await browser.newPage()
        await page.goto('https://www.baidu.com/')
        hot_searches = await page.evaluate("""() => {
            const hot_searches = [];
            const spans = document.querySelectorAll(".title-content-title")
            spans.forEach((element) => {
                hot_searches.push(element.innerHTML);
            });
            return hot_searches;  
        }""")
        logging.info(f"今日热搜：{hot_searches}")
        await page.type("#kw", "卡塔尔", {'delay': 100})
        await page.waitFor(1000)
        await page.click('#su')
        # await page.screenshot({'path': './baidu.png', 'quality': 50, 'fullPage': True})
        for i in range(1, 3):
            await page.waitForNavigation({'waitUntil': 'load'})
            aa = await page.Jx('//div[@tpl="se_com_default"]/div/div/h3/a')
            logging.info(f"--- 第{i}页的搜索结果: ---")
            for a in aa:
                title_str1 = await (await a.getProperty('textContent')).jsonValue()
                logging.info(title_str1)

            await page.waitFor(1000)
            await page.click('.n')

    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())

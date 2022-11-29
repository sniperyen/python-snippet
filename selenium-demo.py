# coding=utf-8
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import logging
logging.basicConfig(format='%(levelname)s: %(asctime)s [line:%(lineno)d  thread:%(thread)d] %(message)s',
                    level=logging.INFO)


def random_device_name():
    device_names = ['Galaxy S5', 'iPhone 6/7/8 Plus']
    return random.choice(device_names)

def random_mobile_metric():
    mobileMetrics = [
        (360, 780, 2.0),
        (360, 780, 3.0),
    ]
    return random.choice(mobileMetrics)

def random_ua(is_mobile=False):
    mobileAgents = [
        "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
        "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    ]

    pcAgents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    ]
    if is_mobile:
        return random.choice(mobileAgents)
    else:
        return random.choice(pcAgents)


def get_opts(is_visible=False, host_port='', user_agent='', is_mobile=False, user_data_dir=False, *args, **kwargs) -> Options:
    # 启动参数列表:  https://peter.sh/experiments/chromium-command-line-switches/
    # selenium 启动 Chrome配置参数问题 https://zhuanlan.zhihu.com/p/60852696
    opts = Options()
    if not is_visible:
        opts.add_argument("log-level=3")
        # 浏览器不提供可视化页面. linux 下如果系统不支持可视化不加这条会启动失败
        opts.add_argument("--headless")
        # 以最高权限运行
        opts.add_argument('--no-sandbox')

    # 添加代理服务
    if host_port:
        # 代理软件使用方法: browsermob-proxy
        opts.add_argument('--proxy-server=http://%s' % host_port)

    # 添加 user-agent
    if not user_agent:
        # https://www.jianshu.com/p/9453579154e3
        # 普通格式: User-Agent: Mozilla/<version> (<system-information>) <platform> (<platform-details>) <extensions>
        user_agent = random_ua(is_mobile)

    # 手机浏览器
    if is_mobile:
        # https://zhuanlan.zhihu.com/p/28710941
        # mobileEmulation = {'deviceName': random_device_name()}
        oneMetrics = random_mobile_metric()
        mobileEmulation = {
            "deviceMetrics": {"width": oneMetrics[0], "height": oneMetrics[1], "pixelRatio": oneMetrics[2]},
            "userAgent": user_agent}
        opts.add_experimental_option('mobileEmulation', mobileEmulation)
    else:
        opts.add_argument('user-agent="%s"' % user_agent)

    # 手动指定浏览器位置
    if 'binary_location' in kwargs:
        opts.binary_location = kwargs.get('binary_location')

    # 设置开发者模式启动，该模式下 window.navigator.webdriver 属性为正常值，否则会被网站监测到
    opts.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 最大化运行（全屏窗口）
    opts.add_argument("--start-maximized")
    # # 指定浏览器分辨率
    # opts.add_argument('window-size=1920x3000')
    # 解决跨域问题
    opts.add_argument("--disable-web-security")
    # # 禁用浏览器正在被自动化程序控制的提示
    # opts.add_argument("--disable-infobars")
    # 谷歌文档提到需要加上这个属性来规避bug
    opts.add_argument("--disable-gpu")
    # 解决混合内容问题，不看到不安全内容的提示
    opts.add_argument("--allow-running-insecure-content")

    #打开带浏览器插件的浏览器页面（需要关闭所有谷歌浏览器页面，不然会出错）
    #需要多开时，复制/User Data/ 文件夹重命名为其它名字，然后修改这边配置
    # opts.add_argument("--user-data-dir="+r"C:/Users/admin/AppData/Local/Google/Chrome/User Data/")
    # opts.add_argument("--user-data-dir="+r"C:/Users/asus/AppData/Local/Google/Chrome/User Data/")
    if user_data_dir:
        opts.add_argument("--user-data-dir="+r"C:/Users/admin/AppData/Local/Google/Chrome/User Data/")
        # opts.add_argument("--user-data-dir="+r"C:/Users/asus/AppData/Local/Google/Chrome/User Data/")
    # # 隐藏滚动条, 应对一些特殊页面
    # opts.add_argument('--hide-scrollbars')
    # # 不加载图片, 提升速度
    # opts.add_argument('blink-settings=imagesEnabled=false')

    # # 添加扩展应用
    # opts.add_extension()
    # opts.add_encoded_extension()
    #
    # # 设置调试器地址
    # opts.debugger_address()
    #
    # # 添加crx插件
    # opts.add_extension('d:\crx\AdBlock_v2.17.crx')
    #
    # # 禁用JavaScript
    # opts.add_argument("--disable-javascript")
    #
    #
    # # 禁用浏览器弹窗
    # prefs = {
    #     'profile.default_content_setting_values': {
    #         'notifications': 2
    #     }
    # }
    # opts.add_experimental_option('prefs', prefs)

    return opts


def get_driver(opts, executable_path='', page_load_timeout=30, *args, **kwargs) -> webdriver.Chrome:
    capabilities = webdriver.DesiredCapabilities.CHROME
    # executable_path = kwargs.get('executable_path')
    if not executable_path:
        _driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opts,
                                   desired_capabilities=capabilities)
    else:
        _driver = webdriver.Chrome(executable_path=executable_path, chrome_options=opts,
                                   desired_capabilities=capabilities)

    _driver.implicitly_wait(5)
    _driver.set_page_load_timeout(page_load_timeout)
    return _driver


if __name__ == '__main__':
    opts = get_opts(is_visible=True, is_mobile=False)
    driver = get_driver(opts)
    try:
        url = "https://abc.requestcatcher.com/test"
        driver.get(url)
        print(driver.title)
        time.sleep(20000)
    finally:
        driver.quit()

__author__ = 'jarek tanistra'
from lib.configuration_reader import load_configuration_from_file
from appium import webdriver
import os

def create_driver(platform, reinstallApp=True):
    """
    :param platform: set platform for testing - iOS or Android
    :return: driver
    """
    platform = platform.upper()
    if platform == 'ANDROID':
        CONFIG_ANDROID = load_configuration_from_file('android_config.json')
        desktopFile = os.path.expanduser(CONFIG_ANDROID['APP_PATH'])
        app = os.path.join(desktopFile, CONFIG_ANDROID['APP_NAME'])
        desired_caps = {}
        desired_caps['platformName'] = CONFIG_ANDROID['PLATFORM_NAME']
        desired_caps['platformVersion'] = CONFIG_ANDROID['PLATFORM_VERSION']
        desired_caps['deviceName'] = CONFIG_ANDROID['DEVICE_NAME']
        if reinstallApp:
            desired_caps['app'] = app
        desired_caps['appPackage'] = CONFIG_ANDROID['APP_PACKAGE']
        desired_caps['appActivity'] = CONFIG_ANDROID['APP_ACTIVITY']
        print("[DEBUG]: Desired capabilities: ", desired_caps)
        driver = webdriver.Remote(CONFIG_ANDROID['REMOTE'], desired_caps)
    elif platform == 'IOS':
        CONFIG_IOS = load_configuration_from_file('config_iOS.json')
        desktopFile = os.path.expanduser(CONFIG_IOS['APP_PATH'])
        app = os.path.join(desktopFile, CONFIG_IOS['APP_NAME'])
        absApp = os.path.abspath(app)
        driver = webdriver.Remote(
            command_executor=CONFIG_IOS['REMOTE'],
            desired_capabilities={
                'app': app,
                'deviceName': CONFIG_IOS['DEVICE_NAME'],
                'platformName': CONFIG_IOS['PLATFORM_NAME'],
                'platformVersion': CONFIG_IOS['PLATFORM_VERSION'],
                'udid': CONFIG_IOS['UDID'],
                'orientation': CONFIG_IOS['ORIENTATION']
            })
    else:
        raise AssertionError('[ERROR] Available platforms: iOS or Android only')
    return driver

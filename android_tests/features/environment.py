from lib.appium_starter import start_appium, stop_appium
# from lib.create_driver import create_driver
from lib.create_driver import create_driver
from lib.adb_commands import adb_shell_screenrecord, adb_shell_screenrecord_stop, adb_pull, adb_logcat_android

def before_all(context):
    start_appium()

def before_feature(context, feature):
    create_driver('android', reinstallApp=True)
    print("Before feature\n")

#Scenario level objects are popped off context when scenario exits
def before_scenario(context,scenario):

    adb_shell_screenrecord('/sdcard/Download')
    print("Before scenario\n")

def after_scenario(context,scenario):
    context.driver.quit()
    print("After scenario\n")

def after_feature(context,feature):
    print("\nAfter feature")

def after_all(context):
    print("Executing after all")
    stop_appium()


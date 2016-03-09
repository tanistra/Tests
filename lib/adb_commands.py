import subprocess
import os
import signal


def _execute_command(cmd, *args):
    """
    Internal function execute adb commands in terminal
    :param cmd: adb command
    :param args: options
    """
    cmd = ''.join(cmd) + ' '.join(args)
    output = subprocess.getstatusoutput(cmd)
    print('INFO: adb command: "%s %s " executed' % (cmd, str(args)))
    if output[0]:
        raise AssertionError('Non zero status output. \n %s' % output[1])
    print('INFO: ','adb command output:', output[1])
    return output[1]


def _execute_subprocess(cmd):
    subprocess.Popen(cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, preexec_fn=os.setsid)


def _kill_subprocess():
    pid = os.getpid()
    try:
        os.kill(pid, signal.SIGINT)
    except (KeyboardInterrupt, SystemExit):
        print('Subprocess killed')


def adb_install(apk, *options):
    """
    :param apk: path to the app
    :param options:
    -l test.apk forward lock application
    -r test.apk replace existing application
    -t test.apk allow test packages
    -s test.apk install application on sdcard
    -d test.apk allow version code downgrade
    -p test.apk partial application install
    """
    cmd = ('adb install ', *options, apk)
    cmd_output = _execute_command(cmd)
    if 'Failure' in cmd_output:
        raise AssertionError(cmd_output)


def adb_uninstall(package, option = None):
    """
    Uninstall app by package
    :param package: app package
    :param option: default disabled
    -k keep the data and cache directories around
    """
    cmd_output = _execute_command('adb uninstall ', package)
    if 'Failure' in cmd_output:
        raise AssertionError(cmd_output)


def logcat_android(log_level ='v', tags_list=''):
    """
    returns android logs to txt file in logs directory. Logs can be filtred by tags or by app package.
    :param tags_list: can be string in specific format: '"TAG1","TAG2","TAG3"'
    :param log_level:
    *:V lowest priority, filter to only show Verbose level
    *:D filter to only show Debug level
    *:I filter to only show Info level
    *:W filter to only show Warning level
    *:E filter to only show Error level
    *:F filter to only show Fatal level
    *:S Silent, highest priority, on which nothing is ever printed
    """
    file = "mesh_tool_system_logs.log"
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/logs/' + file
    U_COMMAND = 'adb logcat -s ' + str(tags_list) + ' > ' + path
    print('INFO: adb command: ' + str(U_COMMAND))
    print('INFO: Start android log to file: ' + str(path))
    _execute_subprocess(U_COMMAND)


def adb_shell_clear(package):
    """
    Deletes all data associated with a package. Clearing app data, cache.
    :param package: appPackage
    """
    _execute_command('adb shell pm clear ', package)


def logcat_android_stop():
    """
    Stops android adb logcat
    """
    _kill_subprocess()
    print('INFO: Stop android logs')


def adb_devices():
    """
    Prints a list of all attached emulator/device
    In response, return serial number and state
    e4b25377        device
    emulator-5554  device
    """
    _execute_command('adb devices')


def adb_kill_server():
    """
    terminates the adb server process
    """
    _execute_command('adb kill-server')


def adb_pull(path_to_file, destination_path):
    """
    Download a specified file from an emulator/device to your computer.
    :param path_to_file: path to file to file in android storage
    :param destination_path: path to
    :return:
    """
    _execute_command('adb pull ', path_to_file, destination_path)


def adb_push(path_to_file, android_destination):
    """
    Upload a specified file from your computer to an emulator/device. Copies <local/path/to/file.apk to /path/android/dir directory.
    :param path_to_file:
    :param android_destination:
    """
    _execute_command('adb push ', path_to_file, android_destination)


def adb_shell_screencap(file):
    """
    taking a screenshot of a device display.
    :param file: android destionation path to file. Default /sdcard/screen.png.
    """
    _execute_command('adb shell screencap ', file)


def adb_shell_screenrecord(file, **kwargs):
    """
    recording the display of devices running Android. Android 4.4 and higher.
    :param file:
    :param kwargs:
    :return:
    """
    cmd = 'adb shell screenrecord ' + file
    _execute_subprocess(cmd)


def adb_shell_screenrecord_stop():
    _kill_subprocess()
    adb_kill_server()
    adb_devices()
    'INFO: Screen Recording stopped'

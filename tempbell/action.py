import subprocess

class ActionExecutionError (BaseException):
    pass

#
def action_ignore():
    pass

#
def action_dbus():
    raise NotImplementedError('not implemented. comming soon')

#
def is_enable_action_poweroff() -> bool:
    retval = False

    with open('/proc/sys/kernel/sysrq', 'r') as f:
        if int(f.read()) == 0x80:
            retval = True

    return retval

# set power off
def action_poweroff():
    try:
        if not is_enable_action_poweroff():
            raise ActionExecutionError('operation not supported by kernel config')

        with open('/proc/sysrq-trigger', 'w') as f:
            subprocess.run(['echo', 'o'], stdout = f)

    except ( OSError, FileNotFoundError, PermissionError ) as e:
        raise ActionExecutionError(e)
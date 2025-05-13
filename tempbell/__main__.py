import os
import sys
import signal
import logging
import logging.handlers
import platform
import argparse

from time import sleep
from daemon import DaemonContext

from .config import Config
from .action import ( ActionExecutionError, 
                      is_enable_action_poweroff, 
                      action_poweroff, 
                      action_ignore,
                      action_dbus )

from tempbell.reader import ReaderFactory

#
def app_init():
    
    # dublicate logs
    if settings.daemon:
        logging.getLogger().addHandler(logging.handlers.SysLogHandler(address='/dev/log'))

#
def app_loop():
    global keep_looping

    logger = logging.getLogger('AppLoop')

    reader = ReaderFactory.get_reader(settings.vendor, settings.model)

    if reader is None:
        logger.fatal('{} {} not supporting yet, sorry'.format(settings.vendor, settings.model))

        sys.exit(1)

    while keep_looping:
        logger.debug("reading sensors")
        
        temp_slice = reader.read()

        if temp_slice.status == 'alarm':
            logger.info('ALARM! {}'.format(temp_slice.alarm_reason))

            if settings.alarm == 'ignore':
                logger.info('call ignore action')
                action_ignore()

            elif settings.alarm == 'dbus':
                logger.info('calling dbus action')
                action_dbus()

            elif settings.alarm == 'poweroff':
                logger.info('calling poweroff action')

                try:
                    action_poweroff()
                except ActionExecutionError as e:
                    logger.fatal('can not execute poweroff action: {}'.format(e))
                    exit(1)

        # shootdown the node
        logger.debug("sleeping for a {} seconds".format(settings.interval))

        sleep(settings.interval)
#
def stop_and_exit(signal, frame):
    global keep_looping
    
    keep_looping = False
    logger.info('terminating sensor reading loop')

# reading argvs
args_parser = argparse.ArgumentParser()
args_parser.add_argument("-c", '--config', default = '.env')

args = args_parser.parse_args()

if not os.path.isfile(args.config) or not os.access(args.config, os.R_OK):
    sys.stderr.write('config file does not exists or not readable\n')
    exit(1)

# reading app config
settings = Config(_env_file = args.config)

# manage application loop
keep_looping = True

# setting up logger
logging.basicConfig(level=settings.loglevel, 
                    stream=sys.stdout)

#
if __name__ == "__main__":

    logger = logging.getLogger('App')

    if platform.system() != "Linux":
        logger.fatal('config check: os {} does not support'.format(platform.system()))
        sys.exit(1)

    # check poweroff campabilitie
    if settings.alarm == 'poweroff':
        if not is_enable_action_poweroff():
            logger.fatal('config check: action poweroff is disabled in linux kernel config (see. https://www.kernel.org/doc/Documentation/admin-guide/sysrq.rst)')
            exit(1)

    app_init()

    # create daemon context
    context = DaemonContext(signal_map = { signal.SIGTERM: stop_and_exit, 
                                           signal.SIGINT: stop_and_exit })

    if not settings.daemon:
        context.detach_process = False

        context.stdout = sys.stdout
        context.stderr = sys.stderr

    with context as ctx:
        logger.info('enter sensor feeding loop')

        app_loop()
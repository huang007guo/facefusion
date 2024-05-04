import logging
import pathlib
import sys
from typing import Dict
from logging import basicConfig, getLogger, Logger, DEBUG, INFO, WARNING, ERROR

from facefusion.typing import LogLevel


def init(log_level : LogLevel) -> None:
	# 创建目录/tmp/facefusion.log
	# pathlib.Path('/tmp').mkdir(exist_ok = True, parents = True)
	# 日志文件位置: /tmp/facefusion.log
	# basicConfig(format = None, filename = '/tmp/facefusion.log')
	# get_package_logger().setLevel(get_log_levels()[log_level])
	log_init(get_package_logger(), log_level=get_log_levels()[log_level])


def log_init(logger, log_filename='facefusion.log', log_level: int | str="INFO", log_level_file=None):
	# formatter = logging.Formatter('%(asctime)s.%(msecs)d %(name)s %(levelname)s %(pathname)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	formatter = logging.Formatter(
		'%(asctime)s.%(msecs)d %(name)s %(levelname)s %(module)s.%(funcName)s:%(lineno)d - %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S')
	log_level_file = log_level_file if log_level_file is not None else log_level
	streamHandler = logging.StreamHandler(sys.stdout)
	streamHandler.setFormatter(formatter)
	streamHandler.setLevel(log_level)
	logging.basicConfig(handlers=[streamHandler], level=log_level)
	fileHandler = logging.FileHandler(log_filename)
	fileHandler.setFormatter(formatter)
	fileHandler.setLevel(log_level_file)
	logger.addHandler(fileHandler)

def get_package_logger() -> Logger:
	return getLogger('facefusion')


def debug(message : str, scope : str) -> None:
	get_package_logger().debug('[' + scope + '] ' + message)


def info(message : str, scope : str) -> None:
	get_package_logger().info('[' + scope + '] ' + message)


def warn(message : str, scope : str) -> None:
	get_package_logger().warning('[' + scope + '] ' + message)


def error(message : str, scope : str) -> None:
	get_package_logger().error('[' + scope + '] ' + message)


def enable() -> None:
	get_package_logger().disabled = False


def disable() -> None:
	get_package_logger().disabled = True


def get_log_levels() -> Dict[LogLevel, int]:
	return\
	{
		'error': ERROR,
		'warn': WARNING,
		'info': INFO,
		'debug': DEBUG
	}

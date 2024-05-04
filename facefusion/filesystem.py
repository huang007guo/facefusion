import base64
from typing import List, Optional
import glob
import os
import shutil
import tempfile
import filetype
from pathlib import Path

import facefusion.globals
from facefusion import logger

TEMP_DIRECTORY_PATH = os.path.join(tempfile.gettempdir(), 'facefusion')
TEMP_OUTPUT_VIDEO_NAME = 'temp.mp4'


def get_temp_frame_paths(target_path: str) -> List[str]:
	temp_frames_pattern = get_temp_frames_pattern(target_path, '*')
	return sorted(glob.glob(temp_frames_pattern))


def has_files(directory):
	for entry in os.scandir(directory):
		if entry.is_file():
			return True
	return False


def get_out_temp_frame_paths(target_path: str) -> List[str]:
	temp_frames_pattern = get_out_temp_frames_pattern(target_path, '*')
	return sorted(glob.glob(temp_frames_pattern))


# 检查是否为临时文件
def is_temp_file(file_path: str) -> bool:
	# 检查是否在tempfile.gettempdir()下
	return file_path.startswith(tempfile.gettempdir())


def get_temp_frames_pattern(target_path: str, temp_frame_prefix: str) -> str:
	temp_directory_path = get_temp_directory_path(target_path)
	return os.path.join(temp_directory_path, temp_frame_prefix + '.' + facefusion.globals.temp_frame_format)


# 获取新的输出临时目录
def get_out_temp_directory_path(target_path: str) -> str:
	return os.path.join(get_temp_directory_path(target_path), 'out')


def get_out_temp_frames_pattern(target_path: str, temp_frame_prefix: str) -> str:
	temp_directory_path = get_out_temp_directory_path(target_path)
	return os.path.join(temp_directory_path, temp_frame_prefix + '.' + facefusion.globals.temp_frame_format)


import hashlib


def get_str_md5(content: str) -> str:
	"""
	计算字符串的 MD5 哈希值。

	参数:
		content (str): 待计算哈希值的字符串。

	返回:
		str: 计算得到的 MD5 哈希值，以十六进制字符串形式表示。
	"""
	m = hashlib.md5()
	m.update(content.encode('utf-8'))  # 将字符串编码为字节串，然后更新到 MD5 对象
	return m.hexdigest()  # 返回 MD5 哈希值的十六进制表示


# 获得临时目录路径
def get_temp_directory_path(target_path: str) -> str:
	target_name, _ = os.path.splitext(os.path.basename(target_path))
	# target_path做base64
	# target_name = base64.encodebytes(target_name.encode()).decode()
	# 替换为一个合法路径 系统找不到指定的路径。: 'C:\\Users\\ADMINI~1.PC-\\AppData\\Local\\Temp\\facefusion\\5peg56CB56C06KejLUFUSUQtNDU0IOaIkeeahOavjeS6suaIkOS4uuaIkeiHquW3seeahCBPbmFo\nbyDlubbluK7liqnov5vooYzmgKfmsrvnlpfoiJ7ljp_po57lsLs=\n'
	# target_name = target_name.replace('+', '_').replace('/', '_')
	# md5路径
	target_name = get_str_md5(target_name)
	temp_path = os.path.join(facefusion.globals.temp_dir if facefusion.globals.temp_dir else TEMP_DIRECTORY_PATH,
							 target_name)
	# logger.info("temp_path:" + temp_path, __name__.upper())
	return temp_path


def get_temp_output_video_path(target_path: str) -> str:
	temp_directory_path = get_temp_directory_path(target_path)
	return os.path.join(temp_directory_path, TEMP_OUTPUT_VIDEO_NAME)


def create_temp(target_path: str) -> None:
	temp_directory_path = get_temp_directory_path(target_path)
	logger.info(f'creating temp directory: {temp_directory_path}', __name__.upper())
	Path(temp_directory_path).mkdir(parents=True, exist_ok=True)


# 移动临时文件
def move_temp(target_path: str, output_path: str) -> None:
	temp_output_video_path = get_temp_output_video_path(target_path)
	if is_file(temp_output_video_path):
		if is_file(output_path):
			os.remove(output_path)
		shutil.move(temp_output_video_path, output_path)


# 检查临时文件是否移动完成, output_path不是文件或output_path是文件大于等于temp_output_video_path的文件大小
def is_temp_moved(target_path: str, output_path: str) -> bool:
	temp_output_video_path = get_temp_output_video_path(target_path)
	return not is_file(temp_output_video_path) or (
		is_file(output_path) and os.path.getsize(output_path) >= os.path.getsize(temp_output_video_path))


def clear_temp(target_path: str) -> None:
	temp_directory_path = get_temp_directory_path(target_path)
	parent_directory_path = os.path.dirname(temp_directory_path)
	if not facefusion.globals.keep_temp and is_directory(temp_directory_path):
		shutil.rmtree(temp_directory_path, ignore_errors=True)
	if os.path.exists(parent_directory_path) and not os.listdir(parent_directory_path):
		os.rmdir(parent_directory_path)


def is_file(file_path: str) -> bool:
	return bool(file_path and os.path.isfile(file_path))


def is_directory(directory_path: str) -> bool:
	return bool(directory_path and os.path.isdir(directory_path))


def is_audio(audio_path: str) -> bool:
	return is_file(audio_path) and filetype.helpers.is_audio(audio_path)


def has_audio(audio_paths: List[str]) -> bool:
	if audio_paths:
		return any(is_audio(audio_path) for audio_path in audio_paths)
	return False


def is_image(image_path: str) -> bool:
	return is_file(image_path) and filetype.helpers.is_image(image_path)


def has_image(image_paths: List[str]) -> bool:
	if image_paths:
		return any(is_image(image_path) for image_path in image_paths)
	return False


def is_video(video_path: str) -> bool:
	return is_file(video_path) and filetype.helpers.is_video(video_path)


def filter_audio_paths(paths: List[str]) -> List[str]:
	if paths:
		return [path for path in paths if is_audio(path)]
	return []


def filter_image_paths(paths: List[str]) -> List[str]:
	if paths:
		return [path for path in paths if is_image(path)]
	return []


def resolve_relative_path(path: str) -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


def list_directory(directory_path: str) -> Optional[List[str]]:
	if is_directory(directory_path):
		files = os.listdir(directory_path)
		return sorted([Path(file).stem for file in files if not Path(file).stem.startswith(('.', '__'))])
	return None

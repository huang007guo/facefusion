import base64
import fnmatch
from typing import List, Optional
import glob
import os
import shutil
import tempfile
import filetype
from pathlib import Path

from filetype.types import IMAGE as FILETYPE_IMAGE, VIDEO as FILETYPE_VIDEO

import facefusion.globals
from facefusion import logger

TEMP_DIRECTORY_PATH = os.path.join(tempfile.gettempdir(), 'facefusion')
TEMP_OUTPUT_VIDEO_NAME = 'temp.mp4'


# 判断是否存在输出的临时目录,并且里面有文件
def exist_temp_directory(target_path: str) -> bool:
	temp_directory_path = get_temp_directory_path(target_path)
	if os.path.isdir(temp_directory_path) and has_files(temp_directory_path):
		return True
	return False


# 判断是否需要范围取帧
def is_need_range(total_frame) -> bool:
	from facefusion.ffmpeg import is_use_history_frame
	return is_use_history_frame and (
		(facefusion.globals.trim_frame_start and facefusion.globals.trim_frame_start > 1) or (
		facefusion.globals.trim_frame_end and facefusion.globals.trim_frame_end < total_frame))


def get_temp_frame_paths_range(target_path, trim_frame_start, trim_frame_end):
	"""
	获取指定范围的帧路径
	:param target_path:
	:param trim_frame_start:
	:param trim_frame_end:
	:return:
	"""
	temp_directory_path = get_temp_directory_path(target_path)
	# return [os.path.join(temp_directory_path, "{:04d}".format(now_frame) + '.' + facefusion.globals.temp_frame_format)
	# 		for now_frame in range(trim_frame_start, trim_frame_end + 1)]
	result = []
	for now_frame in range(trim_frame_start, trim_frame_end+1):
		file_path = os.path.join(temp_directory_path,
								 "{:04d}".format(now_frame) + '.' +
								 facefusion.globals.temp_frame_format)
		if os.path.exists(file_path):
			result.append(file_path)
	return result


def get_out_temp_frame_paths_range(target_path, trim_frame_start, trim_frame_end):
	"""
	获取指定范围的帧路径
	:param target_path:
	:param trim_frame_start:
	:param trim_frame_end:
	:return:
	"""
	temp_directory_path = get_out_temp_directory_path(target_path)
	# return [os.path.join(temp_directory_path, "{:04d}".format(now_frame) + '.' + facefusion.globals.temp_frame_format)
	# 		for now_frame in range(trim_frame_start, trim_frame_end + 1)]
	result = []
	for now_frame in range(trim_frame_start, trim_frame_end+1):
		file_path = os.path.join(temp_directory_path,
								 "{:04d}".format(now_frame) + '.' +
								 facefusion.globals.temp_frame_format)
		if os.path.exists(file_path):
			result.append(file_path)
	return result


def get_temp_frame_paths(target_path: str) -> List[str]:
	from facefusion.vision import count_video_frame_total
	total_frame = count_video_frame_total(target_path)
	# 如果是跳过的情况判断,并且临时目录有文件,并且指定开始帧结束帧,需要去手动匹配
	if is_need_range(total_frame):
		return get_temp_frame_paths_range(target_path, facefusion.globals.trim_frame_start or 1,
										  facefusion.globals.trim_frame_end or total_frame)
	temp_frames_pattern = get_temp_frames_pattern(target_path, '*')
	return sorted(glob.glob(temp_frames_pattern))


def has_files(directory):
	for entry in os.scandir(directory):
		if entry.is_file():
			return True
	return False


def get_out_temp_frame_paths(target_path: str) -> List[str]:
	from facefusion.vision import count_video_frame_total
	total_frame = count_video_frame_total(target_path)
	# 如果是跳过的情况判断,并且临时目录有文件,并且指定开始帧结束帧,需要去手动匹配
	if is_need_range(total_frame):
		return get_out_temp_frame_paths_range(target_path, facefusion.globals.trim_frame_start or 1,
											  facefusion.globals.trim_frame_end or total_frame)
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
	if facefusion.globals.out_new_dir:
		out_temp_directory_path = get_out_temp_directory_path(target_path)
		logger.info(f'creating out temp directory: {out_temp_directory_path}', __name__.upper())
		Path(out_temp_directory_path).mkdir(parents=True, exist_ok=True)


# 创建目录
def create_directory(directory_path: str) -> None:
	# logger.info(f'creating directory: {directory_path}', __name__.upper())
	Path(directory_path).mkdir(parents=True, exist_ok=True)


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


def find_images(target_dir, call_back: callable = None):
	img_extensions = [img_ext for img_ext in [now_file_type.EXTENSION for now_file_type in FILETYPE_IMAGE]]
	img_extensions.append("jpeg")
	return find_files(target_dir, img_extensions, call_back)


def find_files(target_dir, img_extensions, call_back: callable = None):
	"""
	递归遍历target_dir目录下的所有图片文件（包括子目录），
	并将图片文件的路径存储到一个列表中返回。

	:param img_extensions:
	:param call_back:
	:param target_dir: 要遍历的目录路径
	:return: 包含所有图片路径的列表
	"""
	# 图片文件的可能扩展名列表
	# img_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']

	image_paths = []  # 用于存储图片路径的列表

	# 递归遍历目录
	for root, dirs, files in os.walk(target_dir):
		for img_file in files:
			# 当前文件后缀
			extension = img_file.split('.')[-1]
			# 转换为小写
			extension = extension.lower()
			if extension in img_extensions:
				# for extension in img_extensions:
				# 使用fnmatch过滤出图片文件,使用is_image?
				# for img_file in fnmatch.filter(files, extension):
				# 获取完整的图片文件路径并添加到列表中
				img_path = os.path.join(root, img_file)
				if call_back:
					call_back(img_path)
				else:
					image_paths.append(img_path)
	# 这里可以根据需要对每个图片路径进行处理
	# process_image(img_path)  # 示例处理函数调用

	return image_paths


def find_images_or_videos(target_dir, call_back: callable = None):
	img_extensions = [img_ext for img_ext in [now_file_type.EXTENSION for now_file_type in FILETYPE_IMAGE]]
	img_extensions.append("jpeg")
	img_extensions.extend([now_file_type.EXTENSION for now_file_type in FILETYPE_VIDEO])
	return find_files(target_dir, img_extensions, call_back)


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

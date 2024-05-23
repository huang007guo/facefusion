from typing import List
import os
import glob

def get_temp_directory_path(target_path: str) -> str:
	"""返回目标路径下的临时目录路径"""
	# 这个函数的实现取决于您的具体需求，这里假设是直接在目标路径下创建名为'temp'的目录
	return os.path.join(target_path, 'temp')

def get_temp_frames_pattern(target_path: str, start_frame: int, end_frame: int) -> str:
	"""
	根据指定的开始帧和结束帧生成匹配文件名的模式。

	:param target_path: 目标目录路径
	:param start_frame: 开始帧编号
	:param end_frame: 结束帧编号
	:return: 匹配指定帧范围的文件模式字符串
	"""
	temp_directory_path = get_temp_directory_path(target_path)
	# 确保帧号至少为4位
	frame_format = f"{start_frame:04d}.jpg-{end_frame:04d}.jpg"
	return os.path.join(temp_directory_path, frame_format)

target_path = r'C:\tmp\out\tmp\c9ac5c7c918f75ee03d12aa009d37889'
temp_frames_pattern = get_temp_frames_pattern(target_path, 1, 10)
print(temp_frames_pattern)

# 分解模式以获取基础路径和前缀后缀
base_path, _ = temp_frames_pattern.rsplit('-', 1)
prefix, suffix = base_path.rsplit('.', 1)

# 生成范围内所有可能的文件名
frame_numbers = range(1, 10 + 1)
frame_filenames = [f"{os.path.join(base_path, f'{frame:04d}')}{suffix}" for frame in frame_numbers]
print(sorted(frame_filenames))

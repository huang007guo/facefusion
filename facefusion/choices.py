from typing import List, Dict

from facefusion.typing import VideoMemoryStrategy, FaceSelectorMode, FaceAnalyserOrder, FaceAnalyserAge, FaceAnalyserGender, FaceDetectorModel, FaceMaskType, FaceMaskRegion, TempFrameFormat, OutputVideoEncoder, OutputVideoPreset
from facefusion.common_helper import create_int_range, create_float_range

video_memory_strategies : List[VideoMemoryStrategy] = [ 'strict', 'moderate', 'tolerant' ]
face_analyser_orders : List[FaceAnalyserOrder] = [ 'left-right', 'right-left', 'top-bottom', 'bottom-top', 'small-large', 'large-small', 'best-worst', 'worst-best' ]
face_analyser_ages : List[FaceAnalyserAge] = [ 'child', 'teen', 'adult', 'senior' ]
face_analyser_genders : List[FaceAnalyserGender] = [ 'female', 'male' ]
face_detector_set : Dict[FaceDetectorModel, List[str]] =\
{
	'many': [ '640x640' ],
	'retinaface': [ '160x160', '320x320', '480x480', '512x512', '640x640' ],
	'scrfd': [ '160x160', '320x320', '480x480', '512x512', '640x640' ],
	'yoloface': [ '640x640' ],
	'yunet': [ '160x160', '320x320', '480x480', '512x512', '640x640', '768x768', '960x960', '1024x1024' ]
}
face_selector_modes : List[FaceSelectorMode] = [ 'many', 'one', 'reference' ]
face_mask_types : List[FaceMaskType] = [ 'box', 'occlusion', 'region' ]
face_mask_regions : List[FaceMaskRegion] = [ 'skin', 'left-eyebrow', 'right-eyebrow', 'left-eye', 'right-eye', 'glasses', 'nose', 'mouth', 'upper-lip', 'lower-lip' ]
temp_frame_formats : List[TempFrameFormat] = [ 'bmp', 'jpg', 'png' ]
'''
libx264
类型: H.264/AVC 编码器。
开源: 是，基于MPEG-4 AVC标准。
特点: 提供高质量的视频压缩，广泛支持，CPU密集型，适用于软件编码。
应用场景: 网络视频、蓝光光盘、视频会议等。
libx265
类型: H.265/HEVC 编码器。
开源: 是，基于H.265标准。
特点: 相比x264，提供更高的压缩效率（通常能减少约50%的比特率），但计算复杂度更高，对硬件要求较高。
应用场景: 4K超高清视频、高分辨率视频流、视频存储优化等。
libvpx-vp9
类型: VP9 编码器，由Google开发。
开源: 是，开源且免费使用。
特点: 高压缩效率，特别适合网络视频应用，支持HDR，但相比H.265，编码速度较慢。
应用场景: YouTube、WebM格式视频、网页视频等。
h264_nvenc, hevc_nvenc
类型: 分别对应基于NVIDIA GPU的H.264和H.265硬件加速编码器。
特点: 利用GPU进行视频编码，显著降低CPU负担，提高编码速度，但可能在某些场景下的压缩效率和质量上不如最佳的软件编码器。
应用场景: 实时视频处理、游戏直播、高性能视频转码等需要高效编码的场景。
h264_amf, hevc_amf
类型: 分别对应基于AMD GPU的H.264和H.265硬件加速编码器。
特点: 同样利用GPU加速编码，减轻CPU压力，提升编码效率，与nvenc类似，但在不同硬件平台上的性能表现会有所差异。
应用场景: 与nvenc相似，适用于拥有AMD显卡的系统，进行高效视频处理和转码。
总结对比
压缩效率: libx265 > libvpx-vp9 > libx264 > (h264_nvenc/hevc_nvenc, h264_amf/hevc_amf)。硬件加速编码器在某些情况下可能因算法优化程度而有所不同。
资源消耗: 硬件加速编码器（如nvenc, amf）显著降低CPU使用，但可能需要更多GPU资源；软件编码器（如libx264, libx265）则更依赖CPU。
兼容性: libx264和libx265具有最广泛的兼容性，特别是在旧设备或不支持最新编解码标准的平台上。VP9在Web环境中得到良好支持，而硬件加速编码器则依赖于特定的GPU型号。
应用场景选择: 根据具体需求（如追求极致压缩、实时性、硬件条件等）来决定使用哪种编解码器。对于专业视频制作或存储空间有限的场景，libx265或libvpx-vp9可能是更好的选择；而对于需要快速编码、减轻CPU负担的应用，则应考虑硬件加速编码器。
'''
output_video_encoders : List[OutputVideoEncoder] = [ 'libx264', 'libx265', 'libvpx-vp9', 'h264_nvenc', 'hevc_nvenc', 'h264_amf', 'hevc_amf' ]
output_video_presets : List[OutputVideoPreset] = [ 'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow' ]

image_template_sizes : List[float] = [ 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4 ]
video_template_sizes : List[int] = [ 240, 360, 480, 540, 720, 1080, 1440, 2160, 4320 ]

execution_thread_count_range : List[int] = create_int_range(1, 128, 1)
execution_queue_count_range : List[int] = create_int_range(1, 32, 1)
system_memory_limit_range : List[int] = create_int_range(0, 128, 1)
face_detector_score_range : List[float] = create_float_range(0.0, 1.0, 0.05)
face_landmarker_score_range : List[float] = create_float_range(0.0, 1.0, 0.05)
face_mask_blur_range : List[float] = create_float_range(0.0, 1.0, 0.05)
face_mask_padding_range : List[int] = create_int_range(0, 100, 1)
reference_face_distance_range : List[float] = create_float_range(0.0, 1.5, 0.05)
output_image_quality_range : List[int] = create_int_range(0, 100, 1)
output_video_quality_range : List[int] = create_int_range(0, 100, 1)

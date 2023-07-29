from typing import Any, List, Callable
import cv2
import threading
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

import roop.globals
import roop.processors.frame.core
from roop.typing import Frame, Face
from roop.utilities import conditional_download, resolve_relative_path

BACKGROUND_ENHANCER = None
THREAD_SEMAPHORE = threading.Semaphore()
THREAD_LOCK = threading.Lock()
NAME = 'ROOP.PROCESSORS.FRAME.BACKGROUND_ENHANCER'


def get_background_enhancer() -> Any:
    global BACKGROUND_ENHANCER

    with THREAD_LOCK:
        if BACKGROUND_ENHANCER is None:
            model_path = resolve_relative_path('../models/RealESRGAN_x4plus.pth')
            BACKGROUND_ENHANCER = RealESRGANer(
                scale=4,
                model_path=model_path,
                model=RRDBNet(
                    num_in_ch=3,
                    num_out_ch=3,
                    num_feat=64,
                    num_block=23,
                    num_grow_ch=32,
                    scale=4
                ),
                device=get_device()
            )
    return BACKGROUND_ENHANCER


def get_device() -> str:
    if 'CUDAExecutionProvider' in roop.globals.execution_providers:
        return 'cuda'
    if 'CoreMLExecutionProvider' in roop.globals.execution_providers:
        return 'mps'
    return 'cpu'


def clear_background_enhancer() -> None:
    global BACKGROUND_ENHANCER

    BACKGROUND_ENHANCER = None


def pre_check() -> bool:
    download_directory_path = resolve_relative_path('../models')
    conditional_download(download_directory_path, ['https://huggingface.co/henryruhs/roop/resolve/main/RealESRGAN_x4plus.pth'])
    return True


def pre_start() -> bool:
    return True


def post_process() -> None:
    clear_background_enhancer()


def enhance_background(temp_frame: Frame) -> Frame:
    with THREAD_SEMAPHORE:
        temp_frame, _ = get_background_enhancer().enhance(temp_frame, outscale=1)
    return temp_frame


def process_frame(source_face: Face, reference_face: Face, temp_frame: Frame) -> Frame:
    return enhance_background(temp_frame)


def process_frames(source_path: str, temp_frame_paths: List[str], update: Callable[[], None]) -> None:
    for temp_frame_path in temp_frame_paths:
        temp_frame = cv2.imread(temp_frame_path)
        result = process_frame(None, None, temp_frame)
        cv2.imwrite(temp_frame_path, result)
        if update:
            update()


def process_image(source_path: str, target_path: str, output_path: str) -> None:
    target_frame = cv2.imread(target_path)
    result = process_frame(None, None, target_frame)
    cv2.imwrite(output_path, result)


def process_video(source_path: str, temp_frame_paths: List[str]) -> None:
    roop.processors.frame.core.process_video(None, temp_frame_paths, process_frames)
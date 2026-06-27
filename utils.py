"""工具模块"""
import os
import sys


def resource_path(relative_path: str) -> str:
    """获取资源文件路径，支持开发环境和 PyInstaller 打包环境"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def get_config_path() -> str:
    """获取配置文件路径（用户可写）"""
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        return os.path.join(exe_dir, 'config.json')
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
"""Winget 命令处理模块"""
import subprocess
import json
import unicodedata
from typing import List, Optional, Tuple
from models import SoftwarePackage, UpgradeResult


class WingetHandler:
    """处理与 winget 命令的交互"""
    
    def __init__(self, i18n=None):
        self.winget_path = "winget"
        self.i18n = i18n
    
    @staticmethod
    def _display_width(s: str) -> int:
        """计算字符串在终端中的显示宽度
        
        中文字符（全角字符）占2列，英文字符（半角字符）占1列
        """
        width = 0
        for char in s:
            # 获取字符的东亚宽度属性
            # W = 全角字符（宽度2）
            # F = 全角字符（宽度2）
            # H = 半角字符（宽度1）
            # N = 中性字符（宽度1）
            # Na = 窄字符（宽度1）
            ea_width = unicodedata.east_asian_width(char)
            if ea_width in ('W', 'F'):
                width += 2
            else:
                width += 1
        return width
    
    def check_winget_available(self) -> Tuple[bool, str]:
        """检查 winget 是否可用"""
        try:
            result = subprocess.run(
                [self.winget_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                if self.i18n:
                    return True, f"{self.i18n.t('winget')} {self.i18n.t('version')}: {result.stdout.strip()}"
                return True, f"Winget 版本: {result.stdout.strip()}"
            else:
                if self.i18n:
                    return False, self.i18n.t('error_winget_unavailable')
                return False, "Winget 命令执行失败"
        except FileNotFoundError:
            if self.i18n:
                return False, self.i18n.t('error_winget_unavailable') + "\n\n" + self.i18n.t('error_winget_install')
            return False, "未找到 winget 命令，请确保已安装 Windows Package Manager"
        except subprocess.TimeoutExpired:
            return False, "Winget 命令超时"
        except Exception as e:
            return False, f"检查 winget 时发生错误: {str(e)}"
    
    def get_upgradeable_packages(self) -> Tuple[List[SoftwarePackage], str]:
        """获取可更新的软件包列表
        
        Returns:
            Tuple[List[SoftwarePackage], str]: (软件包列表, 错误信息)
        """
        try:
            # 使用 winget upgrade 命令获取可更新的软件列表
            # 使用 --include-unknown 参数确保显示所有软件
            result = subprocess.run(
                [self.winget_path, "upgrade", "--include-unknown"],
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode != 0:
                return [], f"获取更新列表失败: {result.stderr}"
            
            # 解析输出
            packages = self._parse_upgrade_output(result.stdout)
            return packages, ""
            
        except subprocess.TimeoutExpired:
            return [], "获取更新列表超时"
        except Exception as e:
            return [], f"获取更新列表时发生错误: {str(e)}"
    
    def _parse_upgrade_output(self, output: str) -> List[SoftwarePackage]:
        """解析 winget upgrade 命令的输出"""
        packages = []
        lines = output.split('\n')
        
        # 查找表头位置
        header_line = None
        header_index = -1
        
        for i, line in enumerate(lines):
            # 查找包含 "名称" 或 "Name" 的行作为表头
            if '名称' in line or 'Name' in line:
                header_line = line
                header_index = i
                break
        
        if header_line is None:
            return packages
        
        # 解析列位置
        columns = self._parse_header_columns(header_line)
        
        # 解析数据行（跳过表头和分隔线）
        for i in range(header_index + 2, len(lines)):
            line = lines[i].strip()
            if not line or line.startswith('-'):
                continue
            
            package = self._parse_package_line(line, columns)
            if package:
                packages.append(package)
        
        return packages
    
    def _parse_header_columns(self, header_line: str) -> dict:
        """解析表头列位置（使用显示宽度）"""
        columns = {}
        
        # 找到各列的起始位置（显示宽度）
        def find_column_display_pos(text: str, patterns: list) -> int:
            """查找列名的显示宽度位置"""
            for pattern in patterns:
                pos = text.find(pattern)
                if pos != -1:
                    # 计算该位置的显示宽度
                    display_pos = self._display_width(text[:pos])
                    return display_pos
            return -1
        
        name_pos = find_column_display_pos(header_line, ['名称', 'Name'])
        id_pos = find_column_display_pos(header_line, ['ID', '标识'])
        version_pos = find_column_display_pos(header_line, ['版本', 'Version'])
        available_pos = find_column_display_pos(header_line, ['可用', 'Available'])
        source_pos = find_column_display_pos(header_line, ['来源', 'Source'])
        
        columns = {
            'name': name_pos,
            'id': id_pos,
            'version': version_pos,
            'available': available_pos,
            'source': source_pos
        }
        
        return columns
    
    def _parse_package_line(self, line: str, columns: dict) -> Optional[SoftwarePackage]:
        """解析单行软件包数据（使用从右往左的正则表达式）"""
        # 优先使用从右往左的正则表达式解析，更可靠
        result = self._parse_package_line_regex(line)
        if result:
            return result
        
        # 如果正则解析失败，尝试显示宽度解析作为备用
        return self._parse_package_line_positional(line, columns)
    
    def _parse_package_line_regex(self, line: str) -> Optional[SoftwarePackage]:
        """使用正则表达式从右往左解析（主解析方法）"""
        try:
            import re
            
            line = line.strip()
            if not line:
                return None
            
            # 匹配模式：source 在最后，前面是版本号，再前面是版本号，再前面是ID，最前面是名称
            # 模式：(.*?)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+(winget|msstore)$
            # group(1): name (可能包含空格)
            # group(2): package_id (不包含空格)
            # group(3): current_version (不包含空格)
            # group(4): available_version (不包含空格)
            # group(5): source (winget 或 msstore)
            pattern = r'^(.*?)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+(winget|msstore)$'
            match = re.match(pattern, line)
            
            if match:
                name = match.group(1).strip()
                package_id = match.group(2).strip()
                current_version = match.group(3).strip()
                available_version = match.group(4).strip()
                source = match.group(5).strip()
                
                if name and package_id:
                    return SoftwarePackage(
                        name=name,
                        package_id=package_id,
                        current_version=current_version or "未知",
                        available_version=available_version or "未知",
                        source=source or "winget"
                    )
            
            return None
            
        except Exception:
            return None
    
    def _parse_package_line_positional(self, line: str, columns: dict) -> Optional[SoftwarePackage]:
        """使用显示宽度解析（备用方法）"""
        try:
            def display_pos_to_index(target_display_pos: int) -> int:
                if target_display_pos == -1:
                    return -1
                
                current_display_width = 0
                for i, char in enumerate(line):
                    ea_width = unicodedata.east_asian_width(char)
                    if ea_width in ('W', 'F'):
                        current_display_width += 2
                    else:
                        current_display_width += 1
                    
                    if current_display_width >= target_display_pos:
                        return i
                return -1
            
            name_start = display_pos_to_index(columns['name'])
            id_start = display_pos_to_index(columns['id'])
            version_start = display_pos_to_index(columns['version'])
            available_start = display_pos_to_index(columns['available'])
            source_start = display_pos_to_index(columns['source'])
            
            def get_field(start_idx: int, end_idx: int = None) -> str:
                if start_idx == -1:
                    return ""
                if end_idx is None or end_idx == -1:
                    return line[start_idx:].strip()
                if start_idx >= end_idx:
                    return ""
                return line[start_idx:end_idx].strip()
            
            name = get_field(name_start, id_start)
            package_id = get_field(id_start, version_start)
            current_version = get_field(version_start, available_start)
            available_version = get_field(available_start, source_start)
            source = get_field(source_start)
            
            if name and package_id:
                return SoftwarePackage(
                    name=name,
                    package_id=package_id,
                    current_version=current_version or "未知",
                    available_version=available_version or "未知",
                    source=source or "winget"
                )
            
            return None
            
        except Exception:
            return None
    
    def upgrade_package(self, package_id: str, progress_callback=None) -> UpgradeResult:
        """更新指定软件包（支持实时进度回调）"""
        try:
            process = subprocess.Popen(
                [self.winget_path, "upgrade", "--id", package_id, "--accept-source-agreements", "--accept-package-agreements"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            
            output_lines = []
            
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                
                if line:
                    line = line.strip()
                    output_lines.append(line)
                    
                    if progress_callback and callable(progress_callback):
                        try:
                            progress_callback(line)
                        except Exception:
                            pass
            
            returncode = process.poll()
            
            if returncode == 0:
                if self.i18n:
                    return UpgradeResult(
                        package_id=package_id,
                        success=True,
                        message=self.i18n.t('success_upgrade', package_id=package_id)
                    )
                return UpgradeResult(
                    package_id=package_id,
                    success=True,
                    message=f"软件 {package_id} 更新成功"
                )
            else:
                if self.i18n:
                    return UpgradeResult(
                        package_id=package_id,
                        success=False,
                        message=self.i18n.t('error_upgrade_failed', package_id=package_id),
                        error='\n'.join(output_lines)
                    )
                return UpgradeResult(
                    package_id=package_id,
                    success=False,
                    message=f"软件 {package_id} 更新失败",
                    error='\n'.join(output_lines)
                )
                
        except subprocess.TimeoutExpired:
            if self.i18n:
                return UpgradeResult(
                    package_id=package_id,
                    success=False,
                    message=self.i18n.t('error_upgrade_failed', package_id=package_id),
                    error=self.i18n.t('error_upgrade_timeout')
                )
            return UpgradeResult(
                package_id=package_id,
                success=False,
                message=f"软件 {package_id} 更新超时",
                error="更新操作超时"
            )
        except Exception as e:
            if self.i18n:
                return UpgradeResult(
                    package_id=package_id,
                    success=False,
                    message=self.i18n.t('error_upgrade_error', package_id=package_id),
                    error=str(e)
                )
            return UpgradeResult(
                package_id=package_id,
                success=False,
                message=f"软件 {package_id} 更新时发生错误",
                error=str(e)
            )
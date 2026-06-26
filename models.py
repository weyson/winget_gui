"""数据模型定义"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SoftwarePackage:
    """软件包数据模型"""
    name: str
    package_id: str
    current_version: str
    available_version: str
    source: str = "winget"
    selected: bool = False
    
    def __str__(self):
        return f"{self.name} ({self.current_version} -> {self.available_version})"


@dataclass
class UpgradeResult:
    """更新结果数据模型"""
    package_id: str
    success: bool
    message: str
    error: Optional[str] = None


class PackageManager:
    """软件包管理器"""
    
    def __init__(self):
        self.packages: List[SoftwarePackage] = []
    
    def add_package(self, package: SoftwarePackage):
        """添加软件包"""
        self.packages.append(package)
    
    def clear_packages(self):
        """清空软件包列表"""
        self.packages.clear()
    
    def get_selected_packages(self) -> List[SoftwarePackage]:
        """获取所有被选中的软件包"""
        return [pkg for pkg in self.packages if pkg.selected]
    
    def select_all(self):
        """全选"""
        for pkg in self.packages:
            pkg.selected = True
    
    def deselect_all(self):
        """取消全选"""
        for pkg in self.packages:
            pkg.selected = False
    
    def toggle_select_all(self) -> bool:
        """切换全选状态，返回当前是否全选"""
        if self.is_all_selected():
            self.deselect_all()
            return False
        else:
            self.select_all()
            return True
    
    def is_all_selected(self) -> bool:
        """检查是否全选"""
        return len(self.packages) > 0 and all(pkg.selected for pkg in self.packages)
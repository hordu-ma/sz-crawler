#!/usr/bin/env python3
"""
PATH 管理模块
提供高效的PATH环境变量优化功能
"""

import os
import sys
from typing import List, Set, Dict, Optional
from pathlib import Path


class PathOptimizer:
    """PATH优化器类，提供高效的PATH管理功能"""
    
    def __init__(self):
        """初始化PATH优化器"""
        self.priority_paths = self._get_priority_paths()
        self.system_paths = self._get_system_paths()
    
    def _get_priority_paths(self) -> List[str]:
        """获取优先级路径列表"""
        priority_paths = []
        
        # 用户本地bin目录
        if os.name == 'posix':  # Unix/Linux/macOS
            priority_paths.extend([
                '/usr/local/bin',
                '/opt/homebrew/bin',  # Apple Silicon Mac
                '/usr/bin',
                '/bin',
                f'{os.path.expanduser("~")}/.local/bin',
                f'{os.path.expanduser("~")}/bin'
            ])
        elif os.name == 'nt':  # Windows
            priority_paths.extend([
                r'C:\Windows\System32',
                r'C:\Windows',
                r'C:\Program Files\Git\bin',
                r'C:\Python39\Scripts',
                r'C:\Python39'
            ])
        
        # 过滤存在的路径
        return [path for path in priority_paths if os.path.exists(path)]
    
    def _get_system_paths(self) -> Set[str]:
        """获取系统关键路径集合"""
        system_paths = set()
        
        if os.name == 'posix':
            system_paths.update([
                '/usr/bin', '/bin', '/usr/sbin', '/sbin',
                '/usr/local/bin', '/usr/local/sbin'
            ])
        elif os.name == 'nt':
            system_paths.update([
                r'C:\Windows\System32',
                r'C:\Windows',
                r'C:\Windows\System32\Wbem'
            ])
        
        return system_paths
    
    def _is_valid_path(self, path: str) -> bool:
        """检查路径是否有效
        
        Args:
            path: 要检查的路径
            
        Returns:
            bool: 路径是否有效
        """
        if not path or not isinstance(path, str):
            return False
        
        try:
            # 检查路径是否存在
            return os.path.isdir(path.strip())
        except (OSError, ValueError):
            return False
    
    def _deduplicate_preserving_order(self, paths: List[str]) -> List[str]:
        """使用集合进行高效去重，同时保持顺序
        
        Args:
            paths: 路径列表
            
        Returns:
            List[str]: 去重后的路径列表
        """
        seen = set()
        result = []
        
        for path in paths:
            # 标准化路径（处理大小写、斜杠等）
            normalized = os.path.normpath(path.strip()).lower()
            if normalized not in seen:
                seen.add(normalized)
                result.append(path.strip())
        
        return result
    
    def _categorize_paths(self, paths: List[str]) -> Dict[str, List[str]]:
        """将路径分类为优先级路径、系统路径和用户路径
        
        Args:
            paths: 路径列表
            
        Returns:
            Dict[str, List[str]]: 分类后的路径字典
        """
        categorized = {
            'priority': [],
            'system': [],
            'user': []
        }
        
        priority_set = set(os.path.normpath(p).lower() for p in self.priority_paths)
        
        for path in paths:
            normalized = os.path.normpath(path).lower()
            
            if normalized in priority_set:
                categorized['priority'].append(path)
            elif normalized in {os.path.normpath(p).lower() for p in self.system_paths}:
                categorized['system'].append(path)
            else:
                categorized['user'].append(path)
        
        return categorized
    
    def optimize_path(self, path_string: Optional[str] = None) -> str:
        """优化PATH环境变量
        
        优化策略：
        1. 使用集合进行O(1)去重操作
        2. 批量处理路径验证
        3. 智能排序：优先级路径 -> 系统路径 -> 用户路径
        4. 最小化字符串操作
        
        Args:
            path_string: PATH字符串，默认使用环境变量
            
        Returns:
            str: 优化后的PATH字符串
        """
        # 获取PATH字符串
        if path_string is None:
            path_string = os.environ.get('PATH', '')
        
        if not path_string:
            return ''
        
        # 分割PATH，使用系统特定的分隔符
        separator = ';' if os.name == 'nt' else ':'
        paths = path_string.split(separator)
        
        # 第一步：去重（保持顺序）
        unique_paths = self._deduplicate_preserving_order(paths)
        
        # 第二步：批量验证路径有效性
        valid_paths = [path for path in unique_paths if self._is_valid_path(path)]
        
        # 第三步：路径分类
        categorized = self._categorize_paths(valid_paths)
        
        # 第四步：按优先级重新排序
        optimized_paths = []
        
        # 优先级路径按预定义顺序排列
        priority_order = {path: i for i, path in enumerate(self.priority_paths)}
        categorized['priority'].sort(
            key=lambda x: priority_order.get(os.path.normpath(x).lower(), 999)
        )
        
        optimized_paths.extend(categorized['priority'])
        optimized_paths.extend(categorized['system'])
        optimized_paths.extend(categorized['user'])
        
        # 返回优化后的PATH字符串
        return separator.join(optimized_paths)
    
    def analyze_path(self, path_string: Optional[str] = None) -> Dict[str, any]:
        """分析PATH环境变量
        
        Args:
            path_string: PATH字符串，默认使用环境变量
            
        Returns:
            Dict[str, any]: 分析结果
        """
        if path_string is None:
            path_string = os.environ.get('PATH', '')
        
        separator = ';' if os.name == 'nt' else ':'
        original_paths = path_string.split(separator) if path_string else []
        
        # 统计信息
        unique_paths = self._deduplicate_preserving_order(original_paths)
        valid_paths = [path for path in unique_paths if self._is_valid_path(path)]
        invalid_paths = [path for path in unique_paths if not self._is_valid_path(path)]
        
        # 分类统计
        categorized = self._categorize_paths(valid_paths)
        
        return {
            'original_count': len(original_paths),
            'unique_count': len(unique_paths),
            'valid_count': len(valid_paths),
            'invalid_count': len(invalid_paths),
            'duplicates_removed': len(original_paths) - len(unique_paths),
            'invalid_paths': invalid_paths,
            'categorized': {
                'priority': len(categorized['priority']),
                'system': len(categorized['system']),
                'user': len(categorized['user'])
            },
            'optimized_path': self.optimize_path(path_string)
        }


def optimize_path(path_string: Optional[str] = None) -> str:
    """便捷函数：优化PATH环境变量
    
    Args:
        path_string: PATH字符串，默认使用环境变量
        
    Returns:
        str: 优化后的PATH字符串
    """
    optimizer = PathOptimizer()
    return optimizer.optimize_path(path_string)


def analyze_current_path() -> Dict[str, any]:
    """便捷函数：分析当前PATH环境变量
    
    Returns:
        Dict[str, any]: 分析结果
    """
    optimizer = PathOptimizer()
    return optimizer.analyze_path()


def main():
    """主函数：演示PATH优化功能"""
    print("PATH优化器 - 分析当前PATH环境变量")
    print("=" * 50)
    
    optimizer = PathOptimizer()
    analysis = optimizer.analyze_path()
    
    print(f"原始PATH条目数: {analysis['original_count']}")
    print(f"去重后条目数: {analysis['unique_count']}")
    print(f"有效路径数: {analysis['valid_count']}")
    print(f"无效路径数: {analysis['invalid_count']}")
    print(f"移除的重复项: {analysis['duplicates_removed']}")
    
    print(f"\n路径分类:")
    print(f"  优先级路径: {analysis['categorized']['priority']}")
    print(f"  系统路径: {analysis['categorized']['system']}")
    print(f"  用户路径: {analysis['categorized']['user']}")
    
    if analysis['invalid_paths']:
        print(f"\n无效路径:")
        for path in analysis['invalid_paths']:
            print(f"  - {path}")
    
    print(f"\n优化建议:")
    if analysis['duplicates_removed'] > 0:
        print(f"  - 可移除 {analysis['duplicates_removed']} 个重复路径")
    if analysis['invalid_count'] > 0:
        print(f"  - 可移除 {analysis['invalid_count']} 个无效路径")
    
    optimization_gain = analysis['original_count'] - analysis['valid_count']
    if optimization_gain > 0:
        percentage = (optimization_gain / analysis['original_count']) * 100
        print(f"  - 总共可减少 {optimization_gain} 个条目 ({percentage:.1f}%)")


if __name__ == "__main__":
    main()

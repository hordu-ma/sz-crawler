#!/usr/bin/env python3
"""
PATH优化器测试模块
测试optimize_path()函数的性能和正确性
"""

import time
import os
from typing import List
from path_manager import PathOptimizer, optimize_path


def create_test_path(size: int = 100) -> str:
    """创建用于测试的PATH字符串
    
    Args:
        size: PATH条目数量
        
    Returns:
        str: 测试用的PATH字符串
    """
    separator = ';' if os.name == 'nt' else ':'
    
    # 创建包含重复项和无效路径的测试PATH
    paths = []
    
    # 添加一些真实路径
    real_paths = ['/usr/bin', '/bin', '/usr/local/bin'] if os.name == 'posix' else [r'C:\Windows\System32', r'C:\Windows']
    paths.extend(real_paths * (size // 20 + 1))  # 添加重复项
    
    # 添加一些无效路径
    for i in range(size // 4):
        paths.append(f'/invalid/path/{i}')
    
    # 添加一些用户路径
    home = os.path.expanduser('~')
    for i in range(size // 4):
        paths.append(f'{home}/test_path_{i}')
    
    # 确保达到指定大小
    while len(paths) < size:
        paths.append(f'/test/path/{len(paths)}')
    
    return separator.join(paths[:size])


def benchmark_optimize_path():
    """基准测试optimize_path函数的性能"""
    print("PATH优化器性能测试")
    print("=" * 50)
    
    test_sizes = [50, 100, 500, 1000, 2000]
    
    for size in test_sizes:
        print(f"\n测试PATH大小: {size} 条目")
        
        # 创建测试数据
        test_path = create_test_path(size)
        
        # 测试优化性能
        start_time = time.time()
        optimized_path = optimize_path(test_path)
        end_time = time.time()
        
        # 分析结果
        optimizer = PathOptimizer()
        analysis = optimizer.analyze_path(test_path)
        
        execution_time = (end_time - start_time) * 1000  # 转换为毫秒
        
        print(f"  执行时间: {execution_time:.2f} ms")
        print(f"  原始条目: {analysis['original_count']}")
        print(f"  优化后条目: {analysis['valid_count']}")
        print(f"  去重数量: {analysis['duplicates_removed']}")
        print(f"  无效路径: {analysis['invalid_count']}")
        
        reduction_rate = ((analysis['original_count'] - analysis['valid_count']) / analysis['original_count']) * 100
        print(f"  减少率: {reduction_rate:.1f}%")


def test_optimize_path_correctness():
    """测试optimize_path函数的正确性"""
    print("\nPATH优化器正确性测试")
    print("=" * 50)
    
    # 测试用例1：基本去重
    print("\n测试1: 基本去重功能")
    separator = ';' if os.name == 'nt' else ':'
    test_path1 = separator.join(['/usr/bin', '/usr/local/bin', '/usr/bin', '/bin'])
    result1 = optimize_path(test_path1)
    
    result_paths = result1.split(separator)
    print(f"  输入: {test_path1}")
    print(f"  输出: {result1}")
    print(f"  去重正确: {len(result_paths) == len(set(result_paths))}")
    
    # 测试用例2：无效路径移除
    print("\n测试2: 无效路径移除")
    invalid_paths = ['/invalid/path/1', '/invalid/path/2', '/nonexistent']
    real_paths = ['/usr/bin'] if os.name == 'posix' else [r'C:\Windows\System32']
    test_path2 = separator.join(real_paths + invalid_paths)
    result2 = optimize_path(test_path2)
    
    print(f"  输入包含无效路径: {len(invalid_paths)} 个")
    print(f"  输出: {result2}")
    print(f"  无效路径已移除: {all(invalid not in result2 for invalid in invalid_paths)}")
    
    # 测试用例3：路径排序
    print("\n测试3: 优先级路径排序")
    optimizer = PathOptimizer()
    if optimizer.priority_paths:
        # 颠倒优先级路径的顺序
        reversed_priority = list(reversed(optimizer.priority_paths[:3]))
        test_path3 = separator.join(reversed_priority)
        result3 = optimize_path(test_path3)
        
        print(f"  输入（颠倒顺序): {test_path3}")
        print(f"  输出（应该重排序): {result3}")
        
        # 检查是否按优先级排序
        result_paths3 = result3.split(separator)
        is_sorted_correctly = True
        for i in range(len(result_paths3) - 1):
            path1 = os.path.normpath(result_paths3[i]).lower()
            path2 = os.path.normpath(result_paths3[i + 1]).lower()
            priority_paths_lower = [os.path.normpath(p).lower() for p in optimizer.priority_paths]
            
            if path1 in priority_paths_lower and path2 in priority_paths_lower:
                idx1 = priority_paths_lower.index(path1)
                idx2 = priority_paths_lower.index(path2)
                if idx1 > idx2:
                    is_sorted_correctly = False
                    break
        
        print(f"  优先级排序正确: {is_sorted_correctly}")


def test_edge_cases():
    """测试边界情况"""
    print("\nPATH优化器边界情况测试")
    print("=" * 50)
    
    # 测试空PATH
    print("\n测试1: 空PATH")
    result_empty = optimize_path("")
    print(f"  空PATH结果: '{result_empty}'")
    print(f"  处理正确: {result_empty == ''}")
    
    # 测试None PATH
    print("\n测试2: None PATH")
    # 临时移除PATH环境变量
    original_path = os.environ.get('PATH')
    if 'PATH' in os.environ:
        del os.environ['PATH']
    
    result_none = optimize_path()
    print(f"  None PATH结果: '{result_none}'")
    print(f"  处理正确: {result_none == ''}")
    
    # 恢复PATH环境变量
    if original_path:
        os.environ['PATH'] = original_path
    
    # 测试单个路径
    print("\n测试3: 单个路径")
    single_path = '/usr/bin' if os.name == 'posix' else r'C:\Windows\System32'
    result_single = optimize_path(single_path)
    print(f"  单个路径输入: {single_path}")
    print(f"  单个路径输出: {result_single}")
    print(f"  处理正确: {result_single == single_path}")


def performance_comparison():
    """性能对比测试：优化前后的性能对比"""
    print("\n性能对比测试")
    print("=" * 50)
    
    def naive_optimize_path(path_string: str) -> str:
        """朴素的PATH优化实现（效率较低）"""
        if not path_string:
            return ''
        
        separator = ';' if os.name == 'nt' else ':'
        paths = path_string.split(separator)
        
        # 低效的去重方法
        unique_paths = []
        for path in paths:
            if path not in unique_paths:
                unique_paths.append(path)
        
        # 低效的验证方法
        valid_paths = []
        for path in unique_paths:
            if os.path.isdir(path.strip()):
                valid_paths.append(path.strip())
        
        return separator.join(valid_paths)
    
    test_path = create_test_path(500)
    
    # 测试优化版本
    start_time = time.time()
    for _ in range(10):
        optimized_result = optimize_path(test_path)
    optimized_time = time.time() - start_time
    
    # 测试朴素版本
    start_time = time.time()
    for _ in range(10):
        naive_result = naive_optimize_path(test_path)
    naive_time = time.time() - start_time
    
    print(f"优化版本平均时间: {(optimized_time/10)*1000:.2f} ms")
    print(f"朴素版本平均时间: {(naive_time/10)*1000:.2f} ms")
    print(f"性能提升: {naive_time/optimized_time:.2f}x")
    print(f"结果一致性: {optimized_result == naive_result}")


def main():
    """主测试函数"""
    print("开始PATH优化器完整测试")
    print("=" * 60)
    
    # 运行所有测试
    benchmark_optimize_path()
    test_optimize_path_correctness()
    test_edge_cases()
    performance_comparison()
    
    print("\n" + "=" * 60)
    print("所有测试完成！")


if __name__ == "__main__":
    main()

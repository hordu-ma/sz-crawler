#!/usr/bin/env python3
"""
PATH优化器使用示例
演示如何使用高效的optimize_path()函数
"""

import os
from path_manager import PathOptimizer, optimize_path, analyze_current_path


def demo_basic_usage():
    """演示基本使用方法"""
    print("=== PATH优化器基本使用示例 ===\n")
    
    # 1. 使用便捷函数优化当前PATH
    print("1. 优化当前系统PATH:")
    original_path = os.environ.get('PATH', '')
    optimized_path = optimize_path()
    
    print(f"原始PATH长度: {len(original_path.split(':'))}")
    print(f"优化后PATH长度: {len(optimized_path.split(':'))}")
    print(f"优化后PATH: {optimized_path[:100]}...")  # 只显示前100字符
    
    # 2. 分析当前PATH
    print("\n2. 分析当前PATH:")
    analysis = analyze_current_path()
    print(f"原始条目数: {analysis['original_count']}")
    print(f"有效条目数: {analysis['valid_count']}")
    print(f"可移除条目数: {analysis['original_count'] - analysis['valid_count']}")
    
    if analysis['invalid_paths']:
        print("无效路径:")
        for path in analysis['invalid_paths'][:3]:  # 只显示前3个
            print(f"  - {path}")


def demo_custom_path_optimization():
    """演示自定义PATH优化"""
    print("\n=== 自定义PATH优化示例 ===\n")
    
    # 创建一个包含重复和无效路径的示例PATH
    separator = ':' if os.name == 'posix' else ';'
    custom_path = separator.join([
        '/usr/bin',
        '/usr/local/bin',
        '/usr/bin',  # 重复
        '/invalid/path',  # 无效
        '/bin',
        '/usr/local/bin',  # 重复
        '/another/invalid/path',  # 无效
        '/opt/homebrew/bin'
    ])
    
    print("自定义PATH优化:")
    print(f"原始PATH: {custom_path}")
    
    optimized = optimize_path(custom_path)
    print(f"优化后PATH: {optimized}")
    
    # 分析优化效果
    optimizer = PathOptimizer()
    analysis = optimizer.analyze_path(custom_path)
    
    print(f"\n优化统计:")
    print(f"  移除重复项: {analysis['duplicates_removed']}")
    print(f"  移除无效路径: {analysis['invalid_count']}")
    print(f"  总减少项目: {analysis['original_count'] - analysis['valid_count']}")


def demo_advanced_features():
    """演示高级功能"""
    print("\n=== 高级功能演示 ===\n")
    
    # 创建PathOptimizer实例
    optimizer = PathOptimizer()
    
    # 1. 查看优先级路径
    print("1. 系统优先级路径:")
    for i, path in enumerate(optimizer.priority_paths, 1):
        print(f"  {i}. {path}")
    
    # 2. 查看系统路径
    print(f"\n2. 系统关键路径数量: {len(optimizer.system_paths)}")
    
    # 3. 路径分类演示
    test_paths = ['/usr/bin', '/usr/local/bin', '/home/user/bin', '/opt/custom/bin']
    separator = ':' if os.name == 'posix' else ';'
    test_path_string = separator.join(test_paths)
    
    print(f"\n3. 路径分类示例:")
    print(f"测试路径: {test_path_string}")
    
    categorized = optimizer._categorize_paths(test_paths)
    print(f"优先级路径: {categorized['priority']}")
    print(f"系统路径: {categorized['system']}")
    print(f"用户路径: {categorized['user']}")


def demo_performance_comparison():
    """演示性能对比"""
    print("\n=== 性能对比演示 ===\n")
    
    import time
    
    # 创建一个大的测试PATH
    separator = ':' if os.name == 'posix' else ';'
    large_path_parts = []
    
    # 添加大量路径（包含重复和无效）
    for i in range(200):
        large_path_parts.append(f'/test/path/{i}')
        if i % 10 == 0:  # 每10个添加一个重复
            large_path_parts.append('/usr/bin')
    
    large_path = separator.join(large_path_parts)
    
    # 测试优化性能
    iterations = 10
    start_time = time.time()
    
    for _ in range(iterations):
        result = optimize_path(large_path)
    
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    
    print(f"大型PATH优化性能测试:")
    print(f"  测试路径条目数: {len(large_path_parts)}")
    print(f"  测试迭代次数: {iterations}")
    print(f"  平均执行时间: {avg_time*1000:.2f} ms")
    print(f"  吞吐量: {len(large_path_parts)/avg_time:.0f} 条目/秒")


def demo_practical_usage():
    """演示实际使用场景"""
    print("\n=== 实际使用场景演示 ===\n")
    
    print("场景1: 开发环境PATH清理")
    print("适用于开发者需要清理混乱的PATH环境变量")
    
    # 模拟开发环境的混乱PATH
    separator = ':' if os.name == 'posix' else ';'
    messy_dev_path = separator.join([
        '/usr/bin',
        '/usr/local/bin',
        '/Users/dev/.nvm/versions/node/v16.14.0/bin',
        '/usr/bin',  # 重复
        '/opt/homebrew/bin',
        '/Users/dev/.cargo/bin',
        '/invalid/python/path',  # 无效
        '/usr/local/bin',  # 重复
        '/Users/dev/.local/bin',
        '/Applications/Visual Studio Code.app/Contents/Resources/app/bin'
    ])
    
    print(f"混乱的开发PATH (条目数: {len(messy_dev_path.split(separator))}):")
    print(f"优化前: {messy_dev_path[:80]}...")
    
    cleaned_path = optimize_path(messy_dev_path)
    print(f"优化后: {cleaned_path}")
    print(f"优化后条目数: {len(cleaned_path.split(separator))}")
    
    # 展示如何在实际脚本中使用
    print(f"\n场景2: 在shell脚本中使用")
    print("可以在.bashrc或.zshrc中添加:")
    print("export PATH=$(python -c \"from path_manager import optimize_path; print(optimize_path())\")")


def main():
    """主演示函数"""
    print("PATH优化器使用示例")
    print("=" * 60)
    
    # 运行所有演示
    demo_basic_usage()
    demo_custom_path_optimization()
    demo_advanced_features()
    demo_performance_comparison()
    demo_practical_usage()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("\n优化要点总结:")
    print("1. 使用集合(set)进行O(1)去重操作，避免O(n²)的列表查找")
    print("2. 批量路径验证，减少系统调用次数")
    print("3. 智能路径分类和优先级排序，提高PATH查找效率")
    print("4. 最小化字符串操作，使用join而不是多次拼接")
    print("5. 预计算优先级路径和系统路径，避免重复计算")


if __name__ == "__main__":
    main()

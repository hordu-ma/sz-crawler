import PyInstaller.__main__
import os
import shutil
import sys

def build_exe():
    # 确保输出目录存在
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
    # 复制配置文件到dist目录
    shutil.copy('config.py', 'dist/config.py')
    
    # 获取当前目录的绝对路径
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    # PyInstaller参数
    params = [
        'crawler.py',  # 主程序文件
        '--name=思政新闻爬虫',  # 生成的exe名称
        '--onefile',  # 打包成单个exe文件
        '--noconsole',  # 不显示控制台窗口
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认覆盖
        f'--distpath={os.path.join(current_dir, "dist")}',  # 指定输出目录
        '--add-data=config.py;.',  # 添加配置文件
    ]
    
    # 如果存在图标文件，添加图标
    icon_path = os.path.join(current_dir, 'icon.ico')
    if os.path.exists(icon_path):
        params.append(f'--icon={icon_path}')
    
    # 执行打包
    PyInstaller.__main__.run(params)
    
    print("打包完成！")
    print(f"输出目录: {os.path.join(current_dir, 'dist')}")

if __name__ == '__main__':
    try:
        build_exe()
    except Exception as e:
        print(f"打包过程中出现错误: {str(e)}")
        sys.exit(1) 
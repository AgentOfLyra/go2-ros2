#!/usr/bin/env python3
"""
调试脚本：查看 ROS2 包路径和资源文件位置
"""

import os
from ament_index_python.packages import get_package_share_directory

def check_package_paths(package_name='go2_description'):
    """检查包路径和资源文件"""
    
    print("=" * 70)
    print(f"📦 检查包: {package_name}")
    print("=" * 70)
    
    try:
        # 获取包的安装路径
        pkg_path = get_package_share_directory(package_name)
        print(f"\n✅ 包安装路径:")
        print(f"   {pkg_path}")
        
        # 检查各个资源目录
        resources = {
            'URDF文件': 'urdf/go2_description.urdf',
            'DAE meshes': 'dae',
            'Launch文件': 'launch',
            'RViz配置': 'launch/check_joint_rviz2.rviz'
        }
        
        print(f"\n📂 资源文件位置:")
        print("-" * 70)
        
        for name, rel_path in resources.items():
            full_path = os.path.join(pkg_path, rel_path)
            exists = os.path.exists(full_path)
            status = "✅" if exists else "❌"
            
            print(f"\n{status} {name}:")
            print(f"   相对路径: {rel_path}")
            print(f"   绝对路径: {full_path}")
            print(f"   存在: {exists}")
            
            # 如果是目录，列出内容
            if exists and os.path.isdir(full_path):
                try:
                    files = os.listdir(full_path)
                    if files:
                        print(f"   内容 ({len(files)} 项):")
                        for f in sorted(files)[:5]:  # 只显示前5个
                            print(f"     - {f}")
                        if len(files) > 5:
                            print(f"     ... 还有 {len(files) - 5} 个文件")
                except Exception as e:
                    print(f"   无法列出目录内容: {e}")
        
        # 演示 package:// URI 的解析
        print(f"\n🔗 package:// URI 解析示例:")
        print("-" * 70)
        
        test_uris = [
            'package://go2_description/dae/base.dae',
            'package://go2_description/urdf/go2_description.urdf',
        ]
        
        for uri in test_uris:
            # 解析 package:// URI
            if uri.startswith('package://'):
                parts = uri.replace('package://', '').split('/', 1)
                if len(parts) == 2:
                    pkg_name = parts[0]
                    rel_path = parts[1]
                    
                    try:
                        pkg = get_package_share_directory(pkg_name)
                        full_path = os.path.join(pkg, rel_path)
                        exists = os.path.exists(full_path)
                        
                        print(f"\nURI: {uri}")
                        print(f"  → 解析为: {full_path}")
                        print(f"  → 文件存在: {exists}")
                    except Exception as e:
                        print(f"\nURI: {uri}")
                        print(f"  → 错误: {e}")
        
        # 显示 file:// 格式（用于 Gazebo）
        print(f"\n🌐 file:// URI 格式 (用于 Ignition Gazebo):")
        print("-" * 70)
        print(f"file://{pkg_path}/dae/base.dae")
        
        print("\n" + "=" * 70)
        print("✅ 检查完成！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n💡 提示: 请确保已经编译并 source 了工作空间:")
        print("   cd /home/lyra/learnRos2/chapter6_ws")
        print("   colcon build --packages-select go2_description")
        print("   source install/setup.bash")


if __name__ == '__main__':
    import sys
    
    package_name = 'go2_description'
    if len(sys.argv) > 1:
        package_name = sys.argv[1]
    
    check_package_paths(package_name)


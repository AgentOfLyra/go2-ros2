#!/bin/bash

echo "======================================"
echo "检查 Go2 机器人关节状态"
echo "======================================"
echo ""

# 激活工作空间
source /home/lyra/learnRos2/chapter6_ws/install/setup.bash

echo "1. 检查话题列表..."
echo "-----------------------------------"
ros2 topic list | grep -E "(joint|robot|tf)"
echo ""

echo "2. 检查 /joint_states 话题信息..."
echo "-----------------------------------"
ros2 topic info /joint_states
echo ""

echo "3. 等待 2 秒，检查是否有关节状态发布..."
echo "-----------------------------------"
timeout 2 ros2 topic echo /joint_states --once 2>&1 || echo "❌ 没有数据发布到 /joint_states"
echo ""

echo "4. 检查 robot_state_publisher 是否运行..."
echo "-----------------------------------"
ros2 node list | grep robot_state_publisher && echo "✅ robot_state_publisher 正在运行" || echo "❌ robot_state_publisher 未运行"
echo ""

echo "5. 检查 joint_state_publisher_gui 是否运行..."
echo "-----------------------------------"
ros2 node list | grep joint_state_publisher && echo "✅ joint_state_publisher_gui 正在运行" || echo "❌ joint_state_publisher_gui 未运行"
echo ""

echo "======================================"
echo "检查完成！"
echo "======================================"


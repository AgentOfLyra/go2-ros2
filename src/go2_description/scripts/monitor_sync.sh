#!/bin/bash

echo "======================================"
echo "监控 Gazebo 和 RViz 同步状态"
echo "======================================"
echo ""

# 激活工作空间
source /home/lyra/learnRos2/chapter6_ws/install/setup.bash

echo "📡 检查运行中的节点..."
echo "-----------------------------------"
ros2 node list
echo ""

echo "📋 检查话题列表..."
echo "-----------------------------------"
ros2 topic list | grep -E "(joint|clock|model)"
echo ""

echo "🔄 检查 /joint_states 话题..."
echo "-----------------------------------"
ros2 topic info /joint_states
echo ""
echo "发布频率："
ros2 topic hz /joint_states --window 10 &
HZ_PID=$!
sleep 3
kill $HZ_PID 2>/dev/null
echo ""

echo "📊 检查 /joint_states 内容（最新一条）..."
echo "-----------------------------------"
timeout 2 ros2 topic echo /joint_states --once 2>&1 | head -20
echo ""

echo "⏰ 检查仿真时钟..."
echo "-----------------------------------"
ros2 topic info /clock
echo ""

echo "🌉 检查桥接节点..."
echo "-----------------------------------"
ros2 node list | grep bridge && echo "✅ 桥接节点运行中" || echo "❌ 桥接节点未运行"
echo ""

echo "🤖 检查 robot_state_publisher..."
echo "-----------------------------------"
ros2 node list | grep robot_state_publisher && echo "✅ robot_state_publisher 运行中" || echo "❌ robot_state_publisher 未运行"
echo ""

echo "🎮 检查 Gazebo 模型话题..."
echo "-----------------------------------"
ros2 topic list | grep "/world/default/model/go2_description" || echo "⚠️  Gazebo 模型话题未找到"
echo ""

echo "======================================"
echo "💡 提示："
echo "  - /joint_states 应该有持续的数据发布"
echo "  - 桥接节点应该在运行"
echo "  - 在 Gazebo 中移动机器人，RViz 应该同步更新"
echo "======================================"


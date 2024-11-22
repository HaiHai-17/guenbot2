cmake_minimum_required(VERSION 3.5)
project(guenbot2_waypoint)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

option(BUILD_OPENVINO "Build OpenVINO" OFF)
option(BUILD_AUTODOCK "Build Auto Docking" OFF)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav2_behavior_tree REQUIRED)
find_package(nav2_msgs REQUIRED)
find_package(behaviortree_cpp_v3 REQUIRED)
find_package(OpenCV REQUIRED)
find_package(cv_bridge REQUIRED) # Đảm bảo tìm thấy cv_bridge

if(BUILD_OPENVINO STREQUAL "ON")
  find_package(object_msgs REQUIRED)
  set(OTHER_DEPS ${OTHER_DEPS} object_msgs)
  add_definitions(-DSUPPORT_OPENVINO)
endif()

if(BUILD_AUTODOCK STREQUAL "ON")
  find_package(autodock_msgs REQUIRED)
  set(OTHER_DEPS ${OTHER_DEPS} autodock_msgs)
  add_definitions(-DSUPPORT_AUTODOCK)
endif()

# Danh sách các dependencies
set(dependencies
  rclcpp
  rclcpp_action
  std_msgs
  geometry_msgs
  cv_bridge
  nav2_behavior_tree
  nav2_msgs
  behaviortree_cpp_v3
  OpenCV
  ${OTHER_DEPS}
)  

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# Tạo target 'send_goal'
add_executable(send_goal 
  src/send_goal.cpp
)
ament_target_dependencies(send_goal
  ${dependencies}
)

# Tạo target 'guenbot2_waypoint'
add_executable(guenbot2_waypoint
  src/bt_ros2.cpp
  src/qr_code_node.cpp
)
ament_target_dependencies(guenbot2_waypoint
  ${dependencies}
)

# Cài đặt các file thực thi
install(TARGETS
  send_goal
  guenbot2_waypoint
  DESTINATION lib/${PROJECT_NAME}
)

# Cài đặt thư mục XML
install(
  DIRECTORY waypoint_xml 
  DESTINATION share/${PROJECT_NAME}
)

# Cài đặt file launch
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()

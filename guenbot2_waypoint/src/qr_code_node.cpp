#include "qr_code_node.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "behaviortree_cpp_v3/action_node.h"
#include <chrono>
#include <thread>
#include <stack>

std::stack<std::string> PushToStack::stack_t;
std::stack<std::string> ProcessStack::stack_t;

CheckQRCode::CheckQRCode(const std::string& name, const BT::NodeConfiguration& config)
    : BT::SyncActionNode(name, config), qr_data_("") {
    node_ = rclcpp::Node::make_shared("qr_code_node");
    qr_sub_ = node_->create_subscription<std_msgs::msg::String>(
        "/qr_code_data", 10,
        [this](const std_msgs::msg::String::SharedPtr msg) {
            qr_data_ = msg->data;
        });
}

BT::PortsList CheckQRCode::providedPorts() {
    return {BT::InputPort<std::string>("qr_code"), BT::InputPort<int>("timeout")};
}

BT::NodeStatus CheckQRCode::tick() {
    std::string expected_qr;
    int timeout;
    getInput("qr_code", expected_qr);
    getInput("timeout", timeout);

    auto start_time = std::chrono::steady_clock::now();
    bool qr_matched = false;

    while (std::chrono::steady_clock::now() - start_time < std::chrono::seconds(timeout)) {
        if (qr_data_ == expected_qr) {
            qr_matched = true;
            break;
        }
        rclcpp::spin_some(node_);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));  // Prevent busy loop
    }

    if (qr_matched) {
        RCLCPP_INFO(node_->get_logger(), "QR code matched: %s", expected_qr.c_str());
        return BT::NodeStatus::SUCCESS;
    } else {
        RCLCPP_WARN(node_->get_logger(), "QR code did not match within timeout: %s", expected_qr.c_str());
        return BT::NodeStatus::FAILURE;
    }
}

PushToStack::PushToStack(const std::string& name, const BT::NodeConfiguration& config)
    : BT::SyncActionNode(name, config) {}

BT::PortsList PushToStack::providedPorts() {
    return {BT::InputPort<std::string>("value")};
}

BT::NodeStatus PushToStack::tick() {
    std::string value;
    getInput("value", value);
    stack_t.push(value);  // Push goal into stack
    RCLCPP_INFO(node_->get_logger(), "Pushed goal: %s", value.c_str());
    return BT::NodeStatus::SUCCESS;
}

ProcessStack::ProcessStack(const std::string& name, const BT::NodeConfiguration& config)
    : BT::SyncActionNode(name, config) {}

BT::PortsList ProcessStack::providedPorts() {
    return {};
}

BT::NodeStatus ProcessStack::tick() {
    if (!stack_t.empty()) {
        std::string goal = stack_t.top();
        stack_t.pop();
        // Move robot to goal
        RCLCPP_INFO(node_->get_logger(), "Moving to goal: %s", goal.c_str());
        return BT::NodeStatus::SUCCESS;
    }
    return BT::NodeStatus::FAILURE;
}

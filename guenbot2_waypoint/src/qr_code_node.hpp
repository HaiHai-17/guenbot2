#ifndef QR_CODE_NODE_HPP
#define QR_CODE_NODE_HPP

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "behaviortree_cpp_v3/action_node.h"
#include <stack>

class CheckQRCode : public BT::SyncActionNode {
public:
    CheckQRCode(const std::string& name, const BT::NodeConfiguration& config);
    static BT::PortsList providedPorts();
    BT::NodeStatus tick() override;

private:
    rclcpp::Node::SharedPtr node_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr qr_sub_;
    std::string qr_data_;
};

#endif // QR_CODE_NODE_HPP

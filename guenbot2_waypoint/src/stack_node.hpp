#include "behaviortree_cpp_v3/action_node.h"
#include <stack>

class PushToStack : public BT::SyncActionNode {
public:
    PushToStack(const std::string& name, const BT::NodeConfiguration& config)
        : BT::SyncActionNode(name, config) {}

    static BT::PortsList providedPorts() {
        return {BT::InputPort<std::string>("value")};
    }

    BT::NodeStatus tick() override {
        std::string value;
        getInput("value", value);
        stack_.push(value); // Push goal into stack
        return BT::NodeStatus::SUCCESS;
    }

    std::stack<std::string> stack_;
};

class ProcessStack : public BT::SyncActionNode {
public:
    ProcessStack(const std::string& name, const BT::NodeConfiguration& config)
        : BT::SyncActionNode(name, config) {}

    static BT::PortsList providedPorts() {
        return {};
    }

    BT::NodeStatus tick() override {
        if (!stack_.empty()) {
            std::string goal = stack_.top();
            stack_.pop();
            // Move robot to goal
            RCLCPP_INFO(node_->get_logger(), "Moving to goal: %s", goal.c_str());
            return BT::NodeStatus::SUCCESS;
        }
        return BT::NodeStatus::FAILURE;
    }

    std::stack<std::string> stack_;
    rclcpp::Node::SharedPtr node_;
};

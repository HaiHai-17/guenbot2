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
        stack_t.push(value); // Push goal into stack
        return BT::NodeStatus::SUCCESS;
    }

    static std::stack<std::string> stack_t; // Declare static stack
};

class ProcessStack : public BT::SyncActionNode {
public:
    ProcessStack(const std::string& name, const BT::NodeConfiguration& config)
        : BT::SyncActionNode(name, config) {}

    static BT::PortsList providedPorts() {
        return {};
    }

    BT::NodeStatus tick() override {
        if (!stack_t.empty()) {
            std::string goal = stack_t.top();
            stack_t.pop();
            // Move robot to goal
            RCLCPP_INFO(node_->get_logger(), "Moving to goal: %s", goal.c_str());
            return BT::NodeStatus::SUCCESS;
        }
        return BT::NodeStatus::FAILURE;
    }

    static std::stack<std::string> stack_t; // Declare static stack
    rclcpp::Node::SharedPtr node_;
};

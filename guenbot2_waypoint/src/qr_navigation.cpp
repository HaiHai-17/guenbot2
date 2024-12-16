#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "behaviortree_cpp_v3/bt_factory.h"
#include "nav2_client.hpp"
#include <tinyxml2.h>
#include <mutex>

class QRNavigation : public rclcpp::Node
{
public:
    QRNavigation() : Node("qr_navigation")
    {
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "/barcode", 10, std::bind(&QRNavigation::qr_callback, this, std::placeholders::_1));

        factory_.registerNodeType<Nav2Client>("Nav2Client");

        load_goals_from_xml("/home/guen/guenbot2_ws/src/guenbot2_waypoint/waypoint_xml/guen_nav_mememan.xml");
    }

private:
    void load_goals_from_xml(const std::string &xml_path)
    {
        tinyxml2::XMLDocument doc;
        if (doc.LoadFile(xml_path.c_str()) != tinyxml2::XML_SUCCESS)
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to load XML file: %s", xml_path.c_str());
            return;
        }

        auto root = doc.RootElement();
        if (!root)
        {
            RCLCPP_ERROR(this->get_logger(), "Invalid XML file: %s", xml_path.c_str());
            return;
        }

        auto behavior_tree = root->FirstChildElement("BehaviorTree");
        if (!behavior_tree)
        {
            RCLCPP_ERROR(this->get_logger(), "No BehaviorTree element found in XML file: %s", xml_path.c_str());
            return;
        }

        parse_sequence(behavior_tree);
    }

    void parse_sequence(tinyxml2::XMLElement *element)
    {
        for (auto child = element->FirstChildElement(); child; child = child->NextSiblingElement())
        {
            if (std::string(child->Name()) == "SetBlackboard")
            {
                const char *key = child->Attribute("output_key");
                const char *value = child->Attribute("value");
                if (key && value)
                {
                    std::lock_guard<std::mutex> lock(goal_mutex_);
                    goals_[key] = value;
                    RCLCPP_INFO(this->get_logger(), "Loaded goal: %s -> %s", key, value);
                }
            }
            else
            {
                parse_sequence(child); // Recursively parse child elements
            }
        }
    }

    void qr_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        std::string qr_data = msg->data;
        std::string goal;

        {
            std::lock_guard<std::mutex> lock(goal_mutex_);
            if (goals_.find("Goal_" + qr_data) != goals_.end())
            {
                goal = goals_["Goal_" + qr_data];
            }
            else
            {
                RCLCPP_WARN(this->get_logger(), "Unknown QR code data: %s", qr_data.c_str());
                return;
            }
        }

        // Check goal data format
        if (goal.empty())
        {
            RCLCPP_WARN(this->get_logger(), "Goal is empty for QR data: %s", qr_data.c_str());
            return;
        }

        if (std::count(goal.begin(), goal.end(), ';') != 3)
        {
            RCLCPP_ERROR(this->get_logger(), "Invalid goal format: %s", goal.c_str());
            return;
        }

        // Create behavior tree with goal data
        auto tree = factory_.createTreeFromText(
            R"(
            <root main_tree_to_execute = "MainTree">
                <BehaviorTree ID="MainTree">
                    <Sequence>
                        <Nav2Client goal=")" + goal + R"(" />
                    </Sequence>
                </BehaviorTree>
            </root>
            )");

        while (rclcpp::ok() && tree.tickRoot() == BT::NodeStatus::RUNNING)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
    BT::BehaviorTreeFactory factory_;
    std::map<std::string, std::string> goals_;
    std::mutex goal_mutex_; // Protect access to goals_
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<QRNavigation>();

    // Wait for 10 seconds for data from /barcode
    auto start_time = std::chrono::steady_clock::now();
    while (rclcpp::ok() && std::chrono::steady_clock::now() - start_time < std::chrono::seconds(10))
    {
        rclcpp::spin_some(node);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    rclcpp::shutdown();
    return 0;
}

import rclpy
import math
import cv2
from pyzbar.pyzbar import decode
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator

def scan_qr_code():
    cap = cv2.VideoCapture('/dev/video0')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    if not cap.isOpened():
        print("Camera không kết nối được.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không đọc được khung hình từ camera.")
            continue

        qr_codes = decode(frame)
        for qr in qr_codes:
            try:
                qr_data = qr.data.decode('utf-8')
                x, y, rotation = map(float, qr_data.split())
                print(f"Waypoint: x={x}, y={y}, rotation={rotation}")
                cap.release()
                cv2.destroyAllWindows()
                return x, y, rotation
            except ValueError:
                print("Dữ liệu QR không hợp lệ.")
        
        cv2.imshow('Scan QR Code', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

def main():
    rclpy.init()
    navigator = BasicNavigator()

    print("Chờ Nav2 khởi động...")
    navigator.waitUntilNav2Active()

    while rclpy.ok():
        qr_data = scan_qr_code()
        if qr_data is None:
            print("Không tìm thấy QRCode hợp lệ. Thử lại...")
            continue

        x, y, rotation = qr_data

        # Tính toán pose
        rotrot = 360 - rotation
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = navigator.get_clock().now().to_msg()

        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.z = math.sin(math.radians(rotrot) / 2)
        pose.pose.orientation.w = math.cos(math.radians(rotrot) / 2)

        # Điều khiển robot tới waypoint
        navigator.followWaypoints([pose])

        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            if feedback:
                print(f'Waypoint {feedback.current_waypoint + 1} đang xử lý.')

        print("Hoàn thành waypoint. Chờ QRCode tiếp theo...")

if __name__ == '__main__':
    main()


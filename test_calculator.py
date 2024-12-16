import subprocess
import pyautogui
import time

def open_calculator():
    """
    Mở ứng dụng Calculator dựa trên hệ điều hành.
    """
    try:
        # Kiểm tra hệ điều hành
        import platform
        os_name = platform.system()

        if os_name == "Windows":
            # Mở Calculator trên Windows
            subprocess.Popen("calc.exe")
        elif os_name == "Darwin":  # macOS
            # Mở Calculator trên macOS
            subprocess.Popen(["open", "-a", "Calculator"])
        else:
            raise NotImplementedError("Hệ điều hành không được hỗ trợ.")

        time.sleep(2)  # Chờ Calculator mở
        print("Calculator đã được mở.")
    except Exception as e:
        print(f"Không thể mở Calculator: {e}")


def test_addition():
    """
    Test phép cộng trên Calculator.
    """
    # Mở Calculator
    open_calculator()

    # Nhập số 7
    pyautogui.press('7')
    time.sleep(0.5)

    # Nhấn nút +
    pyautogui.press('+')
    time.sleep(0.5)

    # Nhập số 3
    pyautogui.press('3')
    time.sleep(0.5)

    # Nhấn nút =
    pyautogui.press('enter')
    time.sleep(0.5)

    # Lấy kết quả từ Calculator (kiểm tra thủ công vì pyautogui không đọc nội dung).
    print("Đã thực hiện phép tính 7 + 3. Vui lòng kiểm tra kết quả trên màn hình Calculator.")

    # Đóng ứng dụng Calculator
    close_calculator()

def close_calculator():
    """
    Đóng ứng dụng Calculator dựa trên hệ điều hành.
    """
    import os
    os_name = platform.system()
    if os_name == "Windows":
        subprocess.call(["taskkill", "/F", "/IM", "Calculator.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif os_name == "Darwin":  # macOS
        subprocess.call(["osascript", "-e", 'quit app "Calculator"'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("Không thể tự động đóng Calculator trên hệ điều hành này.")

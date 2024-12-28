import random
import subprocess

def calculate_luhn_check_digit(imei):
    sum_digits = 0
    for i in range(14):
        digit = imei[i]
        if i % 2 == 1:  # If the position is odd (0-based index), double it
            digit *= 2
            if digit > 9:
                digit -= 9
        sum_digits += digit
    return (10 - (sum_digits % 10)) % 10

def generate_imei():
    imei = [random.randint(0, 9) for _ in range(14)]
    imei.append(calculate_luhn_check_digit(imei))
    return ''.join(map(str, imei))

def ThietLapThongSoThietbi(index):
    resolutions = [
        (1080, 1920),
        (900, 1600),
        (720, 1280),
        (540, 960),
        (1440, 2560),  # Additional common phone resolutions
        (1080, 2400),
        (720, 1520)
    ]

    manufacturers_and_models = {
        "samsung": [
            "SM-S908B", "SM-S908N",
            "SM-S901B", "SM-S901N",
            "SM-S906B", "SM-S906N",
            "SM-G977B", "SM-G977N",
            "SM-G973F", "SM-G973N",
            "SM-G975F", "SM-G975N",
            "SM-G970F", "SM-G970N",
            "SM-N970F", "SM-N970N",
            "SM-N975F", "SM-N975N",
            "SM-N960F", "SM-N960N",
            "SM-G965F", "SM-G965N",
            "SM-G960F", "SM-G960N",
            "SM-A908B", "SM-A908N"
        ],
        "Xiaomi": ["M2102K1G", "M2011K2G", "M1910F4G", "M2102J20SG"],
        "Redmi": ["M2101K7AG", "M2101K9G", "2201116PG", "M2101K6G"],
        "Google phone": ["GB7N6", "G1F8F", "GVU6C", "GLU0G"],
        "ROG": ["ZS676KS", "I003D", "ZS660KL"],
        "OnePlus": ["DN2101", "LE2100", "LE2113", "LE2123"],
        "SONY": ["XQ-AT52", "XQ-BT52", "XQ-DQ52"],
        "AQUOS": ["SH-51B", "SH-01K", "SH-41A"],
        "vivo": ["V2145", "V2130", "V2150", "V2135"],
        "OPPO": ["CPH2023", "CPH2197", "CPH2357", "CPH2239", "CPH2389"],
        "HUAWEI": ["MSC-AL09", "BAL-AL00", "OXF-AN00", "LGE-AN10", "LGE-AN00"],
        "blackshark": ["SHARK KTUS-H0"],
        "asus": ["ASUS_I001DA"],
    }

    manufacturer = random.choice(list(manufacturers_and_models.keys()))
    model = random.choice(manufacturers_and_models[manufacturer])
    resolution = random.choice(resolutions)
    cpu_cores = random.randint(1, 3)
    ram = random.choice([2048, 4096])
    imei = generate_imei()

    device = {
        "manufacturer": manufacturer,
        "model": model,
        "resolution": f"{resolution[0]}x{resolution[1]}",
        "cpu_cores": cpu_cores,
        "ram": ram,
        "imei": imei
    }

    try:
        # Command to set LDPlayer properties using ldconsole.exe modify
        modify_command = [
            "ldconsole.exe", "modify", "--index", f"{index}",
            "--cpu", f"{device['cpu_cores']}",
            "--memory", f"{device['ram']}",
            "--imei", f"{device['imei']}",
            "--manufacturer", f"{device['manufacturer']}",
            "--model", f"{device['model']}",
            "--pnumber", "13812345678"  # Example phone number
        ]
        subprocess.run(modify_command, check=True)
        # print(f"{index} Modify command:", " ".join(modify_command))
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to set device properties: {e}")
        return False
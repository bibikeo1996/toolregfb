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
    return "".join(map(str, imei))


def ThietLapThongSoThietbi(index, ld_path_console):
    resolutions = [
        (1080, 1920),
        (900, 1600),
        (720, 1280),
        (540, 960),
        (1440, 2560),  # Additional common phone resolutions
        (1080, 2400),
        (720, 1520),
    ]

    manufacturers_and_models = {
        "samsung": [
            "SM-S9180",
            "SM-X910N",
            "SM-X810N",
            "SM-X710N",
            "SM-S906B",
            "SM-S906N",
            "SM-S9280",
            "SM-S9260",
            "SM-S9210",
            "SM-S9160",
            "SM-S9110",
            "SM-N9860",
            "SM-N9810",
        ],
        "Xiaomi": ["23116PN5BC", "23127PN0CC", "2304FPN6DG", "2210132C", "2211133C", "2203121C", "MI 9"],
        "Redmi": ["23133RKC6C", "2311DRK48C", "22127RK46C", "23078RKD5C", "22081212C"],
        "Google phone": ["G576D", "GFE4J", "G82U8"],
        "ROG": ["ASUS_AI2401_A", "ROG Phone 7 Ultimate", "ASUS_AI2205_A", "ASUS AI2201_B"],
        "OnePlus": ["PJD110", "PHB110", "NE210", "HD1910", "HD1900", "GM1910", "GM1900"],
        "SONY": ["XQ-BE42", "XQ-AQ05", "SO-41B", "SO-02L", "SOV44"],
        "AQUOS": ["A208SH", "SH-M24", "SHG07"],
        "vivo": ["V2329A", "V2307A", "V2218A", "V2217A", "V2324A", "V2309A", "V2266A", "V2229A", "V2242A", "V2241A", "V2339A", "V2338A"],
        "OPPO": ["PJJ110", "PJH110", "PHW110", "PHM110", "PHY110", "PHZ110", "PGEM10", "PGFM10"],
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
        "imei": imei,
    }

    try:
        # Command to set LDPlayer properties using ldconsole.exe modify
        modify_command = [
            ld_path_console,
            "modify",
            "--index",
            f"{index}",
            "--cpu",
            f"{device['cpu_cores']}",
            "--memory",
            f"{device['ram']}",
            "--imei",
            f"{device['imei']}",
            "--manufacturer",
            f"{device['manufacturer']}",
            "--model",
            f"{device['model']}",
            "--pnumber",
            "13812345678",  # Example phone number
        ]
        subprocess.run(modify_command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to set device properties: {e}")
        return False

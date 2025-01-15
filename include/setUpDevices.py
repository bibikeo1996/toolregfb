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

def GetPhone(country):
    if country == "VN":
        prefix = random.choice(["077", "093"])
        random_phone_number = prefix + ''.join(random.choices('0123456789', k=7))
    elif country == "USA":
        area_code = random.choice([
            "201", "305", "408", "617", "702", "818", "203", "860", "475", "959", "207", 
            "339", "351", "413", "617", "508", "774", "781", "857", "978", "603", "201", "551", "609", 
            "640", "732", "848", "856", "862", "908", "973", "212", "315", "332", "347", "516", "518", "585", 
            "607", "631", "646", "680", "716", "718", "838", "845", "914", "917", "929", "934", "401", "215", 
            "223", "267", "272", "412", "484", "610", "717", "724", "814", "878", "802", "217", "224", "309", 
            "312", "331", "630", "618", "708", "773", "779", "815", "847", "872", "219", "260", "317", "765", 
            "574", "812", "930", "319", "515", "563", "641", "712", "316", "620", "785", "913", "231", "248", 
            "269", "313", "586", "517", "616", "734", "810", "906", "947", "989", "679", "218", "320", "507", 
            "612", "651", "763", "952", "314", "417", "573", "636", "660", "816", "308", "402", "531", "701", 
            "216", "234", "326", "330", "380", "419", "440", "513", "567", "614", "740", "937", "220", "605", 
            "262", "414", "608", "534", "715", "920", "274", "205", "251", "256", "334", "938", "479", "501", 
            "870", "302", "239", "305", "321", "352", "386", "407", "686", "561", "727", "754", "772", "786", 
            "813", "850", "863", "904", "941", "954", "229", "404", "470", "478", "678", "706", "762", "770", 
            "912", "270", "364", "606", "502", "859", "225", "318", "337", "504", "985", "240", "301", "410", 
            "443", "667", "228", "601", "662", "769", "252", "336", "704", "743", "828", "910", "919", "980", 
            "984", "405", "580", "918", "539", "803", "843", "854", "864", "423", "615", "629", "731", "865", 
            "901", "931", "210", "214", "254", "325", "281", "346", "361", "409", "430", "432", "469", "512", 
            "682", "713", "726", "737", "806", "817", "830", "832", "903", "915", "936", "940", "956", "972", 
            "979", "276", "434", "540", "571", "703", "757", "804", "304", "681", "907", "479", "501", "870", 
            "209", "213", "279", "310", "323", "341", "408", "415", "424", "442", "510", "530", "559", "562", 
            "619", "626", "628", "650", "657", "661", "669", "707", "714", "747", "760", "805", "818", "820", 
            "831", "858", "909", "916", "925", "949", "951", "303", "719", "720", "970", "808", "208", "986", 
            "406", "702", "725", "775", "505", "575", "503", "541", "971", "458", "435", "801", "385", "206", 
            "253", "360", "425", "509", "564", "307"
        ])
        central_office_code = ''.join(random.choices('0123456789', k=3))
        line_number = ''.join(random.choices('0123456789', k=4))
        random_phone_number = f"+1 {area_code} {central_office_code} {line_number}"
    else:
        raise ValueError("Unsupported country. Please use 'VN' or 'USA'.")
    
    return random_phone_number

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
            "",
            # GetPhone(),
        ]
        subprocess.run(modify_command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to set device properties: {e}")
        return False

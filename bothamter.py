

from httpcore import ProxyError
import requests
import json
import time
import random
import base64
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style
from fake_useragent import UserAgent
from requests_html import HTMLSession
import logging
from requests.exceptions import RequestException

import configparser

config = configparser.ConfigParser()
config.read('config.txt', encoding='utf-8')

# Đọc các giá trị từ config
auto_check_task_list = config.get('DEFAULT', 'auto_check_task_list')
auto_attendance = config.get('DEFAULT', 'auto_attendance')
auto_morse = config.get('DEFAULT', 'auto_morse')
auto_claim_combo = config.get('DEFAULT', 'auto_claim_combo')
max_card_price = config.getint('DEFAULT', 'max_card_price')
auto_minigame = config.get('DEFAULT', 'auto_minigame')
auto_upgrade_multitap = config.get('DEFAULT', 'auto_upgrade_multitap')
lv_upgrade_multitap = config.getint('DEFAULT', 'lv_upgrade_multitap')
auto_upgrade_energy = config.get('DEFAULT', 'auto_upgrade_energy')
lv_upgrade_energy = config.getint('DEFAULT', 'lv_upgrade_energy')
auto_upgrade_pph = config.get('DEFAULT', 'auto_upgrade_pph')
max_price = config.getint('DEFAULT', 'max_price')
wait_cooldown = config.get('DEFAULT', 'wait_cooldown')
max_wait_cooldown = config.getint('DEFAULT', 'max_wait_cooldown')
delay_between_accounts = config.get('DEFAULT', 'delay_between_accounts')
max_delay_between_accounts = config.getint('DEFAULT', 'max_delay_between_accounts')


session = HTMLSession()
ua = UserAgent()
# Initialize colorama
init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_proxies():
    with open('proxy.txt', 'r') as proxy_file:
        return [proxy.strip() for proxy in proxy_file.readlines()]

def DailyCipherDecode(cipher):
    cipher = cipher[:3] + cipher[4:]
    cipher = cipher.encode("ascii")
    cipher = base64.b64decode(cipher)
    cipher = cipher.decode("ascii")
    return cipher

def read_promo_keys():
    with open('voucher.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]
    
def categorize_promo_codes(promo_keys):
    categories = {
        'BIKE': [], 'CUBE': [], 'TRAIN': [], 'CLONE': []
    }
    for key in promo_keys:
        for category in categories:
            if key.startswith(category):
                categories[category].append(key)
                break
    return categories

def remove_promo_key(used_key):
    with open('voucher.txt', 'r') as file:
        lines = file.readlines()
    with open('voucher.txt', 'w') as file:
        file.writelines([line for line in lines if line.strip() != used_key])

def apply_promo(session, token):
    promo_keys = read_promo_keys()
    categories = categorize_promo_codes(promo_keys)
    successful_keys = []
    
    for category in ['BIKE', 'CUBE', 'TRAIN', 'CLONE']:
        attempts = 0
        while attempts < 4 and categories[category]:
            promo_key = categories[category].pop(0)
            url = "https://api.hamsterkombatgame.io/clicker/apply-promo"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {"promoCode": promo_key}
            try:
                response = session.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    print(f"Successfully applied promo code: {promo_key}")
                    successful_keys.append(promo_key)
                    attempts += 1
                else:
                    print(f"Failed to apply promo code: {promo_key}")
                    categories[category].append(promo_key)  # Add failed key back to the category
                    break  # Move to next category on failure
            except RequestException as e:
                print(f"Error applying promo code: {e}")
                categories[category].append(promo_key)  # Add failed key back to the category
                break  # Move to next category on error
    
    # Remove successful keys from voucher.txt
    for key in successful_keys:
        remove_promo_key(key)
    
    # Update voucher.txt with remaining keys
    remaining_keys = [key for cat in categories.values() for key in cat]
    with open('voucher.txt', 'w') as file:
        for key in remaining_keys:
            file.write(f"{key}\n")



def TextToMorseCode(text):
    morse_code = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", 
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", 
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", 
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", 
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---", 
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", 
        "8": "---..", "9": "----.", " ": "/", ".": ".-.-.-", ",": "--..--", 
        "?": "..--..", "'": ".----.", "!": "-.-.--", "/": "-..-.", "(": "-.--.", 
        ")": "-.--.-", "&": ".-...", ":": "---...", ";": "-.-.-.", "=": "-...-", 
        "+": ".-.-.", "-": "-....-", "_": "..--.-", '"': ".-..-.", "$": "...-..-", 
        "@": ".--.-.",
    }
    text = text.upper()
    morse = ""
    for char in text:
        if char in morse_code:
            morse += morse_code[char] + " "
    return morse

def countdown(t):
    while t:
        minutes, seconds = divmod(t, 60)
        minutes = str(minutes).zfill(2)
        seconds = str(seconds).zfill(2)
        print(Fore.CYAN + Style.BRIGHT + f"[ Countdown	] : Wait for {minutes}:{seconds} seconds                                     ", flush=True, end="\r")
        time.sleep(1)
        t -= 1
    print("                                        ", flush=True, end="\r")  

def separator(data):
    separated = '{:,}'.format(int(data))
    return separated	

def load_tokens(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

def get_headers(token: str, proxy: str) -> dict:
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua.random,
        'Content-Type': 'application/json'
    }
    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    return headers, proxies

def get_token(init_data_raw, proxy, max_retries=3):
    url = 'https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': ua.random,
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    data = json.dumps({"initDataRaw": init_data_raw})
    
    for attempt in range(max_retries):
        try:
            res = session.post(url, headers=headers, data=data, proxies=proxies, timeout=10)
            res.raise_for_status()
            
            if res.text.strip():
                return res.json()['authToken']
            else:
                logging.warning(f"Empty response received on attempt {attempt + 1}")
        except (RequestException, json.JSONDecodeError) as e:
            logging.error(f"Error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                logging.error("Max retries reached. Unable to get token.")
    
        except ProxyError:
            logging.warning("Proxy error encountered. Skipping to next proxy-account pair.")
            return None

		
def authenticate(token, proxy):
    url = 'https://api.hamsterkombatgame.io/auth/me-telegram'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    return response

def sync_clicker(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/sync'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    return response

def claim_daily(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers, proxies = get_headers(token, proxy)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    return response

def upgrade(token, upgrade_type, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers, proxies = get_headers(token, proxy)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    return response

def tap(token, max_taps, available_taps, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/tap'
    headers, proxies = get_headers(token, proxy)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    return response

def list_tasks(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/list-tasks'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    return response

def get_combo(item):
    url = "https://raw.githubusercontent.com/unadavina/hk/main/combo"
    request = requests.get(url)
    CurrentCombo = request.text
    ComboList = CurrentCombo.split()
    if item == "item":
        Combo_List = [ComboList[0], ComboList[1], ComboList[2]]
    else:
        Combo_List = ComboList[4]
    return Combo_List

def start_minigame(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/start-keys-minigame'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    return response

def claim_MiniGame(token, delay, iduser, proxy):
    random_prefix = '0' + str(delay) + str(random.randint(10000000000, 99999999999))[:10]
    cipher = f'{random_prefix}|{iduser}'
    base64_cipher = base64.b64encode(cipher.encode()).decode()
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame'
    headers, proxies = get_headers(token, proxy)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"cipher": base64_cipher})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    if response.status_code == 200:
        try:
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 400:
        try:
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 500:
        print(Fore.RED + Style.BRIGHT + f"Failed to claim MiniGame, Internal Server Error", flush=True)
        return response
    else:
        print(Fore.RED + Style.BRIGHT + f"Failed to claim MiniGame, status code: {response.status_code}", flush=True)
        return None

def get_ip(token, proxy):
    url = 'https://api.hamsterkombatgame.io/ip'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        try:
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 400:
        try:
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 500:
        print(Fore.RED + Style.BRIGHT + f"Failed to get IP, Internal Server Error", flush=True)
        return response
    else:
        print(Fore.RED + Style.BRIGHT + f"Failed to get IP, status code: {response.status_code}", flush=True)
        return None

def GetAccountConfigRequest(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/config'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    return response

def exchange(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/select-exchange'
    headers, proxies = get_headers(token, proxy)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"exchangeId": 'binance'})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    return response

def claim_cipher(token, DailyMorse, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-cipher'
    headers, proxies = get_headers(token, proxy)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"cipher": DailyMorse})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    
    if response.status_code == 200:
        try:
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 400:
        try:
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 500:
        print(Fore.RED + Style.BRIGHT + f"Failed to claim cipher, Internal Server Error", flush=True)
        return response
    else:
        print(Fore.RED + Style.BRIGHT + f"Failed to claim cipher, status code: {response.status_code}", flush=True)
        return None

def check_task(token, task_id, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/check-task'
    headers, proxies = get_headers(token, proxy)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    return response

def check_booster(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/boosts-for-buy'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    return response

def use_booster(token, idboost, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-boost'
    headers, proxies = get_headers(token, proxy)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": idboost, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    return response

def read_upgrade_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_available_upgrades(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade	] : Failed to get JSON response.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Failed to get upgrade list: Status {response.status_code}", flush=True)
        return []

def buy_upgrade(token, upgrade_id, upgrade_name, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers, proxies = get_headers(token, proxy)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    time.sleep(3)
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade	] : Successfully upgraded...", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade	] : Failed to parse JSON during upgrade.", flush=True)
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Not enough coins :V                             ", flush=True)
                return 'insufficient_funds'
            elif error_response.get('error_code') == 'UPGRADE_COOLDOWN':
                cooldown_seconds = error_response.get('cooldownSeconds', 0)
                minutes, seconds = divmod(cooldown_seconds, 60)
                hours, minutes = divmod(minutes, 60)
                hours = str(hours).zfill(2)
                minutes = str(minutes).zfill(2)
                seconds = str(seconds).zfill(2)
                print(Fore.BLUE + f"\r[ Upgrade	] : {upgrade_name} COOLDOWN: {hours} Hours {minutes} Minutes {seconds} Seconds.", flush=True)
                return {'cooldown': True, 'cooldown_seconds': cooldown_seconds}
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Failed upgrade {upgrade_name}: {error_response}", flush=True)
                return {'error': True, 'message': error_response}
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : Failed to get JSON response. Status: {response.status_code}", flush=True)
            return {'error': True, 'status_code': response.status_code}

def get_available_upgrades_combo(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo	] : Successfully got upgrade list.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo	] : Failed to get JSON response.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Failed to get upgrade list: Status {response.status_code}", flush=True)
        return []

def buy_upgrade_combo(token, upgrade_id, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/buy-upgrade'
    headers, proxies = get_headers(token, proxy)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = session.post(url, headers=headers, data=data, proxies=proxies)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo	] : Combo {upgrade_id} successfully purchased.", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo	] : Failed to parse JSON during upgrade.", flush=True)
        return response
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Not enough coins.", flush=True)
                return 'insufficient_funds'
            else:
                return error_response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Failed to get JSON response. Status: {response.status_code}", flush=True)
            return None

def auto_upgrade_pph_earn(token, max_price, proxy):
    insufficient_funds = False
    cooldown_upgrades = {}

    while not insufficient_funds:
        available_upgrades = get_available_upgrades(token, proxy)
        best_upgrade = None
        best_value = 0

        current_time = time.time()
        for upgrade in available_upgrades:
            if upgrade['isAvailable'] and not upgrade['isExpired']:
                if upgrade['id'] in cooldown_upgrades and current_time < cooldown_upgrades[upgrade['id']]:
                    if wait_cooldown == 'y':
                        if cooldown_seconds <= max_wait_cooldown:
                            countdown(cooldown_seconds)
                        else:
                            continue
                    else:
                        continue

                price = upgrade['price']
                if price > max_price:
                    continue

                profit_per_hour = upgrade['profitPerHour']
                try:
                    value = profit_per_hour / price
                except ZeroDivisionError:
                   value = 0

                if value > best_value:
                    best_value = value
                    best_upgrade = upgrade

        if best_upgrade:
            print(Fore.CYAN + Style.BRIGHT + f"\r[ Upgrade	] : Card: {best_upgrade['name']} | PPH+: {separator(best_upgrade['profitPerHour'])} | Price: {separator(best_upgrade['price'])}", flush=True)
            result = buy_upgrade(token, best_upgrade['id'], best_upgrade['name'], proxy)
            if result == 'insufficient_funds':
                print(Fore.RED + Style.BRIGHT + "[ Upgrade	] : Not enough coins.", flush=True)
                insufficient_funds = True
            elif isinstance(result, dict) and 'cooldown' in result:
                cooldown_seconds = result['cooldown_seconds']
                cooldown_end_time = current_time + cooldown_seconds
                cooldown_upgrades[best_upgrade['id']] = cooldown_end_time
            elif isinstance(result, dict) and 'error' in result:
                print(Fore.RED + Style.BRIGHT + f"[ Upgrade	] : Failed to upgrade with error: {result.get('message', 'No error message provided')}", flush=True)
        else:
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade	] : No upgrades meet the criteria at this time.       ", flush=True)
            break


def check_and_upgrade(token, upgrade_id, required_level, proxy):
    upgrades = get_available_upgrades_combo(token, proxy)
    if upgrades:
        for upgrade in upgrades:
            if upgrade['id'] == upgrade_id and upgrade['level'] < required_level + 1:
                print(Fore.CYAN + Style.BRIGHT + f"[ Daily Combo	] : Upgrading {upgrade_id}", end="", flush=True)
                req_level_total = required_level + 1
                for _ in range(req_level_total - upgrade['level']):
                    result = buy_upgrade_combo(token, upgrade_id, proxy)
                    if isinstance(result, dict) and 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                        needed_upgrade = result['error_message'].split(':')[-1].strip().split()
                        needed_upgrade_id = needed_upgrade[1]
                        needed_upgrade_level = int(needed_upgrade[-1])
                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Daily Combo	] : Trying to buy {needed_upgrade_id} level {needed_upgrade_level}", end="", flush=True)
                        if check_and_upgrade(token, needed_upgrade_id, needed_upgrade_level, proxy):
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo	] : Successfully upgraded {needed_upgrade_id} to level {needed_upgrade_level}. Trying to upgrade {upgrade_id} again.", flush=True)
                            continue
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Failed to upgrade {needed_upgrade_id} to level {needed_upgrade_level}", flush=True)
                            return False
                    elif result == 'insufficient_funds':
                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Not enough coins to upgrade {upgrade_id}", flush=True)
                        return False
                    elif result.status_code != 200:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Failed to upgrade {upgrade_id} with error: {result}", flush=True)
                        return False
                print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo	] : Upgrade {upgrade_id} successfully done to level {required_level}", flush=True)
                return True
    return False

def claim_daily_combo(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/claim-daily-combo'
    headers, proxies = get_headers(token, proxy)
    headers['Content-Length'] = '0'
    
    response = session.post(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo	] : Successfully claimed daily combo.                                          ", flush=True)
        return response.json()
    else:
        error_response = response.json()
        if error_response.get('error_code') == 'DAILY_COMBO_DOUBLE_CLAIMED':
            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo	] : Combo has already been claimed          ", flush=True)
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo	] : Buy Combo first...", flush=True)
        return error_response
    
def check_combo_purchased(token, proxy):
    url = 'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy'
    headers, proxies = get_headers(token, proxy)
    response = session.post(url, headers=headers, proxies=proxies)
    if response.status_code == 200:
        data = response.json()
        purchased_combos = data.get('dailyCombo', {}).get('upgradeIds', [])
        return purchased_combos
    else:
        print(Fore.RED + Style.BRIGHT + f"Failed to get combo status. Status: {response.status_code}", flush=True)
        return None

# MAIN CODE
check_task_dict = {}
claimed_ciphers = set()
claimed_minigame = set()
combo_upgraded = {}

def main():
    global check_task_dict, claimed_ciphers, claimed_minigame, auto_claim_combo, combo_upgraded
    
    print_welcome_message()
    print(Fore.GREEN + Style.BRIGHT + "Bot is running....")
    init_data = load_tokens('initdata.txt')
    proxies = load_proxies()
    token_cycle = cycle(zip(init_data, proxies))

    token_dict = {}
    while True:
        try:
            init_data_raw, proxy = next(token_cycle)
            token = token_dict.get(init_data_raw)
            minigame_delay = random.randint(7, 15)
            
            if token:
                print(Fore.RED + Style.BRIGHT + f"\n\n\n\rAccount: Previously botted", flush=True)
                if delay_between_accounts == "y":
                    delay = random.randint(1, max_delay_between_accounts)
                else:
                    delay = 0   
                countdown(delay)
            else:
                token = get_token(init_data_raw, proxy)
                if token is None:
                    print(Fore.RED + Style.BRIGHT + f"\rSkipping to next account due to proxy error\n", flush=True)
                    continue
                if token:
                    token_dict[init_data_raw] = token
                    print(Fore.GREEN + Style.BRIGHT + f"\n\n\rAccount: Active", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\rSwitching to next account\n", flush=True)
                    continue

            apply_promo(session, token)

            if init_data_raw not in combo_upgraded:
                combo_upgraded[init_data_raw] = False

            response = authenticate(token, proxy)
   
            if response.status_code == 200:
                user_data = response.json()
                username = user_data.get('telegramUser', {}).get('username', 'Empty Username')
                firstname = user_data.get('telegramUser', {}).get('firstName', 'Empty')
                lastname = user_data.get('telegramUser', {}).get('lastName', 'Empty')
                print(Fore.GREEN + Style.BRIGHT + f"~~~~~~[{Fore.WHITE + Style.BRIGHT} {username} | {firstname} {lastname} {Fore.GREEN + Style.BRIGHT}]~~~~~~")
                print(Fore.CYAN + Style.BRIGHT + f"\r[ IP Info	] : Getting IP information...", end="", flush=True)
                response = get_ip(token, proxy)
                if response.status_code == 200:
                    ip_data = response.json()
                    print(Fore.CYAN + Style.BRIGHT + f"\r[ IP Info	] : IP: {ip_data['ip']} | ISP: {ip_data['asn_org']} | Country: {ip_data['country_code']}",  flush=True)
                
                print(Fore.CYAN + Style.BRIGHT + f"\r[ Account id	] : Getting USER information...", end="", flush=True)
                response = sync_clicker(token, proxy)
                if response.status_code == 200:
                    clicker_data = response.json()['clickerUser']
                    iduser=clicker_data['id']
                    print(Fore.CYAN + Style.BRIGHT + f"\r[ Account id	] : {iduser}                      ", flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Level		] : {clicker_data['level']}", flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Total Earned	] : {separator(clicker_data['totalCoins'])}", flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Coin		] : {separator(clicker_data['balanceCoins'])}", flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Energy	] : {separator(clicker_data['availableTaps'])}", flush=True)
                    boosts = clicker_data['boosts']
                    boost_max_taps_level = boosts.get('BoostMaxTaps', {}).get('level', 0)
                    boost_earn_per_tap_level = boosts.get('BoostEarnPerTap', {}).get('level', 0)
                    print(Fore.CYAN + Style.BRIGHT + f"[ Energy Level	] : {boost_max_taps_level}", flush=True)
                    print(Fore.CYAN + Style.BRIGHT + f"[ Tap Level	] : {boost_earn_per_tap_level}", flush=True)
                    print(Fore.CYAN + Style.BRIGHT + f"[ Exchange	] : {clicker_data['exchangeId']}", flush=True)
                    if clicker_data['exchangeId'] == None:
                        print(Fore.GREEN + '\rSetting exchange to Binance..',end="", flush=True)
                        exchange_set = exchange(token, proxy)

                        if exchange_set.status_code == 200:
                            print(Fore.GREEN + Style.BRIGHT +'\rSuccessfully set exchange to Binance', flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT +'\rFailed to set exchange', flush=True)
                    print(Fore.CYAN + Style.BRIGHT + f"[ Income/Hour] : {separator(clicker_data['earnPassivePerHour'])}\n", flush=True)
                    
                    print(Fore.GREEN + f"\r[ Tap Status	] : Tapping ...", end="", flush=True)

                    response = tap(token, clicker_data['maxTaps'], clicker_data['availableTaps'], proxy)
                    if response.status_code == 200:
                        print(Fore.GREEN + Style.BRIGHT + "\r[ Tap Status	] : Successful Tap Tap...            ", flush=True)
                        print(Fore.CYAN + Style.BRIGHT + f"\r[ Booster	] : Checking booster...", end="", flush=True)
                        response = check_booster(token, proxy)
                        if response.status_code == 200:
                            booster_info = response.json()['boostsForBuy']
                            for boost in booster_info:
                                if boost['id'] == 'BoostFullAvailableTaps':
                                    stock = boost['maxLevel'] - boost['level'] 
                                    cooldown = boost['cooldownSeconds']
                                    minutes, seconds = divmod(cooldown, 60)
                                    hours, minutes = divmod(minutes, 60)
                                    hours = str(hours).zfill(2)
                                    minutes = str(minutes).zfill(2)
                                    seconds = str(seconds).zfill(2)
                                    if hours == '00':
                                        hours_str = ""
                                    else:
                                        hours_str = f"{hours} Hours "
                                    if minutes == '00':
                                        minutes_str = ""
                                    else:
                                        minutes_str = f"{minutes} Minutes "
                                    if stock == -1:
                                        stock ="Out of stock"
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Booster	] : Stock {stock} | Cooldown {hours_str}{minutes_str}{seconds} Seconds    ", flush=True)
                            if cooldown == 0:
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Boosted	] : Activating Booster..", end="", flush=True)
                                response = use_booster(token, "BoostFullAvailableTaps", proxy)
                                if response.status_code == 200:
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Boosted	] : Booster Activated", flush=True)   
                                elif response.status_code == 400:
                                    error_info = response.json()
                                    if error_info.get('error_code') == 'BOOST_COOLDOWN':
                                        cooldown_seconds = int(error_info.get('error_message').split()[-2])
                                        cooldown_minutes = cooldown_seconds // 60
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Boosted	] : Booster in cooldown {cooldown_minutes} minutes", flush=True)
                                    else:
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Boosted	] : Failed to activate booster", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Boosted	] : Failed to activate booster", flush=True)

                        else:
                            print(Fore.RED + Style.BRIGHT + "\r[ Booster	] : Tap Status : Failed to Tap           ", flush=True)

                    else:
                        print(Fore.RED + Style.BRIGHT + "\r[ Tap Status	] : Failed to Tap           ", flush=True)
                    time.sleep(1)
                    # Daily Attendance
                    if auto_attendance == 'y':
                        print(Fore.GREEN + f"\r[ Daily Attendance	] : Checking...", end="", flush=True)  
                        response = claim_daily(token, proxy)
                        if response.status_code == 200:
                            daily_response = response.json()['task']
                            if daily_response['isCompleted']:
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Attendance	] :  Day {daily_response['days']} | Completed..", flush=True)
                            else:
                                print(Fore.BLUE + Style.BRIGHT + f"\r[ Daily Attendance	] :  Day {daily_response['days']} | Already attended previously", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Attendance	] :  Failed to Attend.. {response.status_code}", flush=True)
                    else:
                        print(Fore.BLUE + f"\r[ Daily Attendance	] : --> OFF", flush=True)   
                        
                    # Get Morse data and decode to Daily Cipher
                    DailyMorse = ""   
                    if auto_morse == 'y':
                        response = GetAccountConfigRequest(token, proxy)
                        if response.status_code == 200:
                            MorseData = response.json()
                        DailyMorse = DailyCipherDecode(MorseData["dailyCipher"]["cipher"])
                        MorseCode = TextToMorseCode(DailyMorse)
                        print(Fore.CYAN + Style.BRIGHT + f"\r[ Daily Morse	] : Word: {DailyMorse} | Morse: {MorseCode}")
                        if token not in claimed_ciphers:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Claim Morse	] : Claiming Morse...", end="", flush=True)
                            response = claim_cipher(token, DailyMorse, proxy)
                            try:
                                if response.status_code == 200:
                                    bonuscoins = response.json()['dailyCipher']['bonusCoins']
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Claim Morse	] : Successfully claimed Morse | {bonuscoins} bonus coins", flush=True)
                                    claimed_ciphers.add(token)
                                else:
                                    error_info = response.json()
                                    if error_info.get('error_code') == 'DAILY_CIPHER_DOUBLE_CLAIMED':
                                        print(Fore.BLUE + Style.BRIGHT + f"\r[ Claim Morse	] : Already claimed         ", flush=True)
                                    else:
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Claim Morse	] : Failed to claim Morse with error: {error_info.get('error_message', 'No error message')}", flush=True)
                            except json.JSONDecodeError:
                                print(Fore.RED + Style.BRIGHT + "\r[ Claim Morse	] : Failed to parse JSON from response.", flush=True)
                            except Exception as e:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Claim Morse	] : An error occurred: {str(e)}", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Claim Morse	] : Morse has already been claimed previously.", flush=True)
                    else:
                        print(Fore.BLUE + f"\r[ Claim Morse	] : --> OFF", flush=True)
                        
                    # Play mini Game
                    if auto_minigame == 'y':
                        print(Fore.GREEN + Style.BRIGHT + "\r...", end="", flush=True)
                        response = start_minigame(token, proxy)
                        if response.status_code == 200:
                            print(Fore.CYAN + Style.BRIGHT + "\r[ Mini Game	] : Preparing to play MiniGame            ", flush=True)
                            countdown(minigame_delay)
                        if token not in claimed_minigame:
                            print(Fore.GREEN + Style.BRIGHT + "\r[ Mini Game	] : Playing MiniGame            ", end="", flush=True)
                            response = claim_MiniGame(token, minigame_delay, iduser, proxy)
                            try:
                                if response.status_code == 200:
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Mini Game	] : Successfully Claimed MiniGame            ", flush=True)
                                    claimed_minigame.add(token)
                                else:
                                    error_info = response.json()
                                    if error_info.get('error_code') == 'DAILY_KEYS_MINI_GAME_DOUBLE_CLAIMED':
                                        print(Fore.BLUE + Style.BRIGHT + f"\r[ Mini Game	] : Already played MiniGame previously            ", flush=True)
                                    else:
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Mini Game	] : Failed to play MiniGame with error: {error_info.get('error_message', 'No error message')}", flush=True)
                            except json.JSONDecodeError:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Mini Game	] : Failed to parse JSON from response.", flush=True)
                            except Exception as e:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Mini Game	] : An error occurred: {str(e)}", flush=True)
                        else:
                            print(Fore.BLUE + Style.BRIGHT + f"\r[ Mini Game	] : Already played MiniGame previously            ", flush=True)
                    else:
                        print(Fore.BLUE + f"\r[ Mini Game	] : --> OFF ", flush=True)
                    # daily combo
                    if auto_claim_combo == 'y' and not combo_upgraded[init_data_raw]:
                        check = claim_daily_combo(token, proxy)
                        if check.get('error_code') != 'DAILY_COMBO_DOUBLE_CLAIMED':
                            purchased_combos = check_combo_purchased(token, proxy)
                            if purchased_combos is None:
                                print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo	] : Failed to get combo status, will try again with the next account.", flush=True)
                            else:
                                for combo in get_combo("item"):
                                    if combo in purchased_combos:
                                        print(Fore.BLUE + Style.BRIGHT + f"\r[ Daily Combo	] : {combo} already purchased.", flush=True)
                                    elif combo == "none":
                                        continue
                                    else:
                                        print(Fore.GREEN + f"\r[ Daily Combo	] : Buy {combo}", end="", flush=True)
                                        result = buy_upgrade_combo(token, combo, proxy)
                                        if result == 'insufficient_funds':
                                            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Failed to buy {combo}, not enough coins", flush=True)
                                        elif 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                                            upgrade_details = result['error_message'].split(':')[-1].strip().split()
                                            upgrade_key = upgrade_details[1]
                                            upgrade_level = int(upgrade_details[-1])
                                            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Failed to buy {combo} requires {upgrade_key} level {upgrade_level}", flush=True)    
                                            print(Fore.YELLOW + Style.BRIGHT + f"\r[ Daily Combo	] : Trying to buy {upgrade_key} level {upgrade_level}", flush=True)    
                                            result = check_and_upgrade(token, upgrade_key, upgrade_level, proxy)
                                combo_upgraded[init_data_raw] = True
                                required_combos = set(get_combo("item"))
                                purchased_combos = set(check_combo_purchased(token, proxy))
                                if purchased_combos == required_combos:
                                    print(Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo	] : All combos have been purchased, trying to claim 5M Bonus.                 ", end="" ,flush=True)
                                    claim_daily_combo(token, proxy)
                                elif combo == "none":
                                    print(Fore.BLUE + f"\r[ Daily Combo	] Combo not ready, waiting for server update...", flush=True)
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] Failed to claim Daily Combo..", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo	] : Failed. Combos not yet purchased: {required_combos - purchased_combos}               " , flush=True)
                                    combo_upgraded[init_data_raw] = False
                                    continue
                    else:
                        print(Fore.BLUE + f"\r[ Daily Combo	] : --> OFF", flush=True)
                    # List Tasks
                    if auto_check_task_list == 'y':
                        print(Fore.GREEN + f"\r[ Task List	] : Checking...", end="", flush=True)
                        if token not in check_task_dict:
                            check_task_dict[token] = False
                        if not check_task_dict[token]:
                            response = list_tasks(token, proxy)
                            check_task_dict[token] = True
                            if response.status_code == 200:
                                tasks = response.json()['tasks']
                                all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)
                                if all_completed:
                                    print(Fore.BLUE + Style.BRIGHT + "\r[ Task List	] : All tasks have been claimed\n", flush=True)
                                else:
                                    for task in tasks:
                                        if not task['isCompleted']:
                                            print(Fore.YELLOW + Style.BRIGHT + f"\r[ Task List	] : Claiming {task['id']}...", end="", flush=True)
                                            response = check_task(token, task['id'], proxy)
                                            if response.status_code == 200 and response.json()['task']['isCompleted']:
                                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Task List	] : Previously Claimed {task['id']}\n", flush=True)
                                            else:
                                                print(Fore.RED + Style.BRIGHT + f"\r[ Task List	] : Failed to Claim {task['id']}\n", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Task List	] : Failed to get task list {response.status_code}\n", flush=True)
                    else:
                        print(Fore.BLUE + f"\r[ Daily Task	] : --> OFF", flush=True) 
                    # Upgrade Energy
                    if auto_upgrade_energy == 'y':
                        response = check_booster(token, proxy)
                        if response.status_code == 200:
                            booster_info = response.json()['boostsForBuy']
                            for boost in booster_info:
                                if boost['id'] == 'BoostMaxTaps':
                                    lvenergi = boost['level']
                                    lvsekarang = lvenergi-1
                            if lvenergi <= lv_upgrade_energy:
                                print(Fore.GREEN + f"\r[ Upgrade	] : Upgrading Energy....", end="", flush=True)
                                upgrade_response = use_booster(token, "BoostMaxTaps", proxy)
                                if upgrade_response.status_code == 200:
                                    level_boostmaxtaps = upgrade_response.json()['clickerUser']['boosts']['BoostMaxTaps']['level']
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade	] : Energy Successfully Upgraded to Level {level_boostmaxtaps}", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + "\r[ Upgrade	] : Energy Upgrade Failed..", flush=True)
                            else:
                                print(Fore.BLUE + Style.BRIGHT + f"\r[ Upgrade	] : Energy not upgraded, already Level: {lvsekarang}", flush=True)
                    else:
                        print(Fore.BLUE + f"\r[ Upgrade Energy] : --> OFF", flush=True)
                    # Upgrade MultiTap
                    if auto_upgrade_multitap == 'y':
                        response = check_booster(token, proxy)
                        if response.status_code == 200:
                            booster_info = response.json()['boostsForBuy']
                            for boost in booster_info:
                                if boost['id'] == 'BoostEarnPerTap':
                                    lvtap = boost['level']
                                    lvsekarang = lvtap-1
                            if lvtap <= lv_upgrade_multitap:
                                print(Fore.GREEN + f"\r[ Upgrade	] : Upgrading MultiTap....", end="", flush=True)
                                upgrade_response = use_booster(token, "BoostEarnPerTap", proxy)
                                if upgrade_response.status_code == 200:
                                    level_boostmaxtaps = upgrade_response.json()['clickerUser']['boosts']['BoostEarnPerTap']['level']
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade	] : MultiTap Successfully Upgraded to Level {level_boostmaxtaps}", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + "\r[ Upgrade	] : MultiTap Upgrade Failed..", flush=True)
                            else:
                                print(Fore.BLUE + Style.BRIGHT + f"\r[ Upgrade	] : MultiTap not upgraded, already Level: {lvsekarang}", flush=True)
                    else:
                        print(Fore.BLUE + f"\r[ Upgrade MultiTap]: --> OFF", flush=True)

                    # Check upgrade
                    if auto_upgrade_pph == 'y':
                        print(Fore.GREEN + f"\r[ Upgrade	] : Checking...", end="", flush=True)
                        auto_upgrade_pph_earn(token, max_price, proxy)
                    else:
                        print(Fore.BLUE + f"\r[ Auto Upgrade	] : --> OFF", flush=True)
                        
                else:
                    print(Fore.RED + Style.BRIGHT + f"\r Failed to get user info {response.status_code}", flush=True) 
                print(Fore.GREEN + Style.BRIGHT + "\r==========================================")

            elif response.status_code == 401:
                error_data = response.json()
                if error_data.get("error_code") == "NotFound_Session":
                    print(Fore.RED + Style.BRIGHT + f"=== [ Invalid Token {token} ] ===")
                    token_dict.pop(init_data_raw, None)
                    token = None
                else:
                    print(Fore.RED + Style.BRIGHT + "Authentication failed with unknown error")
            else:
                print(Fore.RED + Style.BRIGHT + f"Error with status code: {response.status_code}")
                token = None
                
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"Error with account {init_data_raw} and proxy {proxy}: {str(e)}", flush=True)
            continue  # Bỏ qua cặp này và chuyển sang cặp tiếp theo
            
        time.sleep(1)




def print_welcome_message():
    print(r"""
  _____  _                        _  __     
 |  __ \| |                      | |/ /     
 | |__) | |__  _   _  ___   ___  | ' / __ _ 
 |  ___/| '_ \| | | |/ _ \ / __| |  < / _` |
 | |    | | | | |_| | (_) | (__  | . \ (_| |
 |_|    |_| |_|\__,_|\___/ \___| |_|\_\__,_|
""")
    print(Fore.RED + Style.BRIGHT + " Join PK Airdrop để nhận các tool FREE hiệu chỉnh cực xịn nhé : https://t.me/pkairdrop99" )
    print(Fore.RED + Style.BRIGHT + " TOOL NÀY LÀ FREE, NẾU BẠN PHẢI TRẢ $ ĐỂ CÓ NÓ LÀ BẠN ĐÃ BỊ LỪA !" )
    

if __name__ == "__main__":
    main()




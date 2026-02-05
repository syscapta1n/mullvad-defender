import subprocess
import time
import sys

ACCOUNT_ID = "account id"
CHECK_INTERVAL = 1

def run(args):
    try:
        res = subprocess.run(['mullvad'] + args, capture_output=True, text=True, timeout=10)
        return (res.stdout + " " + res.stderr).strip()
    except Exception as e:
        return str(e)

def main():
    print(f"[*] Запуск защиты (Mullvad New Syntax)...")
    
    while True:
        # 1. Проверяем вход
        acc_info = run(['account', 'get'])
        
        if ACCOUNT_ID not in acc_info:
            print("[!] Вход в аккаунт...")
            run(['account', 'login', ACCOUNT_ID])
            time.sleep(1)
            # Перечитываем инфо после входа
            acc_info = run(['account', 'get'])

        my_name = ""
        for line in acc_info.split('\n'):
            if "Device name:" in line:
                my_name = line.split(":")[-1].strip()

]        devices_raw = run(['account', 'list-devices'])
        lines = devices_raw.split('\n')
        
        enemies = []
        if my_name:
            for line in lines:
                clean_line = line.strip()
                # Фильтруем мусор и технические строки
                if not clean_line or "Devices on" in clean_line or "-----" in clean_line or "Device name" in clean_line or "|" in clean_line:
                    continue
                
                # Если наше имя не встречается в строке — это враг
                if my_name not in clean_line:
                    # Берем имя до скобки
                    enemy_name = clean_line.split('(')[0].strip()
                    if enemy_name:
                        enemies.append(enemy_name)

        if enemies:
            print(f"\n[!] Враги: {enemies}")
            for enemy in enemies:
                print(f"[*] Удаляю: {enemy}...", end=" ")
                
                # ТЕПЕРЬ ИСПОЛЬЗУЕМ REVOKE-DEVICE
                res = run(['account', 'revoke-device', enemy])
                
                if "revoked" in res.lower() or "removed" in res.lower():
                    print("\033[92m[УСПЕХ]\033[0m")
                else:
                    # Если ошибка, выводим её, чтобы понять причину
                    print(f"\033[91m[ОШИБКА: {res}]\033[0m")
        else:
            sys.stdout.write(f"\r\033[92m[✓] Ты: {my_name} | Чисто | {time.strftime('%H:%M:%S')}\033[0m")
            sys.stdout.flush()

        status = run(['status'])
        if "Connected" not in status:
            run(['connect'])

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

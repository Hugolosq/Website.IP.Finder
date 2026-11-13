# --- Imports ---
import socket
import requests
import sys
import os
import time
import pyfiglet
import msvcrt 
import ctypes

# --- Window Maximization ---
if os.name == "nt":
    os.system("") 
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow() 
    if hwnd:
        user32.ShowWindow(hwnd, 3)
    time.sleep(0.4)
    os.system("mode con: cols=200 lines=50")

# --- Colors ---
class C:
    RESET = "\033[0m"
    BOLD  = "\033[1m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    CYAN  = "\033[96m"
    GREEN = "\033[92m"
    RED   = "\033[91m"
    YELLOW= "\033[93m"
    GRAY = "\033[90m"

def get_rgb_color(hue):
    h = hue % 360
    c = 255
    x = int(c * (1 - abs((h / 60) % 2 - 1)))
    if 0 <= h < 60: r, g, b = c, x, 0
    elif 60 <= h < 120: r, g, b = x, c, 0
    elif 120 <= h < 180: r, g, b = 0, c, x
    elif 180 <= h < 240: r, g, b = 0, x, c
    elif 240 <= h < 300: r, g, b = x, 0, c
    else: r, g, b = c, 0, x
    return f"\033[38;2;{r};{g};{b}m"

# --- Banner Generation ---
art = pyfiglet.figlet_format("WEBSITE.IP.FINDER", font="ansi_shadow", width=200)
banner_lines = [line for line in art.split('\n') if line.strip()]

def make_clickable_link(url):
    return f"\033]8;;{url}\033\\{C.BLUE}{C.BOLD}{url}{C.RESET}\033]8;;\033\\"

# --- UI ---
def draw_ui(frame, current_input, status_text=""):
    sys.stdout.write("\033[H")
    output = ""
    
    for y, line in enumerate(banner_lines):
        colored_line = ""
        for x, char in enumerate(line):
            if char != ' ':
                hue = (x * 3) + (y * 10) + (frame * 6)
                colored_line += f"{get_rgb_color(hue)}{C.BOLD}{char}" 
            else:
                colored_line += " "
        output += colored_line + C.RESET + "\033[K\n"
        
    output += "\n" + C.BOLD + C.MAGENTA + "MADE BY HUGOLOSQ" + C.RESET + "\033[K\n\n"
    output += C.GRAY + "─" * 120 + C.RESET + "\033[K\n\n"
    
    if status_text:
        output += f"{C.YELLOW}{status_text}{C.RESET}" + "\033[K\n"
    else:
        cursor = "_" if int(time.time() * 2) % 2 == 0 else " "
        prompt = "Enter a website (e.g. google.com): "
        output += f"{C.BOLD}{prompt}{C.RESET}{current_input}{cursor}" + "\033[K\n"
    
    sys.stdout.write(output)
    sys.stdout.flush()

# --- Logic ---
def find_ip_and_location(website: str):
    print("\033[J") 
    print(C.YELLOW + f"[*] Looking up: {website}" + C.RESET)
    
    try:
        ip_address = socket.gethostbyname(website)
        print(C.GREEN + f"[+] IP address: {ip_address}" + C.RESET)
        
        url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,regionName,city,lat,lon"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("status") == "success":
            print(C.CYAN + "\n--- Approximate location ---" + C.RESET)
            print(f"  Country : {data.get('country', 'Unknown')}")
            print(f"  Region  : {data.get('regionName', 'Unknown')}")
            print(f"  City    : {data.get('city', 'Unknown')}")
            lat, lon = data.get("lat"), data.get("lon")
            print(f"  Coords  : {lat}, {lon}")
            
            if lat is not None and lon is not None:
                maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                print(f"  Map     : {make_clickable_link(maps_url)} {C.GRAY}[Press 'o' to open]{C.RESET}")
                
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        if key.lower() == b'o':
                            os.system(f'start msedge "{maps_url}"')
                        break
                        
        else:
            print(C.RED + "[!] API Error." + C.RESET)
            
    except socket.gaierror:
        print(C.RED + f"[!] Invalid or non-existent website: '{website}'" + C.RESET)
    except Exception:
        print(C.RED + "[!] Connection error." + C.RESET)

# --- Main Loop ---
def main():
    os.system("cls")
    frame = 0
    current_input = ""
    
    sys.stdout.write("\033[?25l") 
    
    try:
        while True:
            anim_frame = frame if not current_input else 0
            draw_ui(anim_frame, current_input)
            
            if msvcrt.kbhit():
                key = msvcrt.getch()
                
                if key == b'\x1b': 
                    break
                    
                if key == b'\r': 
                    if current_input:
                        if current_input.lower() in ["exit", "q"]:
                            break
                            
                        draw_ui(0, "", "SCANNING TARGET... PLEASE WAIT")
                        find_ip_and_location(current_input)
                        
                        print("\n" + C.GRAY + "Press any key to continue..." + C.RESET)
                        msvcrt.getch() 
                        
                        os.system("cls")
                        current_input = ""
                        frame = 0
                        
                elif key == b'\x08': 
                    current_input = current_input[:-1]
                    
                else:
                    try:
                        char = key.decode('utf-8')
                        if char.isprintable():
                            current_input += char
                    except:
                        pass
            
            time.sleep(0.08)
            
            if not current_input:
                frame += 1
                
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h") 
        os.system("cls")

if __name__ == "__main__":
    main()

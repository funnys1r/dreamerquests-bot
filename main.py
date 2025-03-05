import requests
import schedule
import time
from datetime import datetime, timedelta
import colorama
from colorama import Fore, Back, Style
import traceback
import json
import os
import random

colorama.init(autoreset=True)

def print_banner():
    banner = f"""{Fore.MAGENTA}
╔═══════════════════════════════════════════════╗
║   partofdream.io - DreamerQuest 自动签到工具  ║
║     GitHub: https://github.com/example/pod     ║
║     支持多账号 & 多代理自动切换              ║
╚═══════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

class GameAutomation:
    def __init__(self, user_config):
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,id;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://dreamerquests.partofdream.io',
            'priority': 'u=1, i',
            'referer': 'https://dreamerquests.partofdream.io/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
        }
        
        self.cookies = user_config.get('cookies', {})
        self.payload = {
            "userId": user_config.get('userId', ''),
            "timezoneOffset": -420
        }
        self.account_name = user_config.get('name', '未命名账号')
        self.proxies = self.load_proxies()
        self.current_proxy_index = 0
        self.max_retry = 3

    def load_proxies(self):
        """加载代理列表"""
        try:
            if os.path.exists('proxies.txt'):
                with open('proxies.txt', 'r', encoding='utf-8') as f:
                    proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                if proxies:
                    return proxies
        except Exception as e:
            self.log(f"读取代理文件失败：{e}", Fore.RED)
        return [None]  # 如果没有代理文件或代理为空，返回包含None的列表（表示不使用代理）

    def get_next_proxy(self):
        """获取下一个代理"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return proxy

    def log(self, message, color=Fore.WHITE):
        timestamp = f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}"
        print(f"{timestamp} {color}[{self.account_name}]{Style.RESET_ALL} {message}")

    def perform_request(self, url, action_name):
        retry_count = 0
        while retry_count < self.max_retry:
            try:
                proxy = self.get_next_proxy()
                proxies = None
                if proxy:
                    proxies = {
                        'http': proxy,
                        'https': proxy
                    }
                    self.log(f"使用代理: {proxy}", Fore.CYAN)
                
                self.log(f"正在发起{action_name}请求...", Fore.CYAN)
                
                response = requests.post(
                    url, 
                    json=self.payload, 
                    headers=self.headers, 
                    cookies=self.cookies,
                    proxies=proxies,
                    timeout=30
                )
                
                self.log(f"{action_name}详情：", Fore.GREEN)
                self.log(f"时间戳：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Fore.GREEN)
                self.log(f"状态码：{response.status_code}", 
                    Fore.GREEN if response.status_code == 200 else Fore.RED
                )
                
                try:
                    response_json = response.json()
                    self.log(f"响应内容：{response_json}", Fore.MAGENTA)
                    
                    # 检查是否是"今日已完成"的消息
                    if isinstance(response_json, dict) and 'message' in response_json:
                        if 'already checked-in today' in response_json['message'] or 'already spun today' in response_json['message']:
                            # 不再显示具体时间，因为实际执行时间会包含随机延迟
                            self.log(f"今日已完成{action_name}，下次{action_name}将在24小时后（含随机延迟）进行", Fore.GREEN)
                            return True
                except ValueError:
                    self.log(f"响应内容：{response.text}", Fore.YELLOW)
                
                if response.status_code == 200:
                    # 不再显示具体时间，因为实际执行时间会包含随机延迟
                    self.log(f"完成，下次{action_name}将在24小时后（含随机延迟）进行", Fore.GREEN)
                    return True
                
                self.log(f"请求失败，尝试使用下一个代理...", Fore.YELLOW)
                retry_count += 1
                
            except Exception as e:
                self.log(f"代理 {proxy} 连接失败: {str(e)}", Fore.RED)
                retry_count += 1
                if retry_count < self.max_retry:
                    self.log(f"正在切换到下一个代理重试...", Fore.YELLOW)
                time.sleep(2)  # 添加延迟，避免请求过快
        
        self.log(f"{action_name}失败，已尝试所有可用代理", Fore.RED)
        return False

    def perform_checkin(self):
        return self.perform_request(
            'https://server.partofdream.io/checkin/checkin', 
            '签到'
        )

    def perform_spin(self):
        return self.perform_request(
            'https://server.partofdream.io/spin/spin', 
            '抽奖'
        )

def create_proxy_file():
    """创建代理配置文件模板"""
    if not os.path.exists('proxies.txt'):
        with open('proxies.txt', 'w', encoding='utf-8') as f:
            f.write("""# 在下面添加代理地址，每行一个
# 支持格式：
# http://127.0.0.1:7890
# http://用户名:密码@127.0.0.1:7890
# 井号开头的行为注释，会被忽略
# 留空表示不使用代理直连
http://127.0.0.1:7890
http://127.0.0.1:10809
""")
        print(f"{Fore.GREEN}已创建代理配置文件 proxies.txt，请编辑添加代理地址{Style.RESET_ALL}")

def get_user_config():
    print_banner()
    
    # 确保代理配置文件存在
    create_proxy_file()
    
    config = {'accounts': []}
    
    # 尝试读取配置文件
    try:
        if os.path.exists('config.txt'):
            with open('config.txt', 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                for line in lines:
                    try:
                        name, user_id, connect_sid = line.split(':')
                        config['accounts'].append({
                            'name': name,
                            'userId': user_id,
                            'cookies': {
                                'connect.sid': connect_sid
                            }
                        })
                    except ValueError:
                        print(f"{Fore.RED}配置格式错误，请确保每行格式为：账号备注:用户ID:connect.sid{Style.RESET_ALL}")
                        continue
                
                if config['accounts']:
                    print(f"{Fore.GREEN}已从配置文件加载 {len(config['accounts'])} 个账号{Style.RESET_ALL}")
                    return config
    except Exception as e:
        print(f"{Fore.RED}读取配置文件失败：{e}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}未找到配置文件或配置文件为空，请手动输入配置{Style.RESET_ALL}")
    accounts = []
    while True:
        print(f"\n{Fore.CYAN}==== 添加账号 ===={Style.RESET_ALL}")
        account_name = input(f"{Fore.YELLOW}请输入账号备注（便于识别）：{Style.RESET_ALL}")
        user_id = input(f"{Fore.YELLOW}请输入用户ID：{Style.RESET_ALL}")
        connect_sid = input(f"{Fore.YELLOW}请输入connect.sid：{Style.RESET_ALL}")
        
        accounts.append({
            'name': account_name,
            'userId': user_id,
            'cookies': {
                'connect.sid': connect_sid
            }
        })
        
        # 保存到配置文件
        try:
            with open('config.txt', 'w', encoding='utf-8') as f:
                for acc in accounts:
                    f.write(f"{acc['name']}:{acc['userId']}:{acc['cookies']['connect.sid']}\n")
            print(f"{Fore.GREEN}配置已保存到 config.txt{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}保存配置文件失败：{e}{Style.RESET_ALL}")
        
        if input(f"\n{Fore.YELLOW}是否继续添加账号？(y/n)：{Style.RESET_ALL}").lower() != 'y':
            break
    
    return {'accounts': accounts}

def main():
    config = get_user_config()
    bots = []

    for account in config['accounts']:
        bot = GameAutomation(account)
        bots.append(bot)
        
        # 初始执行一次
        bot.perform_checkin()
        bot.perform_spin()
        
        # 设置定时任务：24小时 + 随机1-60分钟
        random_minutes = random.randint(1, 60)
        total_minutes = 24 * 60 + random_minutes
        schedule.every(total_minutes).minutes.do(bot.perform_checkin)
        schedule.every(total_minutes).minutes.do(bot.perform_spin)
        print(f"{Fore.CYAN}[{bot.account_name}] 下次执行将在24小时{random_minutes}分钟后进行{Style.RESET_ALL}")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}程序已被用户终止。{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

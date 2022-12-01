import json
import os
import random
import sys
import time
import requests
import colorama
from colorama import Fore, Style
from threading import Lock
from datetime import datetime
from os import system

print_lock = Lock()
colorama.init(autoreset=True)


RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
GREEN = "\033[92m"
ORANGE = '\033[33m'

class Logger:
	def getTime():
		return datetime.now().strftime("%H:%M:%S")

	def info(reason):
		print(f"[{Logger.getTime()}] {BLUE}{reason}{RESET}")
		pass

	def error(reason):
		print(f"[{Logger.getTime()}] {RED}{reason}{RESET}")
		pass

	def success(message):
		print(f"[{Logger.getTime()}] {GREEN}{message}{RESET}")




class like_bot:
    def __init__(self, username, passw, url) -> None:
        self.delay = random.randint(33,147)
        self.delay_1 = random.randint(16, 57)

        self.s = requests.Session()
        self.password = f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{passw}"
        self.username = username
        
        self.short_code = url.replace("https://www.instagram.com/p/", "").replace("/", "")

        r = self.s.get('https://www.instagram.com/accounts/login/')
        csrf = r.text.replace("\\", "").split('csrf_token\":\"')[1].split('"')[0]

        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "viewport-width": "864",
            "x-asbd-id": "198387",
            "x-csrftoken": csrf,
            "x-ig-app-id": "936619743392459",
            "x-ig-www-claim": "0",
            "x-instagram-ajax": "1006578552",
            "x-requested-with": "XMLHttpRequest"
        }

        self.login()


    def login(self):
        time.sleep(self.delay_1)
        r = self.s.post(
            "https://www.instagram.com/api/v1/web/accounts/login/ajax/",
            headers=self.headers,
            data={
                "enc_password": self.password,
                "username": self.username,
                "queryParams": "{}",
                "optIntoOneTap": "false",
                "trustedDeviceRecords": "{}"
            }
        )
        self.headers.update({"x-ig-set-www-claim": r.headers["x-ig-set-www-claim"]})
        self.headers.update({"x-csrftoken": r.cookies.get("csrftoken")})

    def get_user_id(self):
        time.sleep(self.delay_1)
        r = self.s.get(
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.username}",
            headers=self.headers
        )
        user_id = r.json()["data"]["user"]["id"]
        return user_id


    def get_follower(self):
        time.sleep(self.delay_1)
        follower_list = []
        user_id = self.get_user_id()
        r = self.s.get(
            f"https://www.instagram.com/api/v1/friendships/{user_id}/followers/?count=99999&search_surface=follow_list_page",
            headers=self.headers
        )
        for i in r.json()["users"]:
            follower_list.append(i["pk"])
        return follower_list

    def get_liker(self):
        time.sleep(self.delay_1)
        liker_list = []
        # get who liked the post
        r = self.s.get(
            'https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={"shortcode":"%s","include_reel":true,"first":50}' % self.short_code,#"CBja6-cnmNJ",#self.short_code,
            headers=self.headers
        )
        data = r.json()["data"]["shortcode_media"]["edge_liked_by"]["edges"]
        for i in data:
            liker_list.append(i["node"]["id"])

        like_count = r.json()["data"]["shortcode_media"]["edge_liked_by"]["count"]
        next_page = r.json()["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]
        time.sleep(self.delay_1)
        while True:
            r = self.s.get('https://www.instagram.com/graphql/query/?query_hash=d5d763b1e2acf209d62d22d184488e57&variables={"shortcode":"%s","include_reel":true,"first":50,"after":"%s"}' % (self.short_code, next_page),
            headers=self.headers)
            data = r.json()["data"]["shortcode_media"]["edge_liked_by"]["edges"]
            for i in data:
                liker_list.append(i["node"]["id"])
            next_page = r.json()["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]
            if next_page == '':
                break
            time.sleep(self.delay_1)
        return liker_list

    def like_posts(self):
        time.sleep(self.delay_1)
        follower_list = self.get_follower()
        liker_list = self.get_liker()
        x=0
        for f, l in zip(follower_list, liker_list):
            time.sleep(self.delay)
            x+=1
            if l in f:
                Logger.info(f"Person - {x} is follower")
            else:
                Logger.info(f"Person - {x} is not follower")
                r = self.s.get(
                    f"https://www.instagram.com/api/v1/feed/user/{l}/?count=2", # just get the first  posts from person to like
                    headers=self.headers
                )
                y=0
                for i in r.json()["items"]:
                    time.sleep(self.delay)
                    post_id = i["pk"]
                    r = self.s.post(
                        f"https://www.instagram.com/api/v1/web/likes/{post_id}/like/", # like the post
                        headers=self.headers
                    )
                    y+=1
                    if y == 1:
                        c = "first"
                    else:
                        c = "second"

                    if r.json()["status"] and r.json()["status"] == "ok":
                        Logger.success(f"Successful liked {c} post")
                    else:
                        Logger.error(f"Error while liking {c} post -> {r.text}")

def get_config():
    with open("config.json", "r") as config_file:
        read_config = json.load(config_file)
    username = read_config["username"]
    password = read_config["password"]
    url = read_config["url"]
    return username, password, url



def __start_bot__():
    system('title Insta Like Bot')

    HEADER = """



                         ___ _  _ ___ _____ _     _    ___ _  _____   ___  ___ _____ 
                        |_ _| \| / __|_   _/_\   | |  |_ _| |/ / __| | _ )/ _ \_   _|
                         | || .` \__ \ | |/ _ \  | |__ | || ' <| _|  | _ \ (_) || |  
                        |___|_|\_|___/ |_/_/ \_\ |____|___|_|\_\___| |___/\___/ |_|  
                        
                                                                





    """
    print(Fore.MAGENTA, HEADER, Style.RESET_ALL)

    username, password, url = get_config()
    print("   Username: ", username)
    print("   Password: ", password)
    print("   Url:      ", url)
    print("\n\n\n")
    input("   Press ENTER to start\n\n\n")
    try:
        x = like_bot(username, password, url)
        x.like_posts()
    except Exception as e:
        print(e)
        time.sleep(30)

    input("press enter to exit...")

__start_bot__()
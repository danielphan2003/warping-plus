#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python38.withPackages(ps: with ps; [ httplib2 ])"

import httplib2
import json
import os
import platform
import random
import string
import tempfile

from datetime import datetime
from multiprocessing import Process, Value



###########################################################################################################
###########################################################################################################
####																																																	 ####
####	 ██╗    ██╗ █████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗     ██████╗ ██╗     ██╗   ██╗███████╗   ####
####	 ██║    ██║██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██║     ██║   ██║██╔════╝   ####
####	 ██║ █╗ ██║███████║██████╔╝██████╔╝██║██╔██╗ ██║██║  ███╗    ██████╔╝██║     ██║   ██║███████╗   ####
####	 ██║███╗██║██╔══██║██╔══██╗██╔═══╝ ██║██║╚██╗██║██║   ██║    ██╔═══╝ ██║     ██║   ██║╚════██║	 ####
####	 ╚███╔███╔╝██║  ██║██║  ██║██║     ██║██║ ╚████║╚██████╔╝    ██║     ███████╗╚██████╔╝███████║   ####
####	  ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝     ╚══════╝ ╚═════╝ ╚══════╝   ####
####																																																	 ####
###########################################################################################################
###########################################################################################################



HOME = os.getenv("HOME")

### On Windows, this will be C:\TEMP
CACHE = tempfile.gettempdir() if platform.system() == "Windows" else f"{HOME}/.cache"

config = {

	"referrer": "<warp-id>",
	"proxies_url": "https://api.proxyscrape.com?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all",

	### If auto_download_proxies_file is False...
	"auto_download_proxies_file": True,

	### ...then choose your proxies file here.
	### Note that on Linux and macOS, this file should be in ~/.cache/proxy.txt.
	### On Windows, this file will be relative to where you downloaded this file:
	### /
	### ├── proxy.txt
	### └── wp-plus.py
	"proxies_file_path": f"{CACHE}/proxy.txt",

	### Don't waste time downloading if it is already in cache
	"use_cache": True,
	### Warping Plus can be spawned repeatedly, but only when multi_instance is enabled.
	### Only disable it when you intend to spawn ONLY one instance.
	"multi_instance": True,

}

def clear():
	os.system("cls" if platform.system() == "Windows" else "clear")

def rndStringFromList(array, len):
	return ''.join((random.choice(array) for i in range(len)))

def genAlphanumericString(len):
	letters = string.ascii_letters + string.digits
	return rndStringFromList(letters, len)

def genDigitString(len):
	return rndStringFromList(string.digits, len)

def addWarp(g, b, proxy, referrer):
	proxy_info = httplib2.proxy_info_from_url(f"http://{proxy}")
	h = httplib2.Http(proxy_info = proxy_info)
	status = getWarpStatus(h, referrer)

	clear()
	print(f"[-] WORK ON ID: {referrer}")
	print(f"[=] Trying proxy {proxy_info.proxy_host}")
	if status == 200:
		g.value += 1
		print("[:)] 1 GB has been successfully added to your account.")
	else:
		b.value += 1
		print("[:(] Error when connecting to server.")
	print(f"[#] Total: {g.value} Good {b.value} Bad")

def getWarpStatus(h, referrer):
	try:
		utc_now = f"{datetime.utcnow().isoformat()[:-3]}+00:00"
		rnd_key = f"{genAlphanumericString(43)}="
		rnd_install_id = genAlphanumericString(22)
		rnd_fcm_token = f"{rnd_install_id}:APA91b{genAlphanumericString(134)}"
		rnd_user_reg_url = f"https://api.cloudflareclient.com/v0a{genDigitString(3)}/reg"

		body = json.dumps({
			"key": rnd_key,
			"install_id": rnd_install_id,
			"fcm_token": rnd_fcm_token,
			"referrer": referrer,
			"warp_enabled": False,
			"tos": utc_now,
			"type": "Android",
			"locale": "es_ES"
		}).encode('utf8')

		headers = {
			'Content-Type': 'application/json; charset=UTF-8',
			'Host': 'api.cloudflareclient.com',
			'Connection': 'Keep-Alive',
			'Accept-Encoding': 'gzip',
			'User-Agent': 'okhttp/3.12.1'
		}

		res, _ = h.request(
			rnd_user_reg_url,
			method = "POST",
			body = body,
			headers = headers
		)

		return res.status
	except:
		return 404

def getProxiesFile(config):
	try:
		proxies_file_path = f"{tempfile.gettempdir()}/proxy_{genAlphanumericString(5)}.txt"
			if config["multi_instance"] else config["proxies_file_path"]

		if config["use_cache"]:
			if os.path.exists(proxies_file_path) and os.path.getsize(proxies_file_path) > 0:
				return open(proxies_file_path)

		if config["auto_download_proxies_file"]:
			if not os.path.exists(proxies_file_path):
				if platform.system() != "Windows" and not os.path.exists(CACHE):
					os.mkdir(CACHE)
			h = httplib2.Http()
			_, content = h.request(config["proxies_url"])
			with open(proxies_file_path, "wb") as f:
				f.write(content)
				f.close()
			return str(content).split("\\r\\n")

		print("use_cache and download_proxies_file must not be False at the same time!")
		sys.exit(1)
	except Exception as e:
		print(f"Error occurred when opening {config['proxies_file_path']}")
		print(f"Full error message: {e}")

if __name__ == '__main__':
	if config["referrer"] == "<warp-id>":
		print("Specify your Warp+ ID in `referrer`!")
		sys.exit(1)

	proc = []
	g = Value('i', 0)
	b = Value('i', 0)

	proxies = list(getProxiesFile(config))
	random.shuffle(proxies)
	for proxy in proxies:
		p = Process(target = addWarp, args=(g, b, proxy.strip(), config["referrer"]))
		p.start()
		proc.append(p)
	for p in proc:
		p.join()

from bs4 import BeautifulSoup
import requests
import tweepy
import time
import sys
import os

class TwitterHandler(object):
	def __init__(self, api_cfg=None):
		global api
		if api_cfg:
			auth = tweepy.OAuthHandler(api_cfg['consumer_key'], api_cfg['consumer_secret'])
			auth.set_access_token(api_cfg['access_token'], api_cfg['access_token_secret'])
			api = tweepy.API(auth)
		else:
			if api is None:
				print("You must set your CFG")
				return

	def compose_tweet(self, tweet_content):
		self.content = tweet_content
		api.update_status(status=self.content)
		print("Tweet composed.")

class SiteMonitor(object):
	def __init__(self, target_url, target_x, target_y, target_z):
		self.s = requests.session()

		target_name = str(BeautifulSoup(self.s.get(str(target_url)).text, "lxml").title.string)

		self.site_setup = { 
		"target_name" : str(target_name),
		"target_url"  : str(target_url),
		"target_x"  : str(target_x),
		"target_y"  : str(target_y),
		"target_z"  : str(target_z)
		}

		self.change_check()

	def change_check(self):
		check_number = 0
		keep_monitoring = True

		while keep_monitoring:
			check_number += 1
			print("Checking... (" + str(check_number) + ")")
			time.sleep(5)
			page = self.s.get(self.site_setup['target_url'])
			soup = BeautifulSoup(page.text, "lxml")

			status1 = soup.find(self.site_setup['target_x'], {self.site_setup['target_y']:self.site_setup['target_z']})

			if 'status2' in locals():
				if status1 == status2:
					print("No present change")
					keep_monitoring = True
				else:
					print("Page has been changed")
					keep_monitoring = False
					self.page_change()
			else:
				print("No present change")
				keep_monitoring = True

			status2 = soup.find(self.site_setup['target_x'], {self.site_setup['target_y']:self.site_setup['target_z']})

	def page_change(self):
		print(self.site_setup['target_name'] + " is now back in stock! (" + self.site_setup['target_url'] + ")")
		TwitterHandler().compose_tweet("Restock at " + self.site_setup['target_url'])

class Program(object):
	def __init__(self):
		self.setup_twitter()
		self.add_site()

	def setup_twitter(self):
		cfg = { 
		"consumer_key"        : "",
		"consumer_secret"     : "",
		"access_token"        : "",
		"access_token_secret" : "" 
		}

		TwitterHandler(cfg)

	def add_site(self):
		target_url = input("Target URL? ")
		target_x = input("Target X? ")
		target_y = input("Target Y? ")
		target_z = input("Target Z? ")

		SiteMonitor(target_url, target_x, target_y, target_z)

Program()
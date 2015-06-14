from subprocess import call
from time import sleep

while 1:
	call('scrapy crawl test591', shell=True)
	sleep(30)


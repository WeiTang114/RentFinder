from subprocess import call
from time import sleep

while 1:
	call('scrapy crawl --loglevel=CRITICAL  test591', shell=True)
	sleep(30)


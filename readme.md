# RentCrawler

## Usage

###加入想要的區域
在 test_591_spider.py 的 start_urls 加入想要的區域。區域代碼可在 591 網站上查看 response 得到。

###設定寄件信箱
先申請一個寄件用的 gmail 帳號，然後把帳密填在 settings.py 中。

###設定收件信箱
修改 itempipelines/dataset_pipeline.py 的 self.notifiers，

```
self.notifiers = [
    Emailer(['a@gmail.com', 'b@gmail.com'], settings)
]
```

###執行：
使用 tmux 或 screen 可使其背景執行：

```
cd RentCrawler
python scrapy_runner.py
```



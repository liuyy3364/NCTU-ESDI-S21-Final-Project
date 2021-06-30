# NCTU-ESDI-S21-Final-Project

109學年 下學期 1165嵌入式系統設計概論與實作 期末專案

## 題目

零接觸販賣機

## Requirement

大多是上課的東西

- Python 3.7.3
- RPi.GPIO
- spidev
- signal
- requests
- gspread
- oauth2client
- gTTS
- speech_recognition
- pydub

google 表單需要額外設定，請跟著這篇[文章](https://yanwei-liu.medium.com/%E5%A6%82%E4%BD%95%E9%80%8F%E9%81%8Epython%E5%BB%BA%E7%AB%8Bgoogle%E8%A1%A8%E5%96%AE-%E4%BD%BF%E7%94%A8google-sheet-api-314927f7a601)設定，並修改 key.json 成你的 key.json，qrcode 也記得要還成你自己的連結 qrcode

## Run

``` bash
sudo python webserver.py
```

``` bash
# 有虛擬環境或使用者不同等問題時可以嘗試
sudo `which python` webserver.py
```

``` bash
# 有時候MFRC522會很不乖，感應不到卡
# 這情況發生時請照著以下步驟做
kill -9 <PID of python webserver.py>
# 先跑一次 Read.py
python Read.py
# 刷一次卡之後就可以 kill 掉了
# 之後重新執行主程式
sudo python webserver.py
```

## 使用指南

### 開機後

1. 開啟網頁，預設是 localhost:80
1. 臉正對鏡頭並靠近，直到臉的大小約等於畫面框大小

### 偵測到有客人，開始點餐

1. 等待語音提示結束並顯示收音中
1. 大聲且咬字清楚地說出語音指令：

``` bash
# 依指令優先度排序
取消交易：任何語句包含取消二字
進入結帳：任何語句包含結帳二字，可以與下方指令合用，例：餅乾結帳
清除：任何語句包含清除二字
新增商品：[[數量]商品名稱]...       # 商品名稱必須不同，未指定數量則為 1 個
移除商品：移除 [[數量]商品名稱]...  # 商品名稱必須不同，未指定數量則為 999 個
```

### 結帳

1. 確認結帳並依據庫存調整購物車，待語音提示並顯示收音中時，說出是或確認繼續下一步，否或取消回到點餐階段
1. 感應磁卡扣款結帳，可能有四種狀況
  
    - 已註冊卡且餘額足夠：結帳成功，交易結束並透過 LINE notify 傳送消費資訊
    - 已註冊卡且餘額不足：結帳失敗，餘額不足，交易取消並透過 LINE notify 傳送餘額不足通知
    - 未註冊卡：結帳失敗，提示卡片需註冊，交易取消
    - 讀卡機當機：沒DEBUG成功，請照上方 RUN 的指示作一遍

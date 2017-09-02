# line-bot-Tutorial

 教你建立自己的 line-bot 使用 python flask 📝

 line-bot-tutorial use python flask

* [Youtube Demo Tutorial V1](https://youtu.be/EToFs-ysXKw)

* [Youtube Demo V2](https://youtu.be/1IxtWgWxtlE)

## 執行畫面

請先加入好友

我的 QRCODE

![alt tag](http://i.imgur.com/Kkpzt4p.jpg)

或是手機直接點選 [https://line.me/R/ti/p/%40vbi2716y](https://line.me/R/ti/p/%40vbi2716y)

![alt tag](http://i.imgur.com/oAgR5nr.jpg)

認證記得請選 **同意**

![alt tag](http://i.imgur.com/9LOlGHh.jpg)

### 功能

***精選功能***

![alt tag](http://i.imgur.com/IB3hBl8.jpg)

輸入任何文字即可開始玩

![alt tag](http://i.imgur.com/M30GJOU.jpg)

***開始玩***

![alt tag](http://i.imgur.com/PCcnc5R.jpg)

***新聞***

![alt tag](http://i.imgur.com/mc0R0xL.jpg)

#### 蘋果即時新聞

 apple news 即時新聞 ( 來源 [http://www.appledaily.com.tw/realtimenews/section/new/](http://www.appledaily.com.tw/realtimenews/section/new/) )

![alt tag](http://i.imgur.com/OpJj9DE.png)

#### 科技新報

科技新報 ( Tech News ) 最新文章
( 來源 [https://technews.tw/](https://technews.tw/) )

![alt tag](http://i.imgur.com/H9YsDzP.png)

#### PanX泛科技

PanX泛科技 最新文章
( 來源 [https://panx.asia/](https://panx.asia/) )

![alt tag](http://i.imgur.com/07N2r9N.png)

***電影***

![alt tag](http://i.imgur.com/5T32UW3.jpg)

#### 近期上映電影

近期上映的電影 ( 開眼電影網 )
( 來源 [http://www.atmovies.com.tw/movie/next/0/](http://www.atmovies.com.tw/movie/next/0/) )

![alt tag](http://i.imgur.com/hI3itad.png)

#### eyny

eyny 電影版包含 Mega 以及 Google 標題的文章
( 來源 [http://www.eyny.com/forum-205-1.html](http://www.eyny.com/forum-205-1.html) )

![alt tag](http://i.imgur.com/rIGbmWA.jpg)

***看廢文***

![alt tag](http://i.imgur.com/GJI1BwG.jpg)

#### 近期熱門廢文

( 來源 [http://disp.cc/b/PttHot](http://disp.cc/b/PttHot) )

![alt tag](http://i.imgur.com/Qm28Rso.png)

#### 即時廢文

即時八卦版廢文

( 來源 [https://www.ptt.cc/bbs/Gossiping/index.html](https://www.ptt.cc/bbs/Gossiping/index.html) )

![alt tag](http://i.imgur.com/B2YhFoS.png)

***正妹***

![alt tag](http://i.imgur.com/r6x8GzZ.jpg)

#### PTT 表特版 近期大於 10 推的文章

( 來源 [https://www.ptt.cc/bbs/Beauty/index.html](https://www.ptt.cc/bbs/Beauty/index.html) )

![alt tag](http://i.imgur.com/N00kvip.png)

#### 來張 imgur 正妹圖片

( 來源 ，自己的  imgur ，透過官方 api  [imgurpython](https://github.com/Imgur/imgurpython) 回傳圖片  )

![alt tag](http://i.imgur.com/dzTvo4z.png)

#### 隨便來張正妹圖片

( 來源 ，爬蟲 [auto_crawler_ptt_beauty_image](https://github.com/twtrubiks/auto_crawler_ptt_beauty_image)  ，從資料庫取出圖片)

![alt tag](http://i.imgur.com/emQRbRb.png)

希望這個 **阿肥bot** 能帶給大家歡樂，程式碼很多基本上就是簡單的爬蟲。

如果需要其他的功能，可以給小弟一點建議，我會盡量完成他。

## 教學

請先到 [https://business.line.me/zh-hant/](https://business.line.me/zh-hant/) 這裡登入自己

原本的 line 帳號，然後點選 Messaging API

![alt tag](http://i.imgur.com/KIzExmQ.jpg)

接下來你會看到 **開始使用Messaging API** 以及 **開始使用Developer Trial**

在這裡我們選 **開始使用Messaging API**

![alt tag](http://i.imgur.com/graLPrj.jpg)

這兩個差別在哪裡呢? 可以到同一個頁面的下方觀看，基本上就只是方案不同而已

![alt tag](http://i.imgur.com/bERbTGz.jpg)

接著就是一些設定，點選 選擇公司/經營者

![alt tag](http://i.imgur.com/d1pVdx9.jpg)

點選 新增公司/經營者

![alt tag](http://i.imgur.com/of23y7W.jpg)

填寫一些資料

![alt tag](http://i.imgur.com/7L9nulI.jpg)

line bot 的 大頭貼 以及 名稱 設定

![alt tag](http://i.imgur.com/7483ljT.jpg)

![alt tag](http://i.imgur.com/a4Mf3Rl.jpg)

設定完後，請選擇 申請

![alt tag](http://i.imgur.com/Q6q8zGA.jpg)

以上設定應該不會有什麼問題

請選擇 開始使用 API

![alt tag](http://i.imgur.com/DOEjH0F.jpg)

請選擇 確認

![alt tag](http://i.imgur.com/pKWBvsj.jpg)

這些請注意，  選擇 **允許** ，然後記得 **儲存**

![alt tag](http://i.imgur.com/Ofm9SeJ.jpg)

點選 **Line Developers**

![alt tag](http://i.imgur.com/cW9713h.jpg)

你會進入下面這個畫面，在這個畫面中，有兩個東西很重要，分別是

* Channel Secret

* Channel Access Token

***Channel Secret***

![alt tag](http://i.imgur.com/jpIEMh4.jpg)

***Channel Access Token***

如果你看到的是空的，請點選 **ISSUE** 就會顯示了

![alt tag](http://i.imgur.com/PcCEL4P.jpg)

請將你的 **Channel Secret** 以及 **Channel Access Token**

貼到 [config.ini](https://github.com/twtrubiks/line-bot-tutorial/blob/master/config.ini) 底下 ( 如不了解 .ini 的使用方法，可參考 [configparser_tutorial](https://github.com/twtrubiks/python-notes/tree/master/configparser_tutorial) )

```ini
[line_bot]
Channel_Access_Token = YOUR_CHANNEL_SECRET
Channel_Secret = YOUR_CHANNEL_SECRET
```

更多資訊可參考 [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)

接下來因為 Line Bot 需要 SSL憑證 ( https )，所以我直接使用 [Heroku](https://dashboard.heroku.com/)

如果不知道什麼是 [Heroku](https://dashboard.heroku.com/)  以及它的使用方法

請參考我之前寫的 [Deploying-Flask-To-Heroku](https://github.com/twtrubiks/Deploying-Flask-To-Heroku)

佈署

![alt tag](http://i.imgur.com/kseRgxr.jpg)

如上圖，我的網址是 [https://python-ine-bot.herokuapp.com/](https://python-ine-bot.herokuapp.com/)

接著我們要加入 Webhook URL ，請點選 EDIT ，並且加入你自己的網址，網址格式

```python
https://{你的網址}/callback
```

舉例，我的網址就是

```python
https://python-ine-bot.herokuapp.com/callback
```

![alt tag](http://i.imgur.com/5ckn24T.jpg)

![alt tag](http://i.imgur.com/TIjIM9W.jpg)

輸入完之後，可以按 VERIFY ，如果你的 CODE 正確無誤，就會顯示 Success

![alt tag](http://i.imgur.com/Mey5FKF.jpg)

不過我使用 [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)當我按下 VERIFY，卻出現錯誤，不過是可以正常運作，所以暫時先不管他。

![alt tag](http://i.imgur.com/wb0Qw5W.jpg)

關於上述這個問題，可以到 [issues 2](https://github.com/twtrubiks/line-bot-tutorial/issues/2)
以及 [issues 3](https://github.com/twtrubiks/line-bot-tutorial/issues/3) 觀看說明。( 感謝熱心的網友 )

基本上到這裡就是完成了，趕快去加入自己的 line bot 玩玩看吧~

只要我有新的想法，我會同步更新在這篇文章， line bot 還有很多好玩的地方

## 使用 imgur 官方 api

透過 imgur 官方 api  [imgurpython](https://github.com/Imgur/imgurpython) ,

從自己的相簿隨機回傳一張正妹照片，

請到下方獲取自己的 CLIENT_ID ,  CLIENT_SECRET  , 以及自己相簿的 album_id

![alt tag](http://i.imgur.com/nQNQVD7.jpg)

並將自己的資料輸入在下方程式碼

```python
client_id = 'YOUR_IMGUR_CLIENT_ID'
client_secret = 'YOUR_IMGUR__CLIENT_SECRET'
album_id = 'YOUR_IMGUR_ALBUM_ID'
```

更多詳細的介紹可參考 [imgurpython](https://github.com/Imgur/imgurpython)

## 其他補充

只要有使用到網址，請記得一定都要用 **https**

舉例

```pyhton
image_message = ImageSendMessage(
            original_content_url="https://example.com.img1.jpg",
            preview_image_url="https://example.com.img1.jpg"
        )
```

## 設定選單

有一些東西是必須到 line 的官網去設定的，像是下方的選單

![alt tag](http://i.imgur.com/IB3hBl8.jpg)

請到 [https://admin-official.line.me/](https://admin-official.line.me/) 選擇自己的 bot ，然後開始設定，

建立圖片影音內容 -> 圖文訊息選單 ( 如下圖 )

![alt tag](http://i.imgur.com/igKd6Og.png)

顯示設定，請選擇 ***反映***，不然會沒有效果

![alt tag](http://i.imgur.com/pEHSxUH.png)

接著選擇樣式，

記得，***選單內容設定*** 全部都要設定，不然會沒有效果

![alt tag](http://i.imgur.com/u0bzYu7.png)

最後，那個主要兩個字非常礙眼 ( 如下圖 )

![alt tag](http://i.imgur.com/Lv3BMyz.jpg)

我們可以從這裡把它關掉

帳號設定 -> 基本設定

![alt tag](http://i.imgur.com/bwjWijG.png)

將 行動官網選單 設定為 隱藏 即可

![alt tag](http://i.imgur.com/Q1qvjTT.png)

## Heroku 注意事項

有些人可能會遇到佈署失敗的問題，可以試著將 [runtime.txt](https://github.com/twtrubiks/line-bot-tutorial/blob/master/runtime.txt) 修改為 3.6.2

## 執行環境

* Python 3.6.2

## Reference

* [line messaging-api](https://devdocs.line.me/en/#messaging-api)
* [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
* [imgurpython](https://github.com/Imgur/imgurpython)

## License

MIT license

# Window Programming Final Project — TypeRacer打字練習遊戲

<img width="1058" height="516" alt="image" src="https://github.com/user-attachments/assets/e46c32e7-b3ec-49db-a45e-e65521db34da" />

## 專題特色

- 支援三種遊戲模式：單人遊玩、雙人連機(Client-Server架構)、太鼓模式
- 街機風格介面、賽車打字進度條
- 即時用戶回饋動畫(錯字回饋、文章自動換行)
- 打字速度與準確率統計

## 專題架構

```
final_project/src/
├── articles  # 打字文章題庫
├── main.py  # 程式標題畫面，遊戲模式選擇控制
├── game.py  # 打字遊戲核心邏輯
├── multiplayer_game.py  # 雙人連機遊戲核心邏輯
├── host_gui.py  # 主機端 GUI 控制介面
├── join_gui.py  # 玩家端 GUI 控制介面
├── type_beat_trainer.py  # 太鼓模式遊戲核心邏輯
├── *.pptx / *.pdf # 說明文件
```

## 技術細節

* GUI 使用 `tkinter` 建立，包含倒數計時、地鼠按鈕、分數顯示等元件
* 使用`socket`建立 TCP 連線，主機會廣播玩家進度與接收玩家分數
* 使用 `threading` 管理玩家連線與 GUI 更新
* 自定義 TCP 封包管理雙人連機遊戲連線與進度管控

## 畫面展示

![image](https://media.discordapp.net/attachments/676755269656510464/1421128362071687270/type_scroll.gif?ex=68d7e86c&is=68d696ec&hm=a49c36eb42844854b5cb82514dfbfe1c8524de59e974ff520b913d520e0d5ec9&=&width=1604&height=902)
![image](https://media.discordapp.net/attachments/676755269656510464/1421129545876246619/multi_result.gif?ex=68d7e987&is=68d69807&hm=bc6a30ecf23c6149f01ac8b5e2ee7078f8082bf65455fad7d339c6bbe61a983a&=&width=1604&height=902)
![image](https://media.discordapp.net/attachments/676755269656510464/1421129276895264768/TypeBeat.gif?ex=68d7e946&is=68d697c6&hm=b1825c0046f5d712592925bf7040f39544878b1685d631afcc627e5896f3c8b2&=&width=1604&height=902)

# next-websocket-chat-backend

* 下記をフロントエンドとして使用する
  - (https://github.com/tetsuo-nobe/next-websocket-chat)

* このバックエンドでは、Amazon API Gateway の WebSocket API と統合した AWS Lambda 関数を作成する。

* WebSocket で接続し、下記のメッセージを送信すると回答を受信する
    - `{"action": "sendtext", "text": prompt}`
* WebSocket 接続用 URL は、スタック作成の出力として表示される。それをフロントエンドの .env に NEXT_PUBLIC_WebSocket_URL で指定する
    -  例: wss://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev
* フロントエンドのページへアクセスの後、右上に [接続中] と表示されれば WebSocket 接続に成功
    - その後、チャットを開始できる

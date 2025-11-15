import boto3
import json
import os

API_ENDPOINT = os.environ["API_ENDPOINT"]
STAGE = os.environ["STAGE"]
MODEL_ID = os.environ["MODEL_ID"]

# 推論パラメータの値
temperature = 0.5
# 推論パラメータの値の設定
inference_config = {"temperature": temperature}
# システムプロンプト
system_prompts = [{"text": "あなたは優秀なアシスタントです。問い合わせ内容に丁寧に応答して下さい。"}]

def lambda_handler(event,context):
    # AWS SDK のクライアントオブジェクトの作成
    brt = boto3.client(service_name='bedrock-runtime')
    apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=f"{API_ENDPOINT}/{STAGE}")
    # 接続 ID の取得
    connectionId = event.get('requestContext', {}).get('connectionId')
    # メッセージの取得
    body_content = json.loads(event.get('body', {}))
    # 基盤モデルへのリクエストメッセージの構成
    text = body_content.get('text')
    message_1 = {
      "role": "user",
      "content": [{"text": f"{text}"}]
    }
    messages = []
    messages.append(message_1)
    
    # Bedrock の基盤モデルの ID を指定
    modelId = MODEL_ID
    # Bedrock の基盤モデルへリクエストを送信
    try:
        response = brt.converse_stream(modelId=modelId,messages=messages,system=system_prompts,inferenceConfig=inference_config)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"{e}"
        }
    # レスポンスを取得し、Amazon API Gateway へ返信
    for event in response.get('stream'):
         if 'contentBlockDelta' in event:
            chunk = event['contentBlockDelta']['delta']['text']
            try:
                apigw_management.post_to_connection(ConnectionId=connectionId, Data=json.dumps(chunk))
            except Exception as e:
                return {
                    "statusCode": 500,
                    "body": f"{e}"
                }
    return {
        "statusCode": 200
    }
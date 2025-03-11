from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from pydantic import BaseModel

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS設定（フロントエンドのアクセスを許可）
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 会話履歴を保持するためのリスト
messages = [
    {
        "role": "system",
        "content": "あなたはB社営業の山田秀一です。意地悪かつ慇懃無礼に対応し、最後に必ず【微笑】【強気】【皮肉】【困惑】【妥結】【冷たい】のタグをつけてください。"
    }
]

@app.get("/")
def read_root():
    return {"message": "交渉シミュレーションAPI"}

@app.post("/chat")
async def chat(message: dict):
    import openai, os
    openai.api_key = os.getenv("OPENAI_API_KEY")

    user_message = message.get("message")
    messages.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    # 表情タグ抽出
    expressions = ["微笑", "強気", "皮肉", "困惑", "妥結", "冷たい"]
    expression = "微笑"  # デフォルト
    for exp in expressions:
        if f"【{exp}】" in reply:
            expression = exp
            reply = reply.replace(f"【{exp}】", "").strip()

    return {"message": reply, "expression": expression}

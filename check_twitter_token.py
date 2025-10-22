import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TWITTER_BEARER_TOKEN')
print(f"✅ Token found: {bool(token)}")
print(f"📏 Token length: {len(token) if token else 0} characters")
if token:
    print(f"🔑 Token starts with: {token[:30]}...")
    print(f"🔑 Token ends with: ...{token[-10:]}")
else:
    print("❌ TWITTER_BEARER_TOKEN not found in .env")



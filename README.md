#課堂練習2

import pandas as pd
import requests

url = "https://www.scrapethissite.com/pages/forms/"

# 1. 準備面具 (User-Agent)，偽裝成一般 Windows 電腦的 Chrome 瀏覽器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 2. 先用 requests 帶著面具去請求網頁
print("正在連線至網站...")
response = requests.get(url, headers=headers)

# 3. 檢查有沒有成功被放行 (狀態碼 200 代表成功)
if response.status_code == 200:
    # 4. 把成功拿到的網頁 HTML 內容，交給 Pandas 去找表格
    dfs = pd.read_html(response.text)
    
    df = dfs[0] # 取得第一個表格
    df.to_excel('hockey_teams.xlsx', index=False)
    print("🎉 爬取成功！資料已儲存為 hockey_teams.xlsx")
else:
    print(f"❌ 爬取失敗，伺服器狀態碼：{response.status_code}")

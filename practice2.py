import requests
from bs4 import BeautifulSoup
import csv
import logging
import os

# 1. 設定日誌 (Logging)
# 設定為 DEBUG 級別，這樣 requests 底層的 urllib3 連線細節就會自動寫入 log
logging.basicConfig(
    filename='w03.log',
    level=logging.DEBUG, 
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    encoding='utf-8'
)

# 目標網址
url = "https://www.scrapethissite.com/pages/forms/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

try:
    # 2. 送出 Request 取得網頁
    response = requests.get(url, headers=headers, timeout=10)
    
    # 記錄狀態碼與網址 (對應圖片中的 [INFO] 日誌)
    logging.info(f"狀態碼={response.status_code}, 網址={response.url}")

    if response.status_code == 200:
        # 3. 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 尋找網頁中的資料表格 (<table class="table">)
        table = soup.find("table", class_="table")
        
        # 提取表頭 (表格中的 <th> 標籤)
        headers_list = [th.text.strip() for th in table.find_all("th")]
        
        # 提取每一列資料 (表格中 class="team" 的 <tr> 標籤)
        rows = []
        for tr in table.find_all("tr", class_="team"):
            # 取出該列中所有儲存格 <td> 的文字內容
            row_data = [td.text.strip() for td in tr.find_all("td")]
            if row_data:
                rows.append(row_data)
                
        # 4. 將資料寫入 CSV 檔案
        csv_filename = "output.csv"
        # 使用 utf-8-sig 編碼，避免 Excel 開啟 CSV 時中文亂碼
        with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(headers_list) # 寫入第一行表頭
            writer.writerows(rows)        # 寫入下方所有資料列
            
        # 記錄寫入成功與檔案路徑的日誌 (對應圖片中的 [INFO] 日誌)
        logging.info(f"寫入 {len(rows)} 筆資料")
        logging.info(f"已存檔至 : {os.path.abspath(csv_filename)}")
        
        print("爬取完成！請查看左側檔案總管是否成功產生 output.csv 與 w03.log")
        
except Exception as e:
    logging.error(f"發生錯誤: {e}")
    print("執行失敗，請查看 w03.log 了解詳細錯誤。")
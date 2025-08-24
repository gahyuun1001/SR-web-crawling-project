import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from pykrx import stock
from urllib.parse import quote
from datetime import datetime

# pandas 출력 설정
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 200)

# 사용자 입력 받기
input_name = input("크롤링할 종목명을 입력하세요 (예: 카카오): ").strip()
start_date_input = input("시작일을 입력하세요 (예: 2023-07-01): ").strip()
end_date_input = input("종료일을 입력하세요 (예: 2025-07-25): ").strip()

# 날짜 형식 변환
start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
end_date = datetime.strptime(end_date_input, "%Y-%m-%d")

# 종목명 → 종목코드 변환
ticker_list = stock.get_market_ticker_list(market="ALL")
ticker_name_map = {stock.get_market_ticker_name(code): code for code in ticker_list}

if input_name not in ticker_name_map:
    print(f"[오류] '{input_name}'에 해당하는 종목코드를 찾을 수 없습니다.")
else:
    item_code = ticker_name_map[input_name]
    base_url = "https://finance.naver.com/research/"
    headers = {"User-Agent": "Mozilla/5.0"}

    data = []

    for i in range(1, 7):  # 페이지 수 조정 가능
        url = f"https://finance.naver.com/research/company_list.naver?searchType=itemCode&itemName={quote(input_name)}&itemCode={item_code}&page={i}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table.type_1 tr")[2:]

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            a_tag = cols[1].find("a", href=True)
            if not a_tag or not a_tag["href"].startswith("company_read.naver"):
                continue

            title = a_tag.text.strip()
            detail_url = base_url + a_tag["href"]
            broker = cols[2].text.strip()
            pdf_tag = cols[3].find("a", href=True)
            pdf_link = pdf_tag["href"] if pdf_tag and pdf_tag["href"].endswith(".pdf") else None
            date_str = cols[4].text.strip()

            # 작성일 필터링
            try:
                date = datetime.strptime(date_str, "%y.%m.%d")
            except:
                continue

            if not (start_date <= date <= end_date):
                continue

            # 상세 페이지 크롤링 (목표가, 투자의견)
            try:
                detail_res = requests.get(detail_url, headers=headers)
                detail_soup = BeautifulSoup(detail_res.text, "html.parser")

                target_price = detail_soup.select_one("em.money")
                investment_opinion = detail_soup.select_one("em.coment")

                target_price_text = target_price.text.strip() if target_price else None
                opinion_text = investment_opinion.text.strip() if investment_opinion else None
            except:
                target_price_text = None
                opinion_text = None

            data.append({
                "제목": title,
                "상세페이지링크": detail_url,
                "증권사": broker,
                "PDF 링크": pdf_link,
                "작성일": date_str,
                "목표가": target_price_text,
                "투자의견": opinion_text
            })

            time.sleep(0.3)

    # DataFrame 생성 (링크 있는 버전)
    df_link = pd.DataFrame(data)
    display(df_link.style.set_properties(**{'text-align': 'left'}).set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'left')]}]
    ))

    # Excel 저장 (링크 있는 버전)
    filename = f"{input_name}_{start_date_input}~{end_date_input}_리포트 수집.xlsx"
    df_link.to_excel(filename, index=False, engine='openpyxl')
    print(f"\n✅ 엑셀 파일로 저장 완료: {filename}")

    # DataFrame 생성 (링크 없는 버전)
    df_2 = pd.DataFrame(data)
    df_2 = df_2.drop(columns=["상세페이지링크", "PDF 링크"])
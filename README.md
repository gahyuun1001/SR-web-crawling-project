# SR Web Crawling Project

## 📌 프로젝트 개요
이 프로젝트는 증권사 리서치 리포트를 자동으로 수집하고,
목표주가·투자의견 데이터를 추출하여 실제 주가와 비교하기 위해 진행되었습니다.  
데이터 크롤링부터 분석까지 과정을 주피터 노트북으로 구현하였습니다.

## 🚀 주요 기능
- 종목명과 수집 기간을 입력
- 입력받은 네이버 증권 리포트 크롤링 (종목명, 제목, 증권사, 작성일, PDF 링크 수집)
- 리포트 본문에서 목표주가 및 투자의견 추출
- 리포트 데이터와 실제 주가 데이터 매칭
- 목표주가 오차율 계산 및 시각화

## 🛠 사용 기술
- Python
- Pandas, Matplotlib
- BeautifulSoup
- Jupyter Notebook

## ⚡ 실행 방법 (수정필요)
```bash
git clone https://github.com/gahyuun1001/sr-web-crawling-project.git
cd sr-web-crawling-project
pip install -r requirements.txt
jupyter notebook

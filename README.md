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
- 목표주가 오차율 계산

## 📊 EWM 오차율 (Exponentially Weighted Mean Error)

정의: 리포트 발표일이 가까울수록 더 큰 가중치를 주는 방식으로, 증권사 목표주가의 예측 오차율을 계산한 지표입니다.

이유: 오래된 리포트보다는 최신 리포트가 더 신뢰도가 높다고 판단하여, 최근 데이터를 강조하기 위해 사용했습니다.

계산 방식:

기본 오차율 = (목표가 − 실제 주가) ÷ 실제 주가 × 100

여기에 시간 반감기(halflife) 90일을 적용하여, 시간이 지날수록 영향력이 절반으로 줄어들도록 가중 평균을 적용했습니다.

해석:

값이 낮을수록 최근 리포트 기준으로 실제 주가와의 차이가 적다는 뜻 → 해당 증권사의 예측력이 높다고 볼 수 있습니다.

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


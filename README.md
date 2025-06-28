# insta-qr-nametag

## 만드는 방법
- 이름표_데이터.csv 파일에 이름과 인스타그램 ID 를 저장
- nametag.py 파일에서 폰트 경로 잡아주기
- 아래 명령어 실행하면 pdf 파일이 생성됨

```
python -m venv .venv
source .venv/bin/activate
pip install pandas
python nametag.py
```
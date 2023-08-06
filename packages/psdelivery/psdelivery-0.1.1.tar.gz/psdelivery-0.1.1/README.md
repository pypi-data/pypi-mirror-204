# 📦 psdelivery

[![Test](https://github.com/team-angeline/psdelivery/actions/workflows/dev-test.yml/badge.svg)](https://github.com/team-angeline/psdelivery/actions/workflows/dev-test.yml)
[![CI](https://github.com/team-angeline/psdelivery/actions/workflows/ci.yml/badge.svg)](https://github.com/team-angeline/psdelivery/actions/workflows/ci.yml)
![GitHub](https://img.shields.io/github/license/team-angeline/psdelivery)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psdelivery?logo=python&logoColor=white)
[![PyPI](https://img.shields.io/pypi/v/psdelivery?label=pypi%20package&logo=pypi&logoColor=white)](https://pypi.org/project/psdelivery)
[![codecov](https://codecov.io/gh/team-angeline/psdelivery/branch/main/graph/badge.svg?token=LFC7Z4PGCT)](https://codecov.io/gh/team-angeline/psdelivery)

```shell
pip install psdelivery
```

## Introduction 
여러 코딩 사이트의 코딩 문제들을 크롤링하는 라이브러리 입니다. 초기 버전이라 기본 수준의 기능만 지원하지만. 차후 더 많은 기능들을 추가할 예정입니다. 왜냐면 재가 제 메인 프로젝트에 쓸 거니깐요.

## 🙋‍♂️ Functions

### Implemented
* 해당 사이트에서 코딩문제를 가져올 수 있습니다.
    * 백준 (solved.ac)
    * 리트코드 (leetcode)
* 파이썬 프로젝트에 모듈로 사용할 수 있고, CLI 환경에서도 바로 사용할 수 있습니다.
    * CLI 환경해서 명령어를 통해 실행할 경우, 결과 데이터는 JSON으로 저장됩니다.

### Will be Implemented
* 해당 사이트에도 코딩문제를 가져올 예정입니다.
    * 코드포스 (codeforces)
    * 해커랭크 (hackerrank)
* 여러 페이지 범위의 문제 리스트를 뽑아올 수 있습니다.
    * 해당 사이트의 모든 문제들도 하나의 명령어로 가져올 수 있습니다.
* 특정 문제에 대한 세부 정보를 가져올 수 있습니다.
    * 알고리즘 태그를 가져올 수 있습니다.

## ⭐ Required
* 반드시 크롬이 설치되어 있어야 합니다.
    * Debian계열의 경우, bin디렉토리에 크롬을 설치하는 Shell Script가 있습니다.
* 파이썬 버전은 반드시 ```3.10``` 이상이어야 합니다.

## 💽 How To Install For Developer
크롬과 파이썬이 설치되어있다는 가정 하에 설명합니다.

1. requirements.txt를 통해 패키지를 설치합니다.
2. 끗

## Usage
### As Command Line
✔️ **Version 확인하기**
```shell
python -m psdelivery version

# 0.1.0
```

📚 **문제 리스트 가져오기**
```
python -m psdelivery getlist -t <topic> -sp <page index> -o <output json file>
```
* **Options**
    * -t(--topic): 코딩 페이지 사이트를 명시합니다. 데이터를 가지고올 수 있는 사이트는 다음과 같습니다.
        * 백준: ```baekjoon``` 또는 ```solved.ac```
        * 리트코드: ```leetcode```
    * -sp(--single-page): 페이지 인덱스를 나타냅니다. 해당 옵션을 명시하지 않으면 1페이지의 문제 리스트를 가져옵니다.
    * -o(--output): 코딩문제 데이터를 저장할 파일 루트를 명시합니다.
* **example**
    ```
    python -m psdelivery getlist -t baekjoon -sp 3 -o output.json
    ```

### As Python Module

```python
from psdelivery import PsDelivery

"""
PsDelivery 객체 생성
topic은 크롤링할 사이트 이름을 입력합니다.

백준: baekjoon 또는 solved.ac
리트코드: leetcode
"""
crawler = PsDelivery(topic='leetcode')

"""
특정 페이지의 문제 리스트를 가져옵니다.
page:
    가져올 페이지 쪽수를 입력합니다. 반드시 1 이상이어야 합니다.
serialize:
    일반적인 리턴된 리스트의 요소는 ProblemItem이라는 객체 입니다. 
    serialize=True로 설정하면 ProblemItem을 Dict 형태로 직렬화 합니다. 
    Default값은 False 입니다.
"""
result = crwaler.get_list_by_single_page(page=1)
"""
return: [<ProbmeItem>, <ProblemItem>, ...]
"""

result_as_json = crawler.get_list_by_single_page(page=2, serialize=True)
"""
return: [<Dict>, <Dict>, ...]
"""
```

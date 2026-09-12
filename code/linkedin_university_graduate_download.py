from pathlib import Path
import time

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ==================================================
# LinkedIn에서 실제로 검색할 학교명
# ==================================================

UNIVERSITIES = [
    "서울대학교",
    "Yonsei University 연세대학교",
    "고려대학교",
    "서강대학교",
    "성균관대학교(SKKU)",
    "한양대학교",
    "중앙대학교",
    "Kyung Hee University 경희대학교",
    "한국외국어대학교 (Hankuk University of Foreign Studies)",
    "University of Seoul-서울시립대학교",
    "Ewha Womans University 이화여자대학교",
    "건국대학교",
    "동국대학교",
    "홍익대학교",
    "국민대학교",
    "숭실대학교",
    "세종대학교",
    "단국대학교",
    "광운대학교",
    "명지대학교",
    "상명대학교",
    "가톨릭대학교",
    "Inha University 인하대학교",
    "Ajou University(아주대학교)",
    "서울과학기술대학교",
    "Pusan National University",
    "경북대학교(Kyungpook National University)",
    "인천대학교",
    "충남대학교",
    "전남대학교",
    "충북대학교",
    "한국과학기술원(KAIST)",
    "포항공과대학교",
    "DGIST (대구경북과학기술원)",
    "광주과학기술원",
    "울산과학기술원"
]

# ==================================================
# LinkedIn 학교명 → Google Apps Script용 학교명
# ==================================================

UNIVERSITY_NAME_MAP = {
    "서울대학교": "서울대학교",
    "Yonsei University 연세대학교": "연세대학교",
    "고려대학교": "고려대학교",
    "서강대학교": "서강대학교",
    "성균관대학교(SKKU)": "성균관대학교",
    "한양대학교": "한양대학교",
    "중앙대학교": "중앙대학교",
    "Kyung Hee University 경희대학교": "경희대학교",
    "한국외국어대학교 (Hankuk University of Foreign Studies)": "한국외국어대학교",
    "University of Seoul-서울시립대학교": "서울시립대학교",
    "Ewha Womans University 이화여자대학교": "이화여자대학교",
    "건국대학교": "건국대학교",
    "동국대학교": "동국대학교",
    "홍익대학교": "홍익대학교",
    "국민대학교": "국민대학교",
    "숭실대학교": "숭실대학교",
    "세종대학교": "세종대학교",
    "단국대학교": "단국대학교",
    "광운대학교": "광운대학교",
    "명지대학교": "명지대학교",
    "상명대학교": "상명대학교",
    "가톨릭대학교": "가톨릭대학교",
    "Inha University 인하대학교": "인하대학교",
    "Ajou University(아주대학교)": "아주대학교",
    "서울과학기술대학교": "서울과학기술대학교",
    "Pusan National University": "부산대학교",
    "경북대학교(Kyungpook National University)": "경북대학교",
    "인천대학교": "인천대학교",
    "충남대학교": "충남대학교",
    "전남대학교": "전남대학교",
    "충북대학교": "충북대학교",
    "한국과학기술원(KAIST)": "한국과학기술원",
    "포항공과대학교": "포항공과대학교",
    "DGIST (대구경북과학기술원)": "대구경북과학기술원",
    "광주과학기술원": "광주과학기술원",
    "울산과학기술원": "울산과학기술원"
}


def search_company(
        company,
        company_decoration,
        linkedin_year,
        company_color,
        colors,
        footer_color,
        company_logo_b64=None
):
    results = {}

    # ==================================================
    # Chrome 프로필
    # ==================================================

    profile_path = Path(
        "/Users/handokyung/Desktop/DOK/DOK-univ_news_official/linkedin_profile"
    )

    profile_path.mkdir(
        parents=True,
        exist_ok=True
    )

    options = Options()

    options.add_argument(
        f"--user-data-dir={profile_path}"
    )

    options.add_argument(
        "--profile-directory=Default"
    )

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    driver = webdriver.Chrome(
        options=options
    )

    driver.maximize_window()

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});
"""
        }
    )

    wait = WebDriverWait(
        driver,
        20
    )

    people_url = (
            "https://www.linkedin.com/company/"
            + company
            + "/people/"
    )

    try:

        # ==================================================
        # LinkedIn 회사 People 페이지 접속
        # ==================================================

        driver.get(people_url)

        time.sleep(2)

        # ==================================================
        # 대학별 검색
        # ==================================================

        for school in UNIVERSITIES:

            print()
            print("=" * 60)
            print(f"{school} 검색 중...")
            print("=" * 60)

            try:

                # ==================================================
                # 1. 출신 학교 필터 버튼 클릭
                #
                # 학교명 텍스트는 매번 바뀔 수 있으므로
                # "출신 학교" 영역 자체를 기준으로 찾는다.
                # ==================================================

                school_filter = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//div[@aria-label="필터: 학교"]'
                            '/parent::div[@role="button"]'
                        )
                    )
                )

                driver.execute_script(
                    "arguments[0].click();",
                    school_filter
                )

                time.sleep(1)

                # ==================================================
                # 2. 학교 검색 input 찾기
                # ==================================================

                school_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//input[@placeholder="학교 추가"]'
                        )
                    )
                )

                school_input.clear()

                # ==================================================
                # 3. 학교명 입력
                # ==================================================

                school_input.send_keys(
                    school
                )

                time.sleep(1)

                # ==================================================
                # 4. 검색 결과 가져오기
                # ==================================================

                school_options = wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            '//div[@data-component-type="LazyColumn"]'
                            '//div[@role="option"]'
                        )
                    )
                )

                matched_school = None

                # ==================================================
                # 5. 검색 결과 학교명 정확히 일치하는지 확인
                #
                # 중요:
                # in / startswith / endswith 사용하지 않음
                #
                # 예:
                # 서울대학교
                #
                # 서울대학교 법학전문대학원
                #
                # 위 둘은 서로 다른 학교로 판단
                # ==================================================

                for option in school_options:

                    try:

                        school_span = option.find_element(
                            By.XPATH,
                            './/span'
                        )

                        school_text = school_span.text.strip()

                        print(
                            f"검색 결과 확인: {school_text}"
                        )

                        # 정확히 동일한 경우에만 선택
                        if school_text == school:
                            matched_school = option

                            print(
                                f"정확히 일치: {school}"
                            )

                            break

                    except Exception:
                        continue

                # ==================================================
                # 6. 정확히 일치하는 학교가 없는 경우
                # ==================================================

                if matched_school is None:
                    results[school] = 0

                    print(
                        f"{school}: 정확히 일치하는 학교 없음 → 0"
                    )

                    driver.get(people_url)
                    time.sleep(2)

                    continue

                # ==================================================
                # 7. 정확히 일치하는 학교 클릭
                # ==================================================

                driver.execute_script(
                    "arguments[0].click();",
                    matched_school
                )

                time.sleep(1)

                print(
                    f"{school}: 학교 선택 완료"
                )

                # ==================================================
                # 8. 결과 표시 클릭
                # ==================================================

                result_link = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//a[.//span[normalize-space(.)="결과 표시"]]'
                        )
                    )
                )

                driver.execute_script(
                    "arguments[0].click();",
                    result_link
                )

                time.sleep(2)

                # ==================================================
                # 9. 결과에서 학교 정보 찾기
                # ==================================================

                school_results = wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            '//a[@role="checkbox"][.//p]'
                        )
                    )
                )

                matched_result = None

                # ==================================================
                # 10. 결과 학교명과 검색 학교명을 정확히 비교
                # ==================================================

                for school_result in school_results:

                    try:

                        paragraphs = school_result.find_elements(
                            By.TAG_NAME,
                            "p"
                        )

                        if len(paragraphs) < 2:
                            continue

                        # 학교명
                        result_school_text = (
                            paragraphs[0]
                            .text
                            .strip()
                        )

                        # 인원수
                        count_text = (
                            paragraphs[1]
                            .text
                            .strip()
                        )

                        print(
                            f"결과 학교 확인: {result_school_text}"
                        )

                        # ==================================================
                        # 정확히 동일한 학교명인지 확인
                        #
                        # 예:
                        #
                        # 검색:
                        # Yonsei University 연세대학교
                        #
                        # 결과:
                        # Yonsei University 연세대학교
                        #
                        # → 인정
                        #
                        # 결과:
                        # 연세대학교
                        #
                        # → 불인정
                        #
                        # 결과:
                        # Yonsei University 연세대학교 법학전문대학원
                        #
                        # → 불인정
                        # ==================================================

                        if result_school_text == school:
                            matched_result = (
                                school_result,
                                count_text
                            )

                            print(
                                f"결과 학교 정확히 일치: {school}"
                            )

                            break

                    except Exception:
                        continue

                # ==================================================
                # 11. 정확히 일치하는 결과가 없는 경우
                # ==================================================

                if matched_result is None:

                    results[school] = 0

                    print(
                        f"{school}: 결과 학교 불일치 → 0"
                    )

                else:

                    _, count_text = matched_result

                    try:

                        count = int(
                            count_text.replace(",", "")
                        )

                        results[school] = count

                        print(
                            f"{school}: {count}"
                        )

                    except ValueError:

                        results[school] = 0

                        print(
                            f"{school}: 인원수 변환 실패 → 0"
                        )

                # ==================================================
                # 12. 다음 학교를 위해 People 페이지로 이동
                # ==================================================

                driver.get(people_url)

                time.sleep(2)

            except TimeoutException:

                results[school] = 0

                print(
                    f"{school}: 요소를 찾지 못함 → 0"
                )

                # 오류가 발생해도 다음 학교 검색을 위해
                # People 페이지로 돌아간다.

                try:

                    driver.get(people_url)

                    time.sleep(2)

                except Exception:
                    pass

            except Exception as e:

                results[school] = 0

                print(
                    f"{school}: 오류 발생 → 0"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )

                # 오류 발생 후 People 페이지 초기화

                try:

                    driver.get(people_url)

                    time.sleep(2)

                except Exception:
                    pass

    finally:

        driver.quit()

    # ==================================================
    # 13. 전체 결과 출력
    # ==================================================

    print()
    print("=" * 60)
    print("전체 학교 검색 결과")
    print("=" * 60)

    for school, count in results.items():
        print(
            f"{school}: {count}"
        )

    # ==================================================
    # 14. 인원수 기준 내림차순 정렬
    #
    # Python의 sorted는 stable sort이므로
    # 인원수가 같은 경우 UNIVERSITIES 순서를 유지한다.
    # ==================================================

    sorted_results = sorted(
        results.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # ==================================================
    # 15. TOP 10
    #
    # 여기까지는 LinkedIn에서 사용하는 학교명을 유지한다.
    # ==================================================

    top_10_results = [
        [school, str(count)]
        for school, count in sorted_results[:10]
    ]

    print()
    print("=" * 60)
    print("LinkedIn 기준 TOP 10")
    print("=" * 60)

    for rank, (school, count) in enumerate(
            top_10_results,
            start=1
    ):
        print(
            f"{rank}. {school} - {count}명"
        )

    # ==================================================
    # 16. Google Apps Script 전송용 학교명으로 변환
    #
    # LinkedIn:
    # Yonsei University 연세대학교
    #
    # GAS:
    # 연세대학교
    #
    # LinkedIn:
    # 성균관대학교(SKKU)
    #
    # GAS:
    # 성균관대학교
    # ==================================================

    gas_top_10_results = [
        [
            UNIVERSITY_NAME_MAP.get(
                school,
                school
            ),
            count
        ]
        for school, count in top_10_results
    ]

    print()
    print("=" * 60)
    print("Google Apps Script 전송용 TOP 10")
    print("=" * 60)

    for rank, (school, count) in enumerate(
            gas_top_10_results,
            start=1
    ):
        print(
            f"{rank}. {school} - {count}명"
        )

    # ==================================================
    # 17. Google Apps Script 전송
    # ==================================================

    data = {
        "company": company,
        "companyDecoration": company_decoration,
        "linkedin_year": linkedin_year,
        "results": gas_top_10_results,
        "companyColor": company_color,
        "colors": colors,
        "footerColor": footer_color,
        "companyLogo": company_logo_b64
    }

    response = requests.post(
        "https://script.google.com/macros/s/AKfycbz3sLKPHNK6cfh4siCRRpzeIKyTnyt8hbOZyoULPPi9NKbgENf727h5kaUD3lh0OEXi1A/exec",
        json=data,
        timeout=30
    )

    print()
    print("=" * 60)
    print("Google Apps Script 전송 결과")
    print("=" * 60)

    print(
        f"HTTP 상태 코드: {response.status_code}"
    )

    print(
        f"응답: {response.text}"
    )

    return gas_top_10_results

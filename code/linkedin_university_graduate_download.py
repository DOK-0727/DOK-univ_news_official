from pathlib import Path
import time

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

        driver.get(people_url)

        time.sleep(2)

        for school in UNIVERSITIES:

            try:

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

                school_input = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//input[@placeholder="학교 추가"]'
                        )
                    )
                )

                school_input.clear()

                school_input.send_keys(
                    school
                )

                time.sleep(1)

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

                for option in school_options:

                    try:

                        school_span = option.find_element(
                            By.XPATH,
                            './/span'
                        )

                        school_text = school_span.text.strip()

                        if school_text == school:
                            matched_school = option

                            break

                    except Exception:
                        continue

                if matched_school is None:
                    results[school] = 0

                    driver.get(people_url)
                    time.sleep(2)

                    continue

                driver.execute_script(
                    "arguments[0].click();",
                    matched_school
                )

                time.sleep(1)

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

                school_results = wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            '//a[@role="checkbox"][.//p]'
                        )
                    )
                )

                matched_result = None

                for school_result in school_results:

                    try:

                        paragraphs = school_result.find_elements(
                            By.TAG_NAME,
                            "p"
                        )

                        if len(paragraphs) < 2:
                            continue

                        result_school_text = (
                            paragraphs[0]
                            .text
                            .strip()
                        )

                        count_text = (
                            paragraphs[1]
                            .text
                            .strip()
                        )

                        if result_school_text == school:
                            matched_result = (
                                school_result,
                                count_text
                            )

                            break

                    except Exception:
                        continue

                if matched_result is None:

                    results[school] = 0

                else:

                    _, count_text = matched_result

                    try:

                        count = int(
                            count_text.replace(",", "")
                        )

                        results[school] = count

                    except ValueError:

                        results[school] = 0

                driver.get(people_url)

                time.sleep(2)

            except TimeoutException:

                results[school] = 0

                try:

                    driver.get(people_url)

                    time.sleep(2)

                except Exception:
                    pass

            except Exception as e:

                results[school] = 0

                try:

                    driver.get(people_url)

                    time.sleep(2)

                except Exception:
                    pass

    finally:

        driver.quit()

    for school, count in results.items():
        print(
            f"{school}: {count}"
        )

    sorted_results = sorted(
        results.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_10_results = [
        [school, str(count)]
        for school, count in sorted_results[:10]
    ]

    for rank, (school, count) in enumerate(
            top_10_results,
            start=1
    ):
        print(
            f"{rank}. {school} - {count}명"
        )

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

    for rank, (school, count) in enumerate(
            gas_top_10_results,
            start=1
    ):
        print(
            f"{rank}. {school} - {count}명"
        )

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

    return gas_top_10_results

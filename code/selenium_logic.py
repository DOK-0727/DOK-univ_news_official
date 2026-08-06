from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests

UNIVERSITIES = [
    "서울대학교", "연세대학교", "고려대학교", "서강대학교", "성균관대학교",
    "한양대학교", "중앙대학교", "경희대학교", "한국외국어대학교",
    "서울시립대학교", "이화여자대학교", "건국대학교", "동국대학교",
    "홍익대학교", "국민대학교", "숭실대학교", "세종대학교",
    "단국대학교", "광운대학교", "명지대학교", "상명대학교",
    "가천대학교", "인하대학교", "아주대학교", "서울과학기술대학교",
    "부산대학교", "경북대학교", "인천대학교", "충남대학교",
    "전남대학교", "충북대학교", "한국과학기술원", "포항공과대학교",
    "대구경북과학기술원", "광주과학기술원", "울산과학기술원"
]

def search_company(company, company_decoration, company_color, colors, footer_color, company_logo_b64=None):

    results = {}

    profile_path = Path("/Users/handokyung/Desktop/DOK/DOK-univ_news_official/linkedin_profile")
    Path(profile_path).mkdir(parents=True, exist_ok=True)

    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--profile-directory=Default")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )
    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});
"""
        },
    )

    wait = WebDriverWait(driver, 20)

    try:

        driver.get("https://www.linkedin.com")

        search_box = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'input[data-testid="typeahead-input"]')
            )
        )

        search_box.clear()
        search_box.send_keys(company)
        search_box.send_keys(Keys.ENTER)

        company_button = wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "페이지 보기")
            )
        )

        company_button.click()

        time.sleep(2)

        driver.get(driver.current_url.rstrip("/") + "/people/")

        for school in UNIVERSITIES:

            search_box = wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "people-search-keywords")
                )
            )

            search_box.send_keys(school)
            search_box.send_keys(Keys.ENTER)

            time.sleep(2)

            try:

                items = wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.CSS_SELECTOR,
                            "div.org-people-bar-graph-element__percentage-bar-info"
                        )
                    )
                )

                count = int(
                    items[5]
                    .find_element(By.TAG_NAME, "strong")
                    .text.replace(",", "")
                )

                results[school] = count

            except (TimeoutException, IndexError):

                results[school] = 0

            try:

                remove_button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"//button[contains(@aria-label,'{school}') and contains(@aria-label,'필터 삭제')]"
                        )
                    )
                )

                remove_button.click()

                time.sleep(1)

            except TimeoutException:

                print(f"{school} 필터 삭제 버튼을 찾지 못했습니다.")

    finally:

        driver.quit()

    sorted_results = sorted(
        results.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_10_results = [
        [school, str(count)] for school, count in sorted_results[:10]
    ]

    # Google Apps Script로 보낼 데이터에 로고 이미지(Base64) 추가
    data = {
        "company": company,
        "companyDecoration": company_decoration,
        "results": top_10_results,
        "companyColor": company_color,
        "colors": colors,
        "footerColor": footer_color,
        "companyLogo": company_logo_b64  # ★ 추가된 항목
    }

    response = requests.post(
        "https://script.google.com/macros/s/AKfycbzkuT80AMtSAzXmRQ1SNrODtd7mzvz92GIi2JknYq-ouvvgel2QJRz40xFYerCnlAAUMQ/exec",
        json=data
    )

    return results
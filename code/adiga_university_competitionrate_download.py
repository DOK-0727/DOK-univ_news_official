# adiga_dept_download.py
from pathlib import Path
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

UNIVERSITY_SET = set(UNIVERSITIES)
UNIVERSITY_ORDER = {university: index for index, university in enumerate(UNIVERSITIES)}


def search_department(department, adiga_year, admission_type):
    results_data = []

    profile_path = Path("/Users/handokyung/Desktop/DOK/DOK-univ_news_official/adiga_profile")
    Path(profile_path).mkdir(parents=True, exist_ok=True)

    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"}
    )

    wait = WebDriverWait(driver, 20)

    def get_page_results():
        wait.until(EC.presence_of_element_located((By.XPATH, '//tr[.//span[contains(@class, "univName")]]')))
        rows = driver.find_elements(By.XPATH, '//tr[.//span[contains(@class, "univName")]]')
        page_results = []
        for row in rows:
            try:
                university = row.find_element(By.CSS_SELECTOR, ".univName a").text.strip()
                university = re.sub(r"\s*\[(?:본교|분교)\]\s*$", "", university)

                if university not in UNIVERSITY_SET:
                    continue

                early_rate = row.find_element(
                    By.XPATH, './/dl[contains(@class, "univRate")][.//dt[normalize-space()="수시"]]//strong'
                ).text.strip()
                regular_rate = row.find_element(
                    By.XPATH, './/dl[contains(@class, "univRate")][.//dt[normalize-space()="정시"]]//strong'
                ).text.strip()

                page_results.append({
                    "university": university,
                    "early": early_rate,
                    "regular": regular_rate
                })
            except Exception as e:
                print(f"결과 처리 중 오류: {e}")
        return page_results

    def get_last_page():
        pagination = wait.until(EC.presence_of_element_located((By.ID, "pagination")))
        page_links = pagination.find_elements(By.XPATH, './li[not(contains(@class, "ctrlBtn"))]/a')
        page_numbers = [int(link.text.strip()) for link in page_links if link.text.strip().isdigit()]
        if not page_numbers:
            return 1
        visible_last_page = max(page_numbers)
        try:
            last_button = pagination.find_element(By.XPATH, './li[contains(@class, "nxtEnd")]/a')
            onclick = last_button.get_attribute("onclick")
            if onclick:
                match = re.search(r'fnSearch\s*\(\s*(\d+)\s*\)', onclick)
                if match:
                    end_page = int(match.group(1))
                    if end_page >= visible_last_page:
                        return end_page
        except Exception:
            pass
        return visible_last_page

    def move_to_page(page_number):
        old_rows = driver.find_elements(By.XPATH, '//tr[.//span[contains(@class, "univName")]]')
        old_first_row = old_rows[0] if old_rows else None
        driver.execute_script(f"fnSearch({page_number});")
        if old_first_row:
            try:
                wait.until(EC.staleness_of(old_first_row))
            except Exception:
                pass
        wait.until(EC.presence_of_element_located((By.XPATH, '//tr[.//span[contains(@class, "univName")]]')))
        time.sleep(0.5)

    try:
        driver.get("https://www.adiga.kr")

        major_info = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[.//p[normalize-space()="학과정보"]]')))
        major_info.click()
        wait.until(EC.invisibility_of_element_located((By.ID, "loadingAction")))

        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="학과관련 키워드"]')))
        search_button.click()

        search_input = wait.until(EC.element_to_be_clickable((By.ID, "searchKwrd")))
        search_input.clear()
        search_input.send_keys(department)
        search_input.send_keys(Keys.ENTER)

        course_all = wait.until(EC.element_to_be_clickable((By.ID, "courseAll")))
        course_all.click()

        select_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="button" and normalize-space()="선택"]')))
        select_button.click()
        time.sleep(3)

        last_page = get_last_page()

        for page in range(1, last_page + 1):
            results_data.extend(get_page_results())
            if page == last_page:
                break
            move_to_page(page + 1)

        # 중복 대학 제거
        unique_results = {r["university"]: r for r in results_data}
        results_data = list(unique_results.values())

        # 수시/정시 구분 필터링 및 정렬
        target_key = "early" if admission_type == "수시" else "regular"
        parsed_results = []
        for r in results_data:
            try:
                rate_val = float(r[target_key].replace(",", ""))
                parsed_results.append({
                    "university": r["university"],
                    "rate_str": r[target_key],
                    "rate": rate_val
                })
            except (ValueError, TypeError):
                continue

        top10 = sorted(
            parsed_results,
            key=lambda x: (-x["rate"], UNIVERSITY_ORDER.get(x["university"], 999))
        )[:10]

        top_10_results = [[item["university"], item["rate_str"]] for item in top10]

        # Google Apps Script 연동
        data = {
            "department": department,
            "adiga_year": adiga_year,
            "admission_type": admission_type,
            "results": top_10_results
        }
        try:
            requests.post(
                "https://script.google.com/macros/s/AKfycbz6YsH-szztRuxN46GpwNfvR2o977sa2MnCbfeiP1tuGbhIdglmAPb_zl-4NnlAeL12gQ/exec",
                json=data,
                timeout=5
            )
        except Exception as e:
            print(f"Apps Script 요청 중 오류 발생: {e}")

        return top_10_results

    finally:
        driver.quit()

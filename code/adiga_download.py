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


def get_last_page(driver):
    try:
        end_button = driver.find_element(By.CSS_SELECTOR, "ul.majorPagination li.nxtEnd a")
        onclick = end_button.get_attribute("onclick")
        if onclick:
            match = re.search(r"majorInfo\(['\"](\d+)['\"]\)", onclick)
            if match:
                return int(match.group(1))
    except Exception:
        pass
    try:
        page_links = driver.find_elements(By.CSS_SELECTOR, "ul.majorPagination li.numb.page-item a")
        page_numbers = [int(link.text.strip()) for link in page_links if link.text.strip().isdigit()]
        if page_numbers:
            return max(page_numbers)
    except Exception:
        pass
    return 1


def get_first_row_text(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, "table.ucpTable tbody tr:first-child").text.strip()
    except Exception:
        return ""


def convert_rate(value):
    try:
        match = re.search(r"[\d.]+", str(value).strip())
        if match:
            return float(match.group())
    except Exception:
        pass
    return 0


def search_university(university, adiga_year, admission_type, univ_color, colors, footer_color, univ_logo_b64=None):
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

    results_data = []

    try:
        driver.get("https://www.adiga.kr")
        search_input = wait.until(EC.presence_of_element_located((By.ID, "autoComplet")))
        search_input.clear()
        search_input.send_keys(university)
        search_input.send_keys(Keys.ENTER)

        major_info = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#none' and contains(., '학과 정보')]")))
        major_info.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.ucpTable tbody tr")))
        time.sleep(2)

        last_page = get_last_page(driver)
        current_page = 1

        while current_page <= last_page:
            rows = driver.find_elements(By.CSS_SELECTOR, "table.ucpTable tbody tr")
            row_count = len(rows)

            for index in range(row_count):
                try:
                    row = driver.find_element(By.CSS_SELECTOR, f"table.ucpTable tbody tr:nth-child({index + 1})")
                    full_text = row.find_element(By.CSS_SELECTOR, "td:first-child .univName a").text.strip()
                    if "[본교]" not in full_text: continue

                    univ_name = full_text.split("[본교]")[0].strip()
                    if univ_name != university: continue

                    department = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) a").text.strip()
                    rates = row.find_elements(By.CSS_SELECTOR, "dl.univRate")
                    target_rate = "0"

                    for rate in rates:
                        category = rate.find_element(By.CSS_SELECTOR, "dt").text.strip()
                        value = rate.find_element(By.CSS_SELECTOR, "dd strong").text.strip()
                        if category == admission_type:
                            target_rate = value

                    results_data.append({"department": department, "rate": target_rate})
                except Exception:
                    continue

            if current_page >= last_page: break

            # 페이지네이션 로직 복원 (11페이지 이상도 넘어가도록 처리)
            next_page = current_page + 1
            old_first_row = get_first_row_text(driver)

            try:
                # 같은 페이지 그룹 내 이동
                next_page_link = driver.find_element(By.XPATH,
                                                     f"//ul[contains(@class, 'majorPagination')]//li[contains(@class, 'numb')]//a[normalize-space(text())='{next_page}']")
                driver.execute_script("arguments[0].click();", next_page_link)
                time.sleep(1.5)
                current_page += 1
            except Exception:
                try:
                    # 다음 페이지 그룹(예: 1~10 -> 11~20) 이동 버튼 클릭
                    next_group_button = driver.find_element(By.CSS_SELECTOR, "ul.majorPagination li.nxt a")
                    driver.execute_script("arguments[0].click();", next_group_button)
                    time.sleep(1.5)

                    target_page_link = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                  f"//ul[contains(@class, 'majorPagination')]//li[contains(@class, 'numb')]//a[normalize-space(text())='{next_page}']")))
                    driver.execute_script("arguments[0].click();", target_page_link)
                    time.sleep(1.5)
                    current_page += 1
                except Exception:
                    break
    finally:
        driver.quit()

    # 중복 제거 및 최고 경쟁률 유지 로직
    unique_results = {}
    for item in results_data:
        dept = item["department"]
        rate_str = item["rate"]
        rate_float = convert_rate(rate_str)

        # 학과가 처음 등장하거나, 기존에 저장된 경쟁률보다 현재 경쟁률이 더 높은 경우에만 갱신
        if dept not in unique_results or convert_rate(unique_results[dept]) < rate_float:
            unique_results[dept] = rate_str

    # 실수(float) 값 기준으로 내림차순 정렬
    sorted_items = sorted(unique_results.items(), key=lambda x: convert_rate(x[1]), reverse=True)
    top_10_results = [[dept, rate] for dept, rate in sorted_items[:10]]

    # Google Apps Script로 전송
    data = {
        "university": university,
        "adiga_year": adiga_year,
        "admissionType": admission_type,
        "results": top_10_results,
        "univColor": univ_color,
        "colors": colors,
        "footerColor": footer_color,
        "univLogo": univ_logo_b64
    }

    # TODO: 본인의 Google Apps Script 배포 URL로 변경하세요.
    WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzRlSDf6Icnd8dO0xvnCbJ_Px639Tl8WvxtpFQ4Rf03ZdaDdkOBpsAK2PSwJAvfpcdK/exec"
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

    return top_10_results

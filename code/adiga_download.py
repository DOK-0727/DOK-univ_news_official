from pathlib import Path
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


profile_path = Path(
    "/Users/handokyung/Desktop/DOK/DOK-univ_news_official/adiga_profile"
)

Path(profile_path).mkdir(
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


university = "서울대학교"

results = {
    university: []
}


driver.get(
    "https://www.adiga.kr"
)


search_input = wait.until(
    EC.presence_of_element_located(
        (
            By.ID,
            "autoComplet"
        )
    )
)

search_input.clear()

search_input.send_keys(
    university
)

search_input.send_keys(
    Keys.ENTER
)


major_info = wait.until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "//a[@href='#none' and contains(., '학과 정보')]"
        )
    )
)

major_info.click()


wait.until(
    EC.presence_of_element_located(
        (
            By.CSS_SELECTOR,
            "table.ucpTable tbody tr"
        )
    )
)

time.sleep(2)


def get_last_page():
    try:
        end_button = driver.find_element(
            By.CSS_SELECTOR,
            "ul.majorPagination li.nxtEnd a"
        )

        onclick = end_button.get_attribute(
            "onclick"
        )

        if onclick:
            match = re.search(
                r"majorInfo\(['\"](\d+)['\"]\)",
                onclick
            )

            if match:
                return int(
                    match.group(1)
                )

    except Exception:
        pass

    try:
        page_links = driver.find_elements(
            By.CSS_SELECTOR,
            "ul.majorPagination li.numb.page-item a"
        )

        page_numbers = []

        for link in page_links:
            text = link.text.strip()

            if text.isdigit():
                page_numbers.append(
                    int(text)
                )

        if page_numbers:
            return max(
                page_numbers
            )

    except Exception:
        pass

    return 1


def get_first_row_text():
    try:
        return driver.find_element(
            By.CSS_SELECTOR,
            "table.ucpTable tbody tr:first-child"
        ).text.strip()

    except Exception:
        return ""


def collect_current_page(page_number):
    rows = driver.find_elements(
        By.CSS_SELECTOR,
        "table.ucpTable tbody tr"
    )

    row_count = len(rows)

    for index in range(row_count):

        try:
            row = driver.find_element(
                By.CSS_SELECTOR,
                f"table.ucpTable tbody tr:nth-child({index + 1})"
            )

            university_link = row.find_element(
                By.CSS_SELECTOR,
                "td:first-child .univName a"
            )

            full_text = university_link.text.strip()

            if "[본교]" not in full_text:
                continue

            university_name = (
                full_text
                .split("[본교]")[0]
                .strip()
            )

            if university_name != university:
                continue

            department = row.find_element(
                By.CSS_SELECTOR,
                "td:nth-child(2) a"
            ).text.strip()

            rates = row.find_elements(
                By.CSS_SELECTOR,
                "dl.univRate"
            )

            early_rate = "0"
            regular_rate = "0"

            for rate in rates:

                category = rate.find_element(
                    By.CSS_SELECTOR,
                    "dt"
                ).text.strip()

                value = rate.find_element(
                    By.CSS_SELECTOR,
                    "dd strong"
                ).text.strip()

                if category == "수시":
                    early_rate = value

                elif category == "정시":
                    regular_rate = value

            results[university].append(
                {
                    "department": department,
                    "수시": early_rate,
                    "정시": regular_rate
                }
            )

        except Exception:
            continue


last_page = get_last_page()

current_page = 1


while current_page <= last_page:

    collect_current_page(
        current_page
    )

    if current_page >= last_page:
        break

    next_page = current_page + 1

    old_first_row = get_first_row_text()

    try:

        next_page_link = driver.find_element(
            By.XPATH,
            "//ul[contains(@class, 'majorPagination')]"
            "//li[contains(@class, 'numb')]"
            f"//a[normalize-space(text())='{next_page}']"
        )

        driver.execute_script(
            "arguments[0].click();",
            next_page_link
        )

        if old_first_row:

            try:
                wait.until(
                    lambda d:
                    get_first_row_text()
                    != old_first_row
                )

            except Exception:
                time.sleep(1)

        else:
            time.sleep(1)

        wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "table.ucpTable tbody tr"
                )
            )
        )

        time.sleep(0.5)

        current_page += 1

    except Exception:

        try:

            next_group_button = driver.find_element(
                By.CSS_SELECTOR,
                "ul.majorPagination li.nxt a"
            )

            onclick = next_group_button.get_attribute(
                "onclick"
            )

            match = re.search(
                r"majorInfo\(['\"](\d+)['\"]\)",
                onclick
            )

            if not match:
                break

            next_group_page = int(
                match.group(1)
            )

            driver.execute_script(
                "arguments[0].click();",
                next_group_button
            )

            try:

                wait.until(
                    lambda d:
                    d.find_element(
                        By.CSS_SELECTOR,
                        "ul.majorPagination li.active a"
                    ).text.strip()
                    != str(current_page)
                )

            except Exception:
                time.sleep(1)

            target_page_link = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//ul[contains(@class, 'majorPagination')]"
                        "//li[contains(@class, 'numb')]"
                        f"//a[normalize-space(text())='{next_page}']"
                    )
                )
            )

            driver.execute_script(
                "arguments[0].click();",
                target_page_link
            )

            if old_first_row:

                try:

                    wait.until(
                        lambda d:
                        get_first_row_text()
                        != old_first_row
                    )

                except Exception:
                    time.sleep(1)

            else:
                time.sleep(1)

            wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "table.ucpTable tbody tr"
                    )
                )
            )

            time.sleep(0.5)

            current_page += 1

        except Exception:
            break


# 중복 제거

unique_results = []

seen = set()

for item in results[university]:

    key = (
        item["department"],
        item["수시"],
        item["정시"]
    )

    if key in seen:
        continue

    seen.add(
        key
    )

    unique_results.append(
        item
    )


results[university] = unique_results

def convert_rate(value):

    try:

        value = str(value).strip()

        match = re.search(
            r"[\d.]+",
            value
        )

        if match:
            return float(
                match.group()
            )

    except Exception:
        pass

    return 0

sorted_results = {
    "수시": [],
    "정시": []
}


for item in results[university]:

    sorted_results["수시"].append(
        {
            "department": item["department"],
            "value": item["수시"]
        }
    )

    sorted_results["정시"].append(
        {
            "department": item["department"],
            "value": item["정시"]
        }
    )

sorted_results["수시"].sort(
    key=lambda x: convert_rate(
        x["value"]
    ),
    reverse=True
)

sorted_results["정시"].sort(
    key=lambda x: convert_rate(
        x["value"]
    ),
    reverse=True
)

results[university] = sorted_results

print()
print("=" * 60)
print(f"{university} 수시 경쟁률")
print("=" * 60)

for index, item in enumerate(
    results[university]["수시"],
    start=1
):

    print(
        f"{index}. "
        f"{item['department']} | "
        f"수시: {item['value']}"
    )


print()
print("=" * 60)
print(f"{university} 정시 경쟁률")
print("=" * 60)

for index, item in enumerate(
    results[university]["정시"],
    start=1
):

    print(
        f"{index}. "
        f"{item['department']} | "
        f"정시: {item['value']}"
    )
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup
web = "https://www.google.com/maps/place/Beutea+@+Sunway+Pyramid/@3.0718724,101.6032882,870m/data=!3m1!1e3!4m8!3m7!1s0x31cc4d235910170b:0xf2ec66d021c629b6!8m2!3d3.0718724!4d101.6058631!9m1!1b1!16s%2Fg%2F11tc8vs3ph?entry=ttu&g_ep=EgoyMDI1MDQyMy4wIKXMDSoJLDEwMjExNDUzSAFQAw%3D%3D"
path = r"C:\Users\Lenovo\Downloads\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

# Use WebDriverWait instead of implicit wait
wait = WebDriverWait(driver, 10)

driver.get(web)

# Wait for reviews panel
scrollable_div = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde "]')
    )
)

# Scroll to load more reviews
for _ in range(10):
    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div
    )
    time.sleep(2)

user = []
review_list = []
rating_list = []

# # Wait until the reviews are loaded
# reviews = wait.until(
#     EC.presence_of_all_elements_located(
#         (By.XPATH, '//div[contains(@class, "jftiEf fontBodyMedium")]')
#     )
# )

reviews = driver.find_elements(By.XPATH, '//div[@class="jftiEf fontBodyMedium "]')

for review in reviews:
    # Get user name
    user_name = review.find_element(By.XPATH, './/div[contains(@class, "d4r55")]').text

    # Get rating

    rating = review.find_element(
        By.XPATH, './/span[contains(@class, "kvMYJc")]'
    ).get_attribute("aria-label")

    try:
        review_text = review.find_element(
            By.XPATH, './/span[contains(@class, "wiI7pd")]'
        ).text
    except:
        review_text = ""

    user.append(user_name)
    rating_list.append(rating)
    review_list.append(review_text)

# Create DataFrame
df = pd.DataFrame(
    {
        "user": user,
        "rating": rating_list,
        "review": review_list,
    }
)

# Output
print(df)
df.to_csv("google_reviews.csv", index=False, encoding='utf-8-sig')

driver.quit()

!pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

browser = webdriver.Chrome()
browser.get('https://www.flipkart.com/apple-iphone-13-starlight-128-gb/product-reviews/itmc9604f122ae7f?pid=MOBG6VF5ADKHKXFX&lid=LSTMOBG6VF5ADKHKXFXZVXGTL&sortOrder=MOST_HELPFUL&certifiedBuyer=false&aid=overall')

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

oneline = []
products = []
rating = []
months = []

try:
    for i in range(1200):
        print('Page', i + 1)

        product = browser.find_elements(By.XPATH, "//div[@class='t-ZTKy']")
        line = browser.find_elements(By.XPATH, "//p[@class='_2-N8zT']")
        rate = browser.find_elements(By.XPATH, "//div[@class='_3LWZlK _1BLPMq' or @class='_3LWZlK _32lA32 _1BLPMq' or @class='_3LWZlK _1rdVr6 _1BLPMq']")
        month = browser.find_elements(By.XPATH, "//p[@class='_2sc7ZR']")

        for p in product:
            products.append(p.text.replace("\n", "").replace("READ MORE", ""))
        for p in line:
            oneline.append(p.text)
        for p in rate:
            rating.append(p.text)
        for p in month:
            months.append(p.text)

        wait = WebDriverWait(browser, 10)  # Adjust the timeout as needed
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
            next_button.click()
        except TimeoutException:
            print("Timed out waiting for Next button to be clickable. End of scraping.")
            break
        except ElementClickInterceptedException:
            print("Element click intercepted. Handling overlay...")
            next_button.click()

        sleep(2)

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    browser.quit()

df = pd.DataFrame({'First_Expression':oneline,'Review':products,'Rating':rating,'Month':months})
csv_file_path = 'csv/group3.csv'
df.to_csv(csv_file_path, index=False)

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor


def read_file_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

url = 'https://app.monprotocol.ai/questing/missions'
proxies = read_file_lines('proxies.txt')
user_agents = read_file_lines('user_agents.txt')
accounts = read_file_lines("accounts.txt")


class MonBot:
    def __init__(self, proxy, user_agent, account):
        self.proxy = proxy
        self.user_agent = user_agent
        self.account = account
        self.driver, self.wait = self.create_driver()

    def create_driver(self):

        seleniumwire_options = {
            'verify_ssl': False,
            'proxy': {
                'http': f'http://{self.proxy}',
                'https': f'https://{self.proxy}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        chrome_options.add_argument('--silent')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, seleniumwire_options=seleniumwire_options, options=chrome_options)
        wait = WebDriverWait(driver, 15)

        stealth(driver,
                user_agent=self.user_agent,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        return driver, wait

    def twitter_login(self):

        try:
            self.driver.get('https://twitter.com/')
            cookies = {'name': 'auth_token', 'value': self.account}
            time.sleep(3)
            self.driver.add_cookie(cookies)
            self.driver.refresh()
            time.sleep(1)
            if self.driver.current_url == "https://twitter.com/home":
                return True
            else:
                print("Token dead")
                return False
        except Exception as ex:
            print(f"Error: {ex}")
            return False

    def get_mon(self):
        self.driver.get('https://app.monprotocol.ai/questing')
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div/div[3]/div[2]/button[1]'))).click() #connect twitter
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/div/div/div[1]/div[3]/div'))).click() #Authorize app
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='REFERRAL CODE']"))).send_keys('Varfozel')
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div/div/div[3]/div/button'))).click()
        time.sleep(2)

    def follow_mon(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'FOLLOW')]]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'FOLLOW ON X')]]"))).click()
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))).click()
        self.driver.close()
        self.driver.switch_to.window(window_handles[0])
        follow_mon_done = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Congrats!']")))
        if follow_mon_done:
            print("Succesfully followed Mon")
        else:
            print("Could't follow Mon")
        self.driver.get(url)

    def follow_pixelmon(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'FOLLOW')]]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'FOLLOW ON X')]]"))).click()
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))).click()
        self.driver.close()
        self.driver.switch_to.window(window_handles[0])
        follow_mon_done = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Congrats!']")))
        if follow_mon_done:
            print("Succesfully followed Pixelmon")
        else:
            print("Could't follow Pixelmon")
        self.driver.get(url)

    def follow_giulio(self):

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'FOLLOW')]]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'FOLLOW ON X')]]"))).click()
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[-1])
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))).click()
        self.driver.close()
        self.driver.switch_to.window(window_handles[0])
        follow_mon_done = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Congrats!']")))
        if follow_mon_done:
            print("Succesfully followed Giulio")
        else:
            print("Could't follow Giulio")
        self.driver.get(url)

    def close_driver(self):
        self.driver.quit()

    def run(self):
        try:
            if self.twitter_login():
                print("Login successful, proceeding with other actions.")
                self.get_mon()
                self.follow_mon()
                self.follow_pixelmon()
                self.follow_giulio()
                self.close_driver()
            else:
                print("Login failed, stopping execution.")
                self.close_driver()
        except Exception as ex:
            print(f"Error: {ex}")


def run_bot_for_account(account_data):
    proxy, user_agent, account = account_data
    bot = MonBot(proxy, user_agent, account)
    bot.run()

if __name__ == "__main__":
    account_data_list = [(proxies[i % len(proxies)], user_agents[i % len(user_agents)], account) for i, account in enumerate(accounts)]
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(run_bot_for_account, account_data_list)
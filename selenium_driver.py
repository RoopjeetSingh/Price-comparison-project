from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import threading
import time
from selenium.webdriver.common.keys import Keys
import requests
from io import BytesIO
from collections import OrderedDict

options = Options()
# options = webdriver.ChromeOptions()
user_agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/107.0.0.0 Safari/537.36',
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
              "Connection": "close", "Upgrade-Insecure-Requests": "1"}
options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
driver2 = webdriver.Chrome(executable_path="./chromedriver", options=options)
driver3 = webdriver.Chrome(executable_path="./chromedriver", options=options)
# driver4 = webdriver.Chrome(options=options)

start = time.time()


def get_from_amazon(product: str, keywords: tuple = ()):
    products = dict()
    try:
        driver.get("https://www.amazon.com/s?k=" + product)
        xpath = f'//div[contains(@class, "a-section a-spacing-base")'
        for keyword in keywords:
            xpath += f' and .//span[contains(text(), "{keyword.capitalize()}")]'
        xpath += ']'

        items = WebDriverWait(driver, 5).until(
            ec.presence_of_all_elements_located((By.XPATH, xpath)))
        for item in items:
            try:
                product_link = item.find_element(By.XPATH,
                                                 './/a[@class="a-link-normal s-underline-text s-underline-link-text '
                                                 's-link-style a-text-normal"]')
                product_title = item.find_element(By.XPATH,
                                                  './/span[contains(@class, "a-color-base a-text-normal")]')
                product_price_whole = item.find_element(By.XPATH, './/span[@class="a-price-whole"]')
                product_price_fraction = item.find_element(By.XPATH, './/span[@class="a-price-fraction"]')
                product_img = item.find_element(By.XPATH, './/img[@class="s-image"]')
                response = requests.get(product_img.get_attribute("src"))
                img = BytesIO(response.content)
                products[product_title.text] = [float(product_price_whole.text + '.' + product_price_fraction.text),
                                                product_link.get_attribute("href"), img]
                print("Name:", product_title.text, "Price",
                      product_price_whole.text + '.' + product_price_fraction.text,
                      "Link", product_link.get_attribute("href"))
                try:
                    price_per_lb = item.find_elements(By.XPATH, './/span[@class="a-size-base a-color-secondary"]')
                    price_per_lb = [i.text for i in price_per_lb]
                    price_per_lb = ''.join(price_per_lb)
                    products[product_title.text].append(price_per_lb)
                except NoSuchElementException:
                    pass
            except NoSuchElementException:
                pass
            except ValueError:
                pass
            except StaleElementReferenceException:
                pass
            except requests.exceptions.ConnectionError:
                pass
    except NoSuchElementException:
        print('No such element')
    except TimeoutException:
        print("Timeout")
    except StaleElementReferenceException:
        print('stale element')
    except ElementNotInteractableException:
        print('Element not interactable')
    products = sorted(products.items(), key=lambda x: x[1][0])
    dic = OrderedDict()
    for i in products:
        dic[i[0]] = i[1]
    return dic


def get_from_target(product: str, keywords: tuple = ()):
    products = dict()
    driver2.get("https://www.target.com/s?searchTerm=" + product)
    try:
        driver2.implicitly_wait(5)
        xpath = f'//div[contains(@class,"styles__ProductCardVariantDefaultWrapper-sc-bcz5ql")'
        for keyword in keywords:
            xpath += f' and .//a[contains(text(), "{keyword.capitalize()}")]'
        xpath += ']'
        # driver2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        items = WebDriverWait(driver2, 10).until(
            ec.presence_of_all_elements_located((By.XPATH, xpath)))
        for item in items:
            try:
                product_title = item.find_element(By.XPATH,
                                                  './/a[contains(@class,"Link__StyledLink-sc-frmop1-0 styles__StyledTitleLink-sc-h3r0um-1")]')
                product_price_whole = item.find_element(By.XPATH, './/span[@data-test="current-price"]')
                product_img = item.find_element(By.XPATH, './/picture[contains(@class,"styles__FadeInPicture-sc-12vb1rw-0")]//source')
                response = requests.get(product_img.get_attribute("srcset"))
                img = BytesIO(response.content)
                products[product_title.text] = [float(product_price_whole.text.replace("$", "")),
                                                product_title.get_attribute("href"), img]
                try:
                    price_per_lb = item.find_element(By.XPATH, './/span[@class="h-text-sm h-text-grayDark"]')
                    products[product_title.text].append(price_per_lb.text)
                except NoSuchElementException:
                    pass
                print("Name:", product_title.text, "Price", float(product_price_whole.text.replace("$", "")), "Link",
                      product_title.get_attribute("href"))
            # except NoSuchElementException:
            #     print('no such element')
            except StaleElementReferenceException:
                print('stale element')
            except ValueError:
                print('value error')
            except requests.exceptions.ConnectionError:
                print('no image')
    # except NoSuchElementException:
    #     print('No such element')
    # except TimeoutException:
    #     print('timeout target')
    except StaleElementReferenceException:
        print('stale element')
    except ElementNotInteractableException:
        print('element not interactable')
    products = sorted(products.items(), key=lambda x: x[1][0])
    dic = OrderedDict()
    for i in products:
        dic[i[0]] = i[1]
    return dic


done = 1
def get_from_wholefoods(product: str, brand: tuple, keywords: tuple):
    driver3.get("https://www.wholefoodsmarket.com/search?text=" + product)
    products = dict()
    try:
        WebDriverWait(driver3, 5).until(ec.element_to_be_clickable((By.ID,
                                                                    "pie-store-finder-modal-search-field"))).send_keys("30005")
        WebDriverWait(driver3, 5).until(ec.element_to_be_clickable((By.XPATH,
                                                                    '//li[@class="wfm-search-bar--list_item"]'))).click()

        xpath = f'//div[@class="w-pie--product-tile"'
        for keyword in keywords:
            xpath += f' and .//h2[contains(text(), "{keyword.capitalize()}")]'
        for b in brand:
            xpath += f' and .//span[contains(text(), "{b.capitalize()}")]'
        xpath += ']'
        items = WebDriverWait(driver3, 5).until(
            ec.presence_of_all_elements_located((By.XPATH, xpath)))
        for item in items:
            try:
                brand_title = item.find_element(By.XPATH, './/span[@class="w-cms--font-disclaimer"]')
                product_title = item.find_element(By.XPATH, './/h2[@class="w-cms--font-body__sans-bold"]')
                product_price_whole = item.find_element(By.XPATH, './/span[@class="regular_price"]//b')
                product_link = item.find_element(By.XPATH, './/a[@class="w-pie--product-tile__link"]')
                product_img = item.find_element(By.XPATH, './/img[@class=" ls-is-cached lazyloaded"]')
                response = requests.get(product_img.get_attribute("src"))
                img = BytesIO(response.content)
                products[brand_title.text + " " + product_title.text] = [
                    product_price_whole.text,
                    product_link.get_attribute("href"), img]
                print("Name:", brand_title.text + " " + product_title.text, "Price",
                      product_price_whole.text
                      , "Link:", product_link.get_attribute("href"))
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass
            except ValueError:
                pass
            except requests.exceptions.ConnectionError:
                pass
    except TimeoutException:
        print('timeout whole foods')
    except StaleElementReferenceException:
        print('stale element')
    except ElementNotInteractableException:
        print('element not interactable')
    return products


# def get_from_sprouts(product: str, keywords: tuple = ()):
#     driver4.get("https://shop.sprouts.com/search?search_term=bread")
#     WebDriverWait(driver4, 5).until(
#         ec.presence_of_element_located((By.ID, 'shopping-selector-shop-context-intent-instore'))).click()
#     search_box = driver4.find_element(By.XPATH, '//*[@id="sticky-react-header"]/div/div[2]/div[1]/form/div/input')
#     search_box.send_keys(Keys.CONTROL + "a")
#     search_box.send_keys(Keys.DELETE)
#     search_box.send_keys(product)
#     search_box.send_keys(Keys.ENTER)
#
#     xpath = f'//div[@class="css-yxhcyb"'
#     for keyword in keywords:
#         xpath += f' and .//div[contains(text(), "{keyword.capitalize()}")]'
#     xpath += ']'
#     products = dict()
#     try:
#         items = WebDriverWait(driver4, 5).until(
#             ec.presence_of_all_elements_located((By.XPATH, xpath)))
#         for item in items:
#             try:
#                 product_title = item.find_element(By.XPATH, './/div[@class="css-15uwigl"]')
#                 product_price_whole = item.find_element(By.XPATH, './/span[@class="css-coqxwd"]')
#                 products[product_title.text] = [
#                     float(product_price_whole.text.replace(" /ea", '').replace(" /lb", '').replace("$", '')),
#                     driver4.current_url]
#                 print("Name:", product_title.text, "Price",
#                       float(product_price_whole.text.replace(" /ea", '').replace(" /lb", '').replace("$", ''))
#                       , "Link:", driver4.current_url)
#             except ValueError:
#                 pass
#             except requests.exceptions.ConnectionError:
#                 pass
#             except NoSuchElementException:
#                 pass
#             except StaleElementReferenceException:
#                 pass
#     except TimeoutException:
#         pass
#     except NoSuchElementException:
#         pass
#     except StaleElementReferenceException:
#         pass
#     except ElementNotInteractableException:
#         pass
#     return products


if __name__ == "__main__":
    company_name = "Nature's own"
    product_name = "Whole wheat bread"
    necessary_words = ('whole', 'wheat', 'bread') + tuple(company_name.split())
    t1 = threading.Thread(target=get_from_amazon, args=(company_name + " " + product_name, necessary_words))
    t2 = threading.Thread(target=get_from_target, args=(company_name + " " + product_name, necessary_words))
    t3 = threading.Thread(target=get_from_wholefoods,
                          args=(company_name + " " + product_name, tuple(company_name.split())
                                , ('whole', 'wheat', 'bread')))
    # t4 = threading.Thread(target=get_from_sprouts, args=(company_name + " " + product_name, necessary_words))

    # t1.start()
    t2.start()
    # t3.start()
    # t4.start()
    # t1.join()
    t2.join()
    # t3.join()
    # t4.join()

    print(time.time() - start)
    driver.quit()
    driver2.quit()
    driver3.quit()
    # driver4.quit()


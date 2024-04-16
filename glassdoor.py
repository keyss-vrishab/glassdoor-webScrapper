from selenium import webdriver
from selenium.webdriver.chrome.options import Options    
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fuzzywuzzy import fuzz
from selenium.common.exceptions import NoSuchElementException
import time 
import csv
import sys



class GlassDoor:


    def __init__(self):
        company = ' '.join([str(elem) for elem in sys.argv[1:]])
        self.Reviews = '';
        self.Jobs = '';
        self.company_names = [];
        self.value = company
        self.score = []
        self.detailed_review = [];
        self.rating = [];
        mobile_emulation = {
        "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }

        chrome_options = Options()
        
        chrome_options.headless = True

        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        self.driver = webdriver.Chrome(chrome_options = chrome_options)
        self.driver.set_window_rect(width=360, height=640)


    def login(self):
        
        driver = self.driver
        driver.get("https://www.glassdoor.co.in/index.htm");
        time.sleep(5);
        try:
            element = driver.find_element(By.XPATH,"//*[@id='SiteNav']/nav/div[1]/div[1]/button").click()
            time.sleep(2)
        
        except Exception as e:
            print("no signin button")
        try:
            element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,"//*[@id='modalUserEmail']"))
                )

        except Exception as e:
            print(e)
        element.send_keys("gawajay629@haizail.com");
        
        time.sleep(2);
                
        element = driver.find_element(By.XPATH,'//*[@id="LoginModal"]/div/div/div[2]/div[2]/div/div/div/div/div/div/form/div[2]/button/span').click()

        time.sleep(2);
        try:
            element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="modalUserPassword"]'))
                )

        except Exception as e:
            print(e)
        element.send_keys("vrishab@123");
  
        time.sleep(2);
        element = driver.find_element(By.XPATH,'//*[@id="LoginModal"]/div/div/div[2]/div[2]/div/div/div/div/div/div/form/div[2]/button/span').click()
          
          
        time.sleep(2);     
      
      
    def company_tab(self):
        
        driver = self.driver
        time.sleep(2);
        
        try:
            element = WebDriverWait(driver, 5).until(
                
                  EC.element_to_be_clickable((By.CSS_SELECTOR,"#SiteNav  nav:nth-child(2) > div >div >div:nth-child(2)  > div:nth-child(2)"))
                
            ).click()

        except Exception as e:
             print("error in clicking for companies")
        try:
            element = WebDriverWait(driver, 5).until(
                
                  EC.element_to_be_clickable((By.CSS_SELECTOR,"#SearchForm .search__SearchStyles__iconBtn .SVGInline-svg"))
            ).click()

        except Exception as e:
             print("no search menu")
        time.sleep(2);
        try:
            element = WebDriverWait(driver, 5).until(
                
                
                EC.element_to_be_clickable((By.XPATH,"/html/body/header/nav[1]/div/div/div/div[4]/div[3]/div[2]/form/div[2]/div[1]/div/div/input"))
            )
            element.send_keys(self.value)
            element.send_keys(Keys.RETURN)

        except Exception as e:
            print(e)
        time.sleep(2)
 
 
    def fetch_company_suggestions(self):

        driver = self.driver
        isPresent = True
        while(isPresent):    
            print("just reached")
            time.sleep(3)
            try:
                              
                cards = driver.find_elements(By.CSS_SELECTOR, '#ReviewSearchResults > article.mainCol > div >div.single-company-result.module ')
            
                for i in cards:
                    try:
                        reviews = i.find_element(By.CSS_SELECTOR,'#ReviewSearchResults > article.mainCol > div >div.single-company-result.module  > div.row.justify-content-between > div.col-lg-7 > div.row.justify-content-start >div.col-9.pr-0 >h2 >a')
                        
                        self.company_names.append(reviews.text)
                        print(reviews.text)
                     
                    except Exception as e:
                        print("issue with getting name")
            except Exception as e:
                print("no listing here ")
            try:
                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#FooterPageNav > div.pagingControls.cell.middle>ul>li.next>a'))).is_displayed()
                isPresent = True;
                
                try:
                    s = driver.find_element(By.CSS_SELECTOR,'#FooterPageNav > div.pagingControls.cell.middle>ul>li.next>a')
                    driver.execute_script("arguments[0].click();",s)
                except Exception as e:
                        print("was not able to click")
            except Exception as e:         
                isPresent = False;
                print("no next button")
           
            print(self.company_names)
   
   
    def submit(self):
        
        
        driver = self.driver;
        for value in self.company_names:        
            self.score.append(fuzz.ratio(self.value.lower(), value.lower())); 
        time.sleep(2);
        print(self.score)

        try:
            element = WebDriverWait(driver, 10).until(
                
                  EC.element_to_be_clickable((By.CSS_SELECTOR,"#SearchForm > div.d-flex.d-lg-none.pr-std > button"))
            ).click()

        except Exception as e:
             print("no search menu")
        time.sleep(2);   
        try:
            self.driver.find_element(By.XPATH,"//*[@id='scKeyword']").clear()
        except Exception as e:
            print("issue while cleaning search bar")
            # print(e)
            
        try:
            element = WebDriverWait(driver, 5).until(
                  EC.element_to_be_clickable((By.XPATH,"//*[@id='scKeyword']"))

            )            
            element.send_keys(self.company_names[self.score.index(max(self.score))])
            
            
            
            element.send_keys(Keys.RETURN);   
            
        except Exception as e:
            print("issue while sending company name")
            # print(e)
            
        time.sleep(2)
   
        try:
            dropdown = driver.find_element(By.CSS_SELECTOR,'#MainCol > div > div:nth-child(2) > div > div > div >div:nth-child(2) >h2 >a').click()
            # print("199")
        except Exception as e:
            pass
             

    def next_page_details(self):
       
        driver = self.driver
        time.sleep(2)
        data = []
        fields = ['rating','title' , 'likes' , 'dislikes'] 
        star_value=''
        pros_data=''
        cons_data=''
        heading_data = ''
        isPresent = True
        try:
          
            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#EIProductHeaders > div > a.d-flex.flex-column.justify-content-end.align-items-center.pb-xsm.cellWrapper.reviews > p'))).click()
        except Exception as e:
            print("dbkjasbdkabdkjbj")
            # print(e)
        # clicking on review
        print("123")
        time.sleep(5)
       
        while(isPresent):
            time.sleep(10)
    
            print("just clicked !!!!!!!!!")
            time.sleep(3)
            try:
                cards = driver.find_elements(By.CSS_SELECTOR, '#ReviewsFeed > ol > li ')
            
                for i in cards:
                    
              
                    try:
                        reviews = i.find_elements(By.CSS_SELECTOR,'#ReviewsFeed > ol > li > div > div  > div > div > div  > span:nth-child(1)')
                        star_value = reviews[0].text
                     
                    except Exception as e:
                        
                        reviews[0].text = "no star here"
                     
                    try:
                        reviews1 = i.find_elements(By.CSS_SELECTOR, '.mt-xsm.px-std > h2 a')
                        heading_data = reviews1[0].text
                      
                    except Exception as e:
                           
                            heading_data = "no heading here"
                  
                    
                    try:
                            value =i.find_element(By.CSS_SELECTOR,' #ReviewsFeed > ol > li > div.gdGrid > div:nth-child(5) > div.px-std >div:nth-child(1) >p.mb-0.strong')
                           
                            print(value.text)
                            if value.text == "Pros" :
                               
                                try:
                                    pros_value = i.find_element(By.CSS_SELECTOR,' #ReviewsFeed > ol > li > div.gdGrid > div:nth-child(5)> div.px-std > div >p:nth-child(2)')
                                    pros_data = pros_value.text
                                   
                                except Exception as e:
                                    pros_data ="did not got pros value or data "
                                 
                    except Exception as e:
                            pros_data = "no pro element"
                         
                    
                    try:
                            cons =i.find_element(By.CSS_SELECTOR,'  #ReviewsFeed > ol > li > div.gdGrid > div:nth-child(5) > div.px-std >div:nth-child(2) >p.mb-0.strong')
                            
                            print(cons.text)
                            if cons.text == "Cons" :
                               
                                try:
                                    cons_value = i.find_element(By.CSS_SELECTOR,' #ReviewsFeed > ol > li > div.gdGrid > div:nth-child(5) > div.px-std >div:nth-child(2) >p:nth-child(2)')
                                    cons_data = cons_value.text
                                  
                                except Exception as e:
                                    cons_value.text = "did not get cons value or data "
                                  
                    except Exception as e:
                            cons_data = "no cons element here"
                    
                    data.append([star_value,heading_data,pros_data,cons_data])
                          
            except Exception as e:
                print("did not got review listing")
            
            try:
                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#MainContent > div > div:nth-child(1) > div.d-flex.flex-column.align-items-top > div > div.pageContainer > button.nextButton.css-1hq9k8.e13qs2071'))).is_displayed()
                isPresent = True;
                try:
                    s = driver.find_element(By.CSS_SELECTOR,'#MainContent > div > div:nth-child(1) > div.d-flex.flex-column.align-items-top > div > div.pageContainer > button.nextButton.css-1hq9k8.e13qs2071')
                   
                    driver.execute_script("arguments[0].click();",s)
                except Exception as e:
                        print("was not able to click")
            except Exception as e:         
                isPresent = False;
                print("no next button")
           
            print(isPresent)
            time.sleep(2)
        with open('export_glassdoor.csv', 'w') as f:
            
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(data)


if __name__ == '__main__':  
    st = GlassDoor();
    st.login();
    st.company_tab();
    st.fetch_company_suggestions();
    st.submit();
    st.next_page_details();
    
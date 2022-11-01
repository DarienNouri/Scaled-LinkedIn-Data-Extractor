from shutil import ExecError
from sqlite3 import Time
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from googlesearch import search
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import gender_guesser.detector as gender
from IPython.display import display
from CoegilSdk import Coegil
import os 
import re
from dateutil.relativedelta import relativedelta
from datetime import datetime
import re
from datetime import date 
import pytz
import warnings
warnings.filterwarnings("ignore")
os.environ['LINKEDIN_USERNAME'] = 'darien.nouri@nyu.edu'
os.environ['LINKEDIN_PASSWORD'] = "Amrikor11"
os.environ['API_KEY'] = 'RmcxkJ9K3hv5aRvSgrgh-SD8bDaH5qvBhSsdIaE4W-DySzlVAiu9pfcWvWlGVb'
username = os.environ.get('LINKEDIN_USERNAME')
password = os.environ.get('LINKEDIN_PASSWORD')
api_key = os.environ.get('API_KEY')

try:
    sdk = Coegil(api_key) 
except:
    sdk = False



if username is None:
    raise Exception('Make sure to enter a valid username "LINKEDIN_USERNAME"')
if password is None:
    raise Exception('Make sure to enter a valid password "LINKEDIN_PASSWORD"')
if api_key is None:
    raise Exception('Make sure to enter a valid API KEY "API_KEY"')
if sdk is False:
    raise  Exception('Invalid API KEY "API_KEY"')









class linkedin:
    global driver
    global get_soup
    driver = webdriver.Chrome(r"C:\Users\darie\OneDrive\VM DS Projects\Coegil\chromedriver.exe")
    def login(email,password):
        driver.get("https://linkedin.com/uas/login")
        time.sleep(3)
        username = driver.find_element(By.ID,"username").send_keys(email)
        pword = driver.find_element(By.ID,"password").send_keys(password) 
        driver.find_element_by_xpath("//button[@type='submit']").click()   
    def get_soup():
        src = driver.page_source
        soup = BeautifulSoup(src, from_encoding = "utf-8",features="lxml")
        soup.prettify()
        return soup
    def scroll(last = 0):
        finalScroll = last+1000
        start = time.time()
        initialScroll = last
        finalScroll = finalScroll
        
        while True:
            driver.execute_script(f"window.scrollTo({initialScroll}, {finalScroll})")
            initialScroll = finalScroll
            finalScroll += 1000
            time.sleep(2)
            end = time.time()
            if round(end - start) > 20:
                break
        return finalScroll
    def load_posts_count(load= 10):
        for post_num in range(load):
            try:
                myElem = WebDriverWait(driver, 1,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'button[class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]')))
                driver.find_element(by=By.CSS_SELECTOR,value='button[class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]').click()
            except TimeoutException:
                soup = get_soup()
                break
            
    

    def crawl_posts():
        count = 1
        data_posts = {}
        
        try:
            potent = driver.find_elements_by_css_selector('button[class="artdeco-pill artdeco-pill--slate artdeco-pill--3 artdeco-pill--choice ember-view mr1 mb2"]')
            for i in potent:
                if i.text == 'Posts':
                    i.click()
        except:
            pass
        for post_num in range(12):
            
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'button[class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]')))
                #WebDriverWait(driver, 4).until(EC.presence_of_element_located(by=By.CSS_SELECTOR,value='button[class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]'))
                #WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR,'button[class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]')))
                driver.find_element(by=By.CSS_SELECTOR,value='button[class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]').click()
                
            except TimeoutException:
                soup = get_soup()
                print('fewer than 100 posts')
                break
            
        soup = get_soup()

        
        soup = get_soup()
        containers = soup.findAll("div", {'class':'ember-view occludable-update'})
        
        soup = get_soup()
        containers = soup.findAll("div", {'class':'ember-view occludable-update'})
        for container in containers:   
            data_dict = {}
            #Try function to make sure its a post and not a promotion
            try:
                posted_date = container.find("span",{"class":"feed-shared-actor__sub-description t-12 t-normal t-black--light"}).find("span",{"class":"visually-hidden"})
                text_box = container.find("span",{"class":"break-words"})
                text = text_box.find((text_box.find("span",{"dir":"ltr"})))
                new_likes = container.find("span", {"class":"social-details-social-counts__reactions-count"})
                new_comments = container.find("li", {"class": "social-details-social-counts__item social-details-social-counts__comments social-details-social-counts__item--with-social-proof"})

                #Appending date and text to lists
                post_dates = (posted_date.text.strip())
                post_texts = (text_box.text.strip())
                
                                    
                try:
                    post_likes = (new_likes.text.strip(']'))
                except:
                    post_likes = (0)
                    pass
                try:
                    post_comments = (new_comments.text.strip())                           
                except:                                                           
                    post_comments = (0)
                    pass
            
                
            except:
                pass
            
            def ago_do_date(ago):
                value, unit = re.search(r'(\d+) (\w+) ago', ago).groups()
                if not unit.endswith('s'):
                    unit += 's'
                delta = relativedelta(**{unit: int(value)})
                return ((datetime.now() - delta).date())
            if count == 100:
                break
            post_dates_current = str(ago_do_date(post_dates))
            data_dict = ({'post_dates':post_dates_current,'post_texts':post_texts,'post_likes':post_likes,'post_comments':post_comments})
            data_posts[count] = data_dict
            count+=1
        return data_posts



    def set_posts_filter(): ##For scraping company posts
        soup = get_soup()
        time.sleep(3)
        first_in = driver.find_element(by=By.CSS_SELECTOR,value='li-icon[class="sort-dropdown__icon"]')
        check_sortby = first_in.find_element_by_xpath('..').text
        try:
            while 'Recent' not in check_sortby :
                driver.find_element(by=By.CSS_SELECTOR,value='button[class="artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view display-flex t-normal t-12 t-black--light"]').click()
                time.sleep(4)
                driver.find_element(by=By.CSS_SELECTOR,value='button[class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--tertiary ember-view justify-flex-start ph4"]').click()
                soup = get_soup()
                check_sortby = soup.find("button", {'class':'artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view display-flex t-normal t-12 t-black--light'}).next_element.next_element.text
        except:
            pass
    def check_if_company_or_individual(input_link):
        if 'company' in input_link:
            company = True
        else:
            company = False
        return company
    def create_link(input):
        
        if 'linkedin' not in input:
            input_link = 'https://www.linkedin.com/company/'+ input
        else:
            input_link = input
        print(input_link)
    
            
        return input_link
    def company_basics():

        soup = get_soup()
        name = soup.find('h1',{'class':"ember-view t-24 t-black t-bold full-width"}).text.strip()
        try:
            industry = soup.find('div',{'class':"org-top-card-summary-info-list__info-item"}).text.strip()
            company_website = soup.find('a',{'class':"link-without-visited-state ember-view"}).text.strip()
        except:
            industry = 'null' 
            company_website = 'null'
        
       
        phone_check = soup.find_all('span',{'class':"link-without-visited-state"})
        for i in phone_check:
            phone_num = ''
            try:
                check2 = re.search(r"(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})",i.text)
                if check2 is not None:
                    phone_num = (i.text.strip())
            except:
                phone_num = ''
                continue
            
                


        
        employee_count = soup.find('dd',{'class':"text-body-small t-black--light mb1"}).text.strip()
        try:
            employees_on =  str(soup.find('dd',{'class':"text-body-small t-black--light mb4"}).text.strip())
            employees_on_linkedin = (employees_on[:employees_on.index(" on LinkedIn")])
        except:
            employees_on = 'null'
            employees_on_linkedin = 'null'

        founded_specialty_raw = soup.find_all('dd',{'class':"mb4 text-body-small t-black--light"})
        founded_on = ''
        try:
            for i in founded_specialty_raw:
                check = re.search(r"[0-9]{4}", i.text.strip())
                if  check is not None:
                    value = (i.text.strip())
                    if value.isnumeric():
                        founded_on = (value)
        except:
            founded_on = 'null'

      
        
        try:
            address = soup.find('p',{'class':"t-14 t-black--light t-normal break-words"}).text.strip()
        except:
            address = 'none or multiple'
        
        
        try:
            founded_specialty_raw = soup.find_all('dt',{'class':"mb1 text-heading-small"})
            for i in founded_specialty_raw:
                if 'Headquarters' in i.text:
                            address = i.next_element.next_element.next_element.text.strip()
                        
        except:
            address = 'null'
        special_raw = soup.find_all('dd',{'class':"mb4 text-body-small t-black--light"})
        for i in special_raw:
            try:
                if ',' in (i.text.strip()) and len(i.text.strip().split(','))>3:
                    specialties = i.text.strip()
                    
                    continue
            except:
                specialties = ''
        params = [name,industry,specialties,founded_on,company_website,phone_num,employee_count,employees_on_linkedin,address]
        for i in params:
            if i not in locals() or len(i) < 1:
            
                i = 'null'
        company_info_dict = {'Company Name':name,'Industry':industry,'Speialties':specialties,'Founded':founded_on,'Company Website':company_website,'Phone Number':phone_num,'Size':employee_count,'Employees On LinkedIn':employees_on_linkedin,'Address':address}
        return company_info_dict
    def user_basic_info():
        
        d = gender.Detector()
        soup = get_soup()
        user_profile = get_soup()
        name = user_profile.find('h1',{'class':"text-heading-xlarge inline t-24 v-align-middle break-words"})
        name = name.text.strip()
        try:
            split_name = name.split(" ", 2)
            first_name = split_name[0]
            last_name = split_name[-1]
            full_name = first_name+'_'+last_name
        except:
            first_name = name
            last_name = 'no last name'
            full_name = name
        #Get Liker Gender
        user_gender = (d.get_gender(split_name[0])+"^ ")
        try:
            #Get Liker Location
            location = user_profile.find('span',{'class':"text-body-small inline t-black--light break-words"}).text
            liker_locations = (location.text.strip()+"^ ")
        except:
            liker_locations = ("No Location")

        try:
            #Get Liker Headline
            headline = user_profile.find('div',{"class":"text-body-medium break-words"}).text.strip()
            liker_headlines = (headline.strip())
        except:
            liker_headlines = ("No Headline")
        try:
                soup = get_soup()
            
                bio = soup.find('div',{"class":"pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center"}).find('span',{'class':"visually-hidden"}).text          
                time.sleep(1)        
        except:
                bio = ('No Bio')
        try:
            followers = soup.find('p',{"class":"pvs-header__subtitle text-body-small"}).next_element.next_element.text.strip()
        except:
            followers = ('No Follower Count') 
        basic_info = {'full_name':full_name,'First':first_name,'Last':last_name,'Gender':user_gender[:-2],'Headline':liker_headlines,'Location':liker_locations,'Followers':followers,'Bio':bio}
        return(basic_info)
    def user_edu_exp():##maybe add link arg
        count_edu = 0
        count_exp = 0
        edu_dict = {}
        exp_dict = {}
        soup = get_soup()
        cards = soup.find_all('li',{'class':"artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
        
        for i in cards:
            try:
                institution  = (i.find('span',{'class':"mr1 hoverable-link-text t-bold"}).find('span',{'class':"visually-hidden"}).text)
                try:
                    degree = (i.find('span',{'class':"t-14 t-normal"}).find('span',{'class':"visually-hidden"}).text)
                except:
                    degree = ('null')
                
                try:
                    date = (i.find('span',{'class':"t-14 t-normal t-black--light"}).find('span',{'class':"visually-hidden"}).text)
                    if count_edu == 1:
                            date_check = date

                    try:
                        date_regex = re.findall(r"[0-9]{4}", date_check)[-1] 
                    except:
                        pass
                    try:
                        local_date_regex = re.findall('[1-3][0-9]{3}',date)  
                        if int(date_regex) < int(local_date_regex[-1]) +5:     
                            continue  
                    except:
                        pass
                except:
                    date= ('null')
                count_edu+=1
                education = {}
                
                education =  {'School':institution,'Degree':degree,'Date':date}
                edu_dict[count_edu] = education
            except:
                try:
                    expi = (i.find('span',{'class':"t-14 t-normal"}).find('span',{'class':"visually-hidden"}).text)
                    exp_date = (i.find('span',{'class':"t-14 t-normal t-black--light"}).find('span',{'class':"visually-hidden"}).text)
                    expiernece = {}
                    expierence  = {'Expierence':expi,'Date':exp_date}  
                    count_exp+=1        
                    exp_dict[count_exp] = expierence
                except:
                    
                    continue
            
            
            

        education_df = (pd.DataFrame.from_dict(edu_dict))
        expierence_df = (pd.DataFrame.from_dict(exp_dict))
        display(education_df)
        display(expierence_df)
        return [edu_dict,exp_dict]
    def date_utc():
        
        today = date.today()
        today_format = str(datetime.utcnow())
       
        return today_format
    def main(input,email,password):
        print(linkedin.date_utc())
        username = 'darien.nouri@nyu.edu'
        password = "Amrikor11"
        api_key = 'RmcxkJ9K3hv5aRvSgrgh-SD8bDaH5qvBhSsdIaE4W-DySzlVAiu9pfcWvWlGVb'
        input_link = linkedin.create_link(input)
        print(input_link)
        company = linkedin.check_if_company_or_individual(input_link)
        linkedin.login(email,password)
        if company == True:
                print('Company')
                information = 'Company Profile'
                current_date = linkedin.date_utc()
                try:
                    driver.get(input_link+'/about/')
                    time.sleep(2)
                    user_info = linkedin.company_basics()
                    
                    print(user_info)
                    user_edu = {}
                except:
                    print('no user info')
                    user_info = {}
                    user_edu = {}
                save_name = user_info.get('Company Name')
                if save_name is None:
                    print('Company Not Found')
                    dont_save = True
                else:
                    dont_save = False
                    posts_link = input_link + '/posts/?feedView=all'
                    
                    driver.get(posts_link)
                    linkedin.set_posts_filter()
                    #linkedin.load_posts_count()
                    posts_payload = linkedin.crawl_posts()
                    payload = {'Company Name':user_info['Company Name'],'Date':current_date,'Profile':user_info,'Company Posts': posts_payload}
                    
                    print('Save Name company =',save_name)
               
        else:
            print('Individual')
            time.sleep(2)
            driver.get(input)
            user_info = linkedin.user_basic_info()

            save_name = user_info['First']+'_'+user_info['Last']
            if save_name is None:
                print('Company Not Found')
                dont_save = True
            else:
                dont_save = False
                print('Save Name =',save_name)
                full_name = user_info['full_name']
                user_info.pop('full_name')
                user_edu = linkedin.user_edu_exp()
                posts_link = input + 'recent-activity/shares/'
                driver.get(posts_link)
                #linkedin.load_posts_count()
                posts_payload = linkedin.crawl_posts()
                company = 'User Profile'
                current_date = linkedin.date_utc()
                payload = {'Name':full_name,'Date':current_date,'Profile':user_info,'Education':user_edu[0],'Expierence':user_edu[1],'User Posts': posts_payload}
        if dont_save is not True:
            with open(save_name+'.json', 'w') as fp:
                json.dump(payload, fp,  indent=4)
            print('Done')
            driver.close()
            return payload
        else:
            pass

trial = linkedin.main('https://www.linkedin.com/in/marco-pazsolano2022/',username,password)


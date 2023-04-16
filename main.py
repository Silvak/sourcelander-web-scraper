import time
import json
#import speedtest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from pynput.keyboard import Key, Controller
from selenium.webdriver.common.keys import Keys
import os


#_____________________________________________________________________________________________________
#////////////////////////////////////////// WAIT FOR ELEMENT ////////////////////////////////////////#
def WaitFor(driver, path, time=60):
            element = None
            while(element == None):
                try:
                    findElement = CustomDriver(driver, path, time)
                    findElement.click()
                    element = findElement
                except:
                    print("waiting...")

#_____________________________________________________________________________________________________
#//////////////////////////////////////// CUSTOIM DRIVER ////////////////////////////////////////////#
def CustomDriver(driver, path, time=120):
    """ 
        Configure a web driver with a timeout of 20 seconds by default.
        
        Args:
            driver (_object_): -> selenium driver
            path (_string_):  -> xpath address of the html element
            time (_float_): -> timeout
        Returns:
            _object_: WebDriverWait()
    """ 
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, path))) 


 
#"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[1]/div/div[2]/div[2]/div[1]/div/div/div/span[1]"
#"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[1]/div/div[2]/div[2]/div[1]/div/div/div/span[2]"
#"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[1]/div/div[2]/div[2]/div[1]/div/div/div/a[1]"
#"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[1]/div/div[2]/div[2]/div[1]/div/div/div/a[2]"
#"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[1]/div/div[2]/div[2]/div[1]/div/div/div/a[3]"
#"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[1]/div/div[2]/div[2]/div[1]/div/div/div/a[4]"
#"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[1]/div/div[2]/div[2]/div[1]/div/div/div/a[5]"
   

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
def Main ():
    driver = Setup()
    
    dir = 'data'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    user = GetUser(driver)
    #print(user)
    
    #with open('data//data.json', 'w') as file:
    #    json.dump(user, file, indent=4)
    
    return print("Main execute")


def map(driver, target1, target2 ):
    listItems = []
    elements = driver.find_elements(By.CLASS_NAME, target1)
    
    for element in elements:
        item = element.find_elements(By.TAG_NAME, target2)
        for x in item:
            listItems.append(x)  
    return listItems  


def mapText(driver, target1, target2 ):
    listItems = []
    elements = driver.find_elements(By.CLASS_NAME, target1)
    
    for element in elements:
        item = element.find_elements(By.TAG_NAME, target2)
        for x in item:
            listItems.append(x.text)  
    return listItems  


def mapImg(driver, target1, target2 ):
    listItems = []
    elements = driver.find_elements(By.CLASS_NAME, target1)
    
    for element in elements:
        item = element.find_elements(By.TAG_NAME, target2)
        for x in item:
            listItems.append(x.get_attribute('src'))       
    return listItems  


#_____________________________________________________________________________________________________
#////////////////////////////////////////////// SETUP //////////////////////////////////////////////#
def GetUser(driver):
    errorPages = []    
    data = {}
    
    for pg in range(141, 301):
        print(f'>>>>>>>>>>>>> Bucle {pg} <<<<<<<<<<<<')  
        driver.get(f"https://www.guru.com/d/freelancers/pg/{pg}/")    
        
        itemId = 0
        dataList = []
            
        for i in range(1, 21):
            try:
                itemId += 1
                print(f">>>>>>>>>>>>>>>>>>>>{i}<<<<<<<<<<<<<<<<<<<<<")
                element = CustomDriver( driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]")

                #Usuario Dev
                name = mapText(element, "freelancerAvatar__screenName", "a") #["name"]
                metadata = mapText(element, "freelancerAvatar__meta", "span") #['Rutland, Massachusetts, United States', 'Rutland,', 'Massachusetts,', 'United States', '1,134,918\n/yr', '1,134,918', '/yr', '·', '100%']
                avatar = mapImg(element, "avatar", "img") #["url"]

                ##Description Dev
                mainImage = mapImg(element, "serviceListing__cover", "img")
                title =  mapText(element, "serviceListing__title", "a") #["title"]
                description = mapText(element, "serviceListing__details", "p")
                skills = mapText(element, "skillsList", "a")


                user = {
                    "name": name[0],
                    "metadata": metadata,
                    "avatar": avatar[0],

                    "description": {
                        "mainImg": mainImage[0],  
                        "title": title[0],
                        "description": description,
                        "skills": skills
                    }
                }

                #Get services                    
                CustomDriver(driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]/div[2]/div[2]/nav/button[1]").click()
                time.sleep(0.3)

                services = [] #<<<<<<<<<< arr services
                servicesList = map(element, "module_list", "li")
                for x in servicesList:
                    image_services = mapImg(x, "serviceListing__cover", "img")
                    title_services = mapText(x, "serviceListing__title", "a") #["title"]
                    description_services = mapText(x, "serviceListing__details", "p") #["rate", "desc"]
                    skills_services = mapText(x, "skillsList", "a") #["skill", ...]

                    services.append({
                        "title": title_services[0],
                        "description": description_services,
                        "skills": skills_services,
                        "image": image_services[0]
                    })     
                CustomDriver(driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]/div[2]/div[2]/nav/button[1]").click()


                #Get porfolio 
                CustomDriver(driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]/div[2]/div[2]/nav/button[2]").click()         
                time.sleep(0.3)
                porfolio = [] #<<<<<<<<<< porfolio
                porfolioList = map(element, "portfolioGrid", "div")
                for x in porfolioList:
                    porfolioTitle = x.find_elements(By.CLASS_NAME, "portfolio__title")
                    porfolioImg = mapImg(x, "portfolio__wrapper", "img" )
                    porfolio.append({"title": porfolioTitle[0].text, "image": porfolioImg[0]})
                CustomDriver(driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]/div[2]/div[2]/nav/button[2]").click()         


                #Get Performance      
                CustomDriver(driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]/div[2]/div[2]/nav/button[3]").click()
                time.sleep(0.3)

                feedback = []
                performance = [] #<<<<<<<<<< arr performance

                statsList = mapText(element, "feedback__stats", "li")
                feedbackList = map(element, "module_list", "li")
                for x in feedbackList:
                    avatar_p = mapImg(x, "avatar", "img")
                    comment_p = mapText(x, "avatarinfo", "p")

                    feedback.append({
                        "avatar": avatar_p[0],
                        "commnet": comment_p
                    })
                performance.append({"stats": statsList, "feedback": feedback})        
                CustomDriver(driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]/div[2]/div[2]/nav/button[3]").click()


                #GET ABOUT          
                CustomDriver(driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]/div[2]/div[2]/nav/button[4]").click()
                time.sleep(0.3)

                about = []

                aboutList = map(element, "profile-about", "div")
                bio_a = mapText(element, "rhythmMargin2", "pre")

                for x in aboutList:
                    avatar_a = mapImg(x, "avatar", "img") # avatar_a[0]
                    abstract_a = mapText(x, "avatarinfo", "p") # abstract_a[0]
                    #text_a = mapText(x, "profile-about", "p")
                    about.append({ 
                        "avatar": avatar_a,
                        "abstrac": abstract_a,
                        "bio": bio_a           
                    })


                try: 
                    aboutFirstItem = about[0]
                except:
                    aboutFirstItem = about


                CustomDriver(driver, f"/html/body/form/main/main/div/section[1]/div/div[2]/div[1]/ul/li[{i}]/div/div[2]/div[2]/div[2]/nav/button[4]").click()

                ##
                dataList.append({
                    "id": itemId,
                    "user": user,
                    "services": services,
                    "porfolio": porfolio,
                    "performance": performance,
                    "about": aboutFirstItem
                })
                #print(dataList)
                
                
                dictionary = {
                    "list": dataList
                }
                #data['wallet'].append(dataList)
                with open(f"data/page{pg}.json", "w") as outfile:
                    json.dump(dictionary, outfile)

            except:
                errorPages.append(pg)
                print(f"error get data, errorList:  {errorPages} \n")
                continue
        
        time.sleep(2)
        dictionaryError = {
            "errorPages": errorPages
        }
        #data['wallet'].append(dataList)
        with open(f"data/errorPages.json", "w") as outfile:
            json.dump(dictionaryError, outfile)
    return 


#_____________________________________________________________________________________________________
#////////////////////////////////////////////// SETUP //////////////////////////////////////////////#
def Setup():
 
    #config driver
    options = Options() 
    options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    service = Service('webdriver//chromedriver.exe')   
    driver = webdriver.Chrome(service=service)
    
    driver.get("https://www.guru.com/d/freelancers/pg/1/")
    time.sleep(2)
    CustomDriver(driver, "/html/body/div/div[2]/div/div[1]/div/div[2]/div/button[3]").click()
    return driver


#_____________________________________________________________________________________________________
#////////////////////////////////////////// IMPORT DATA /////////////////////////////////////////////#
def Import_data(namefile):
    """ 
        Import json file with all data.
          
        Args:
            namefile (_string_): -> json file name
        Returns:
            _object_: data
    """
    with open(f'data//{namefile}.json') as file:
        data = json.load(file)
    print("[Import_data] executed.")
    return data



Main()

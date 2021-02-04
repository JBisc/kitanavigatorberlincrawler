import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# define how many pages to want to read
pages = 25

# go on kita navigator with your browser and start a search with your prefered setting
baseURL = "https://kita-navigator.berlin.de/einrichtungen?input=Pfalzburger%20Str.%2080%2C%2010719%20Berlin%2C%20Germany&betb=1-2021&einfacheSuche=true&entfernung=3&lat=52.4982814&lon=13.3229621"\

kitasNumbers = []
kitasNames = []

for page in range(pages):
    URL = baseURL +"&seite=" + str(page) + "&index=0"
    # start webdriver
    driver = webdriver.Firefox()
    driver.get(URL)
    #not sure if necessary
    wait = WebDriverWait(driver, 2)


    matchesNumber = re.findall(r'einrichtungen/\d*\d', driver.page_source)
    driver.close()
    for matchNumber in matchesNumber:
        matchNumberCutted = re.search(r'\d*\d', matchNumber)

        if matchNumberCutted:
            kitasNumbers.append(matchNumberCutted.group())
            #print("Found",matchNumberCutted.group())
            print("Kitas", matchNumberCutted.group())

kitasNumbers = list(dict.fromkeys(kitasNumbers))
print("Kitas", kitasNumbers)

matchesMail = []
for kitaNumbers in kitasNumbers:
    URL = 'https://kita-navigator.berlin.de/einrichtungen/'
    #print(URL+match)
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 2)

    driver.get(URL+kitaNumbers)
    #search for the email adress
    matchMail = re.search(r'[\w\.-]+@[\w\.-]+', driver.page_source)
    f = open("results.txt", "a")

    if matchMail:
        print(matchMail.group(1))
        f.write(matchMail.group()+';')
    else:
        f.write(';')
        print('something went wrong with foinding an Email adress')

    # find names
    matchNames = re.search(r'<h1 class=\"kita-name mb-0 align-self-center\">(.*)</h1>', driver.page_source)
    if matchNames:
        print(matchNames.group(1))
        f.write(matchNames.group(1)+';'+'\n')

    else:
        f.write(';' + '\n')
        print('something went wrong ')

    f.close()
    print('results printed in results.txt. Import it with Excel.')

    driver.close()

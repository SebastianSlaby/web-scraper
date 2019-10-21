from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as Soup
import re
import json
import smtplib
from email.mime.text import MIMEText

url = 'https://cos.po.opole.pl/index.php/organizacja-roku/zaj-odw-weaii'
uClient = ureq(url)
html = uClient.read()
uClient.close()
html_soup=Soup(html, "html.parser")
containers = html_soup.findAll("div", {"class": "leading-1"})
indexes = []
phrase = "computer"
for it, container in enumerate(containers):
    string = containers[it].text.lower()
    index = string.find(phrase)
    if index != -1:
        indexes.append(it)


def get_info(containers, indexes):
    results = []
    for it in indexes:
        text = containers[it].text
        occurrences = [m.start() for m in re.finditer('\n', text)]
        date = text[occurrences[11]:occurrences[12]]
        date=date.replace('|', '')
        date = date.strip()
        name = text[occurrences[1]:occurrences[3]]
        name = name.replace('\n','')
        content = text[occurrences[12]:]
        content = content.strip()
        results.append([name, date, content])
    return results


def write_to_file(contents):
    file = open('previous.txt', 'w')
    json.dump(contents, file)
    file.close()


def check_for_new(contents):
    file = open('previous.txt', 'a')
    file.close();
    file = open('previous.txt', 'r')
    file_contents = json.load(file)
    file.close()
    new_info = []
    if file_contents == contents:
        print("Nothing to do")
    else:
        print("New info")
        sizediff = len(contents) - len(file_contents)
        message = 'Nowe zastępstwo dla naszego kierunku\n\n'
        for it in range(0, sizediff):
            new_info.append(contents[it])
            message += str(contents[it][0])
            message +='\n'
            message += str(contents[it][1])
            message +='\n'
            message += str(contents[it][2])
        #write_to_file(filtered_containers)
        sendmail(message)

def sendmail(message):
    gmail_user = 'mail@gmail.com'
    gmail_pass = 'password'
    sent_from = gmail_user
    to = ['mail@mail.com']
    email_text = MIMEText(message.encode('utf-8'), _charset='utf-8')
    email_text['Subject'] = 'Zastępstwo'
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.set_debuglevel(15)
        server.ehlo()
        server.login(gmail_user, gmail_pass)
        server.sendmail(sent_from, to, email_text.as_string())
        server.close()

        print
        'Email sent!'
    except:
        print('Something went wrong...')




filtered_containers = get_info(containers, indexes)
#write_to_file(filtered_containers) #HAS TO BE RUN ONCE, UNCOMMENT THIS LINE WHEN FIRST RUNNING THIS SCRIPT
check_for_new(filtered_containers)

import requests
import json
from bs4 import BeautifulSoup
import csv

cookies_issueTable = {
    'jira.editor.user.mode': 'wysiwyg',
    'AJS.conglomerate.cookie': '|hipchat.inapp.links.first.clicked.Smit.Patel@fxnetworks.com=false',
    'JSESSIONID': '1A1D0DB08E037F0DDC105AD57586447F',
    'wit-announce-bnr': 'e4905f76-6e43-40cc-92cd-ed5ded62b416-1538627972488-anon',
    'atlassian.xsrf.token': 'B1Q0-LWZP-03X5-1IZG_83e1c9cdcfbf8d15113fbffd089cedcc9f49dfd3_lin',
}
cookies_ticket = {
    'wit-announce-bnr': 'e4905f76-6e43-40cc-92cd-ed5ded62b416-1538627972488-5db9242c29c57070cf522cc824097f52',
    'jira.editor.user.mode': 'wysiwyg',
    'AJS.conglomerate.cookie': '|hipchat.inapp.links.first.clicked.Smit.Patel@fxnetworks.com=false',
    'JSESSIONID': '1A1D0DB08E037F0DDC105AD57586447F',
    'atlassian.xsrf.token': 'B1Q0-LWZP-03X5-1IZG_83e1c9cdcfbf8d15113fbffd089cedcc9f49dfd3_lin',
}


def read_csv(file):
    fixes = []
    with open('downloads/'+file, mode='r') as infile:
        csv_reader = csv.reader(infile, delimiter=',')
        for row in csv_reader:
            fixes.append(row)
    return fixes


def write_csv(bugs):
    try:
        with open('downloads/bug.csv', 'a') as out_file:
            w = csv.DictWriter(out_file, delimiter=',', fieldnames=["Ticket_Number", "Bug"])
            w.writerow(bugs)
    except:
        print("Problem in writing CSV")


def get_issues():
    # import requests
    global cookies_issueTable
    cookies = cookies_issueTable

    headers = {
        'X-Atlassian-Token': 'no-check',
        'Origin': 'https://fng-jira.fox.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'https://fng-jira.fox.com/issues/?jql=project%20%3D%20%22FBC%20-%20FOX%20API%22%20AND%20type%20%3D%20Bug%20AND%20status%20%3D%20Closed%20AND%20(NOT%20attachments%20is%20EMPTY%20OR%20Summary%20~%20charles)',
        '__amdModuleName': 'jira/issue/utils/xsrf-token-header',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = {
        'startIndex': '0',
        'jql': 'project = "FBC - FOX API" AND type = Bug AND status = Closed AND (NOT attachments is EMPTY OR Summary ~ charles)',
        'layoutKey': 'split-view'
    }

    response = requests.post('https://fng-jira.fox.com/rest/issueNav/1/issueTable', headers=headers, cookies=cookies,
                             data=data)

    return response.text


def parse():
    fixes = read_csv("fixes.csv")
    parsed_tickets = read_csv("bug.csv")
    parsed_tickets = [x[0] for x in parsed_tickets] # to get ticket numbers already parsed
    # print([x[0] for x in parsed_tickets])
    bugs = {}
    try:
        issue_json = json.loads(get_issues())
        issues = list(set(issue_json["issueTable"]["issueKeys"]) - set(parsed_tickets))
        # print(len(issue_json["issueTable"]["issueKeys"]))
        for i in issues:
            log_link_parse(i)
            # print(i)
            if i in fixes:
                bugs["Ticket_Number"] = i
                bugs["Bug"] = "Yes"
            else:
                bugs["Ticket_Number"] = i
                bugs["Bug"] = "No"
            write_csv(bugs)
    except ValueError:
        print("File content empty, check cookie!")


def log_link_parse(ticket):
    global cookies_ticket
    cookies = cookies_ticket

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://fox.okta.com/app/jira_onprem/exk17lwpf4yQGEMxk1d8/sso/saml/3.0.667?useRedirects=true&RelayState=https%3A%2F%2Ffng-jira.fox.com%2Fbrowse%2FFOXAPI-5121',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get('https://fng-jira.fox.com/browse/' + ticket, headers=headers, cookies=cookies)
    # print(response.text)  # HTML
    soup = BeautifulSoup(response.text, features="html.parser")
    links = soup.find_all('a')
    drive_ids = []
    for tag in links:
        link = tag.get('href', "")
        if "drive.google" in link:
            index_1 = link.index("1")
            # print(ticket, link[index_1:index_1+33])
            id = link[index_1:index_1+33]
            drive_ids.append(id)  # link ids in 1 ticket

    for id in drive_ids:
        download_file_from_google_drive(id, "downloads/"+ticket+".chls")
        break


# Download files from google drive
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 5

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


parse()


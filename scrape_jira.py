import requests
import json
from bs4 import BeautifulSoup


def get_issues():
    # import requests

    cookies = {
        'AJS.conglomerate.cookie': '|hipchat.inapp.links.first.clicked.Smit.Patel@fxnetworks.com=false',
        'jira.editor.user.mode': 'wysiwyg',
        'JSESSIONID': '1D9FAA5438CC321C15B9FE4EBEB10C3A',
        'atlassian.xsrf.token': 'B1Q0-LWZP-03X5-1IZG_da4dd52cbed4c070e70bd09bbd13c3a8ab56891a_lin',
    }

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
    try:
        issue_json = json.loads(get_issues())
        for i in issue_json["issueTable"]["issueKeys"]:
            get_log_link(i)
    except ValueError:
        print("File content empty, check cookie!")


def get_log_link(ticket):

    cookies = {
        'wit-announce-bnr': 'e4905f76-6e43-40cc-92cd-ed5ded62b416-1538627972488-5db9242c29c57070cf522cc824097f52',
        'AJS.conglomerate.cookie': '|hipchat.inapp.links.first.clicked.Smit.Patel@fxnetworks.com=false',
        'jira.editor.user.mode': 'wysiwyg',
        'JSESSIONID': '1D9FAA5438CC321C15B9FE4EBEB10C3A',
        'atlassian.xsrf.token': 'B1Q0-LWZP-03X5-1IZG_da4dd52cbed4c070e70bd09bbd13c3a8ab56891a_lin',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
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
            print(link[index_1:index_1+33])
            id = link[index_1:index_1+33]
            drive_ids.append(id)  # link ids in 1 ticket

    for id in drive_ids:
        download_file_from_google_drive(id, "downloads/"+ticket)
        break


# Download files from google drive
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


parse()

#
# 14YS7yIGpcqOXknIO0ObFzIvZ0dj1Y7nx/view?usp=sharing
# 1GFuOw_RDHhqwlQBLvPGYp8HSy0abIKsa
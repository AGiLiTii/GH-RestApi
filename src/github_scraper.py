import time
import requests
from bs4 import BeautifulSoup
import json

url = 'https://github.com/'


def test():

    dict = {
        'title': 'test'
    }
    return dict


#Type
def get_type(soup):
    if (soup.find('meta', {'name':"hovercard-subject-tag"})):
        type = 'Organization'
    else:
        type = 'User'
    return type


#name
def get_name(soup,isUser):
    if(isUser):
        return soup.find('span', {'class': 'p-name vcard-fullname d-block overflow-hidden'}).text.strip()
    else:
        return soup.find('h1',class_="h2 lh-condensed").text.strip()

#bio
def get_bio(soup,isUser):
    if(isUser):
        if(soup.find('div', {'class': 'p-note user-profile-bio mb-3 js-user-profile-bio f4'})):
            return soup.find('div', {'class': 'p-note user-profile-bio mb-3 js-user-profile-bio f4'}).text.strip()
        else:
            return None
    else:
        if(soup.find('header', class_='pagehead').find('div',class_='color-fg-muted')):
            prefix = soup.find('header', class_='pagehead').find('div', class_='color-fg-muted')
            return prefix.find('div').text.strip()
        else:
            return None

#location
def get_location(soup,isUser):
    if(isUser):
        if(soup.find('span', {'class': 'p-label'})):
            return soup.find('span', {'class': 'p-label'}).text.strip()
        else:
            return None
    else:
        if(soup.find('span', {'itemprop':'location'})):
            return soup.find('span', {'itemprop':'location'}).text.strip()
        else:
            return None   

#avatar url
def get_avatar(soup):
    return soup.find("img", class_= 'avatar')['src']

#followers
def get_followers(soup,username,isUser):
    page = requests.get(url + 'search?q=' + username + "&type=users")
    print(json.loads(page.text)['payload']['results'][0])
    return json.loads(page.text)['payload']['results'][0]['followers']
        


#following
def get_following(soup,username,isUser):
    if(isUser):
        if (soup.find('a', {'href':'https://github.com/' + username + '?tab=following'})):
            prefix = soup.find('a', {'href':'https://github.com/' + username + '?tab=following'})
            return int(prefix.find('span').text.strip())
        else:
            return int(0)
    else:
        return int(0)

#company
def get_company(soup,isUser):
    if(isUser):
        if(soup.find('span', {'class': 'p-org'})):
            return soup.find('span', {'class': 'p-org'}).text.strip()
        else:
            return None
    else:
        if(soup.find('span', {'itemprop':'worksFor'})):
            return soup.find('span', {'itemprop':'worksFor'}).text.strip()
        else:
            return None

#blog
def get_blog(soup,isUser):
    if(isUser):
        if(soup.find('a', class_='Link--primary')):
            return soup.find('a', class_='Link--primary').text.strip()
        else:
            return ""
    else:
        if(soup.find('a', {'itemprop':'url'})):
            return soup.find('a', {'itemprop':'url'}).text.strip()
        else:
            return ""

#public repos
def get_public_repos(username):
    page = requests.get(url + 'search?q=' + username + "&type=users")
    return json.loads(page.text)['payload']['results'][0]['repos']

#id
def get_id(soup,isUser):
    if(isUser):
        return int(soup.find('meta', {'name': 'octolytics-dimension-user_id'})['content'])
    else:
        return int(soup.find('meta',{'name':'hovercard-subject-tag'})['content'].split(':')[1])
    
#twitter_username
def get_twitter_username(soup,isUser):
    if(isUser):
        if(soup.find('li', {'itemprop':'social'})):
            prefix = soup.find('li', {'itemprop':'social'})
            return prefix.find('a').text.split('@')[1] 
        else:
            return None
    else:
        if(soup.find('a',{'rel':'nofollow me'})):
            return soup.find('a',{'rel':'nofollow me'}).text.split('@')[1]
        else:
            return None 
        
#isUser
def bool_isUser(soup,isUser):
    if (soup.find('meta', {'name':"hovercard-subject-tag"})):
        isUser = False
    else:
        isUser = True
    return isUser


def get_userdata(username):
    response = requests.get(url + username)
    soup = BeautifulSoup(response.text, 'html.parser')

    #status code
    status_code = response.status_code
    if (status_code != 200):
        return None
    

    
    global isUser
    isUser = False

    isUser = bool_isUser(soup,isUser)

    user_data = {

        #Login
        'login': username,

        #type
        'type': get_type(soup),  

        #Name
        'name': get_name(soup,isUser),

        #Bio
        'bio': get_bio(soup,isUser),

        #Location
        'location': get_location(soup,isUser),

        #Avatar
        'avatar_url': get_avatar(soup),

        #url
        'url': 'https://api.github.com/users/' + username,

        #html url
        'html_url': url + username,

        #followers
        'followers': get_followers(soup,username,isUser),

        #following
        'following': get_following(soup,username,isUser),


        #company
        'company': get_company(soup,isUser),

        #blog
        'blog': get_blog(soup,isUser),

        #public_repos
        'public_repos': get_public_repos(username),

        #id
        'id': get_id(soup,isUser),

        #twitter_username
        'twitter_username': get_twitter_username(soup,isUser)

    }
    return user_data

#Exponential backoff
def requests_get_with_backoff(url, max_retries=10, initial_backoff=5):
    retries = 0
    backoff = initial_backoff

    while retries < max_retries:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            print("Rate limited, retrying in", backoff, "seconds...")
            time.sleep(backoff)
            backoff *= 2  # Double the backoff time for each retry
            retries += 1
        else:
            return response

    return response

#ALL repo names
def get_all_repo_name(soup):
    repo_name = []
    for repo in soup.find_all('a',itemprop='name codeRepository'):
        repo_name.append(repo.text.strip())
    return repo_name

#ID
def get_repo_id(soup):
    if(soup.find('meta',{'name':'hovercard-subject-tag'})):
        return int(soup.find('meta',{'name':'hovercard-subject-tag'})['content'].split(':')[1])
    else:
        return None

    
#Full name
def get_full_name(soup):
    if(soup.find('strong', itemprop='name')):
        return soup.find('strong', itemprop='name').text.strip()
    else:
        return None
    
#curr repo name
def get_repo_desc(soup):
        if(soup.find('p',itemprop='description')):
            return soup.find('p',itemprop='description').text.strip()
        else:
            return None
    
#Forks count
def get_forks_count(soup):
    prefix = soup.find('span',id='repo-network-counter')
    if(prefix):
        result = prefix['title'].strip().split(',')
        result = ''.join(result)
        return int(result)
    else:
        return 0
    
    
#Stars & Watchers
def get_stargazers_count(soup):
    prefix = soup.find('span',id='repo-stars-counter-star')
    if(prefix):
        result = prefix['title'].strip().split(',')
        result = ''.join(result)
        return int(result)
    else:
        return 0


#Default
def get_default_branch(repo_data,username):
    # prefix = soup.find('summary',{'title':'Switch branches or tags'})
    # prefix.find('span', {'class' : 'css-truncate-target'})
    response = requests_get_with_backoff(url + username + '/' + repo_data + '/branches')
    soup = BeautifulSoup(response.text, 'html.parser')
    prefix = soup.find('clipboard-copy')
    if(prefix['value']):
        return prefix['value']
    else:
        return None
#Issues
def get_issues_count(repo_name,username):
    issues_url =  username + "/" + repo_name + "/issues?q=is%3Aopen"
    response = requests_get_with_backoff(url + issues_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cnt = soup.find('a', {'href' : '/' + issues_url}).text.strip().split(" ")[0].split(",")
    cnt = ''.join(cnt)
    return int(cnt)

#Has issues
def get_has_issues(soup,repo_name,username):
    prefix = soup.find('a',{'href':'/' + username + '/' + repo_name +'/' + 'issues'})
    if(prefix):
        return True
    else:
        return False
    
#Has projects
def get_has_projects(soup,repo_name,username):
    prefix = soup.find('a',{'href':'/' + username + '/' + repo_name +'/' + 'projects'})
    if(prefix):
        return True
    else:
        return False
    
#Archived
def get_archived(soup):
    if(soup.find('span',{'class':'Label Label--attention v-align-middle ml-1 mb-1'})):
        return True
    else:
        return False
    
#Pushed
def get_pushed_at(soup):
    prefix = soup.find('relative-time',{'class':'no-wrap'})
    if(prefix):
        return prefix['datetime']
    else:
        return None

#Language
def get_language(soup):

    prefix = soup.find('span', itemprop='programmingLanguage')
    if(prefix):
        return prefix.text
    else:
        return None

#Topics
def get_topics(soup):
    prefix = soup.find_all('a',{'class':'topic-tag topic-tag-link'})
    if(prefix):
        result = []
        for i in range(len(prefix)):
            result.append(prefix[i].text.strip())
        result = sorted(result)
        return result
    else:
        return []
    
#Owner
def get_owner(username):
    search_page = url + 'search?q=' + username + "&type=users"
    page = requests_get_with_backoff(search_page)
    owner = {
        'login': json.loads(page.text)['payload']['results'][0]['display_login'],
        'id': int(json.loads(page.text)['payload']['results'][0]['id']),
    }
    return owner

#Forked
def is_forked(soup):
    if(soup.find('span',{'class':'text-small lh-condensed-ultra no-wrap mt-1'})):
        return True
    else:
        return False
    
#Has discussions
def get_has_discussions(soup):
    if(soup.find('a',id='discussions-tab')):
        return True
    else:
        return False
    
#Homepage
def get_hommepage(soup):
    prefix = soup.find('a',{'role':'link'})
    if(prefix):
        return prefix['href']
    else:
        return None



def get_repodata(username):

    # Org or User
    response = requests_get_with_backoff(url+username)
    soup = BeautifulSoup(response.text, 'html.parser')
    isUser = False
    isUser = bool_isUser(soup,isUser)



    if(isUser):
        response = requests_get_with_backoff(url + username  + '?tab=repositories')
        #get status code
        status_code = response.status_code
        if (status_code != 200):
                return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        response = requests_get_with_backoff(url + "orgs/" + username + "/repositories")
        #get status code
        status_code = response.status_code
        if (status_code != 200):
                return None
        soup = BeautifulSoup(response.text, 'html.parser')

   
    repo_data = get_all_repo_name(soup)
    local_button = []
    owner = get_owner(username)


    #if next button exists count the next page and append to repo_data
    while(soup.find('a',{'class':'next_page'})):
        next_page = soup.find('a',{'class':'next_page'})['href']
        response = requests_get_with_backoff(url + next_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        repo_data = repo_data + get_all_repo_name(soup)

    if(isUser):
        response =  requests_get_with_backoff(url + username + '?tab=repositories')
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        response = requests_get_with_backoff(url + "orgs/" + username + "/repositories")
        soup = BeautifulSoup(response.text, 'html.parser')

    #Get repo buttons
    while(True):
        if(isUser):
            repo_buttons = soup.find_all('li',{'itemprop':'owns'})
        else:
            repo_buttons = soup.find_all('div',{'itemprop':'owns'})

        for repo_button in repo_buttons:
            local_button.append(repo_button)

        # Multiple pages
        if(soup.find('a',{'class':'next_page'})):
            next_page = soup.find('a',{'class':'next_page'})['href']
            response = requests_get_with_backoff(url + next_page)
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            break

    # add data to each repo
    for i in range(len(repo_data)):

        #Local soup
        response = requests_get_with_backoff(url + username + "/" + repo_data[i])
        local_soup = BeautifulSoup(response.text, 'html.parser')

        repo_data[i] = {
            'id': get_repo_id(local_soup),
            'full_name':username + '/' + get_full_name(local_soup),
            'name': repo_data[i],
            'owner': owner,
            'private': False,
            'url': 'https://api.github.com/repos/' + username + '/' + repo_data[i],
            'html_url': url + username + '/' + repo_data[i],
            'description': get_repo_desc(local_button[i]),
            'fork': is_forked(local_soup),
            'homepage': get_hommepage(local_soup),
            'language': get_language(local_button[i]),
            'forks_count': get_forks_count(local_soup),
            'stargazers_count': get_stargazers_count(local_soup),
            'watchers_count': get_stargazers_count(local_soup),
            'default_branch': get_default_branch(repo_data[i],username),
            'open_issues_count': get_issues_count(repo_data[i],username),
            'topics': get_topics(local_soup),
            'has_issues': get_has_issues(local_soup,repo_data[i],username),
            'has_projects': get_has_projects(local_soup,repo_data[i],username),
            'has_discussions':get_has_discussions(local_soup),
            'archived': get_archived(local_button[i]),
            'pushed_at':get_pushed_at(local_button[i]),

        }

    return repo_data

# TESTS
if (__name__ == "__main__"):
    
    # test with tommcfarlin for archived repos
    testUser = "twitter"

    print("Testing...")
    theirs = requests_get_with_backoff("https://api.github.com/users/" + testUser + "/repos").json()
    mine = get_repodata(testUser)
    fieldsToCheck = ["id", "name", "full_name", "owner", "private", "html_url", "description", "fork", "url", "homepage", "language", "forks_count", "stargazers_count", "watchers_count", "default_branch", "open_issues_count", "topics", "has_issues", "has_projects","has_discussions" ,"archived", "pushed_at"]


    for repo in theirs:

        for myrepo in mine:
            if (myrepo["name"] == repo["name"]):
                
                print("\n=== TESTING " + repo["name"] + "===\n")

                for field in fieldsToCheck:
                    
                    if (field == "owner"):
                        repo["owner"] = {
                            "login": repo["owner"]["login"],
                            "id": repo["owner"]["id"]
                        }


                    if (myrepo[field] == repo[field]):
                        print("\033[32m" + field + " PASSED")
                    else:
                        print("\033[31m" + field + " FAILED with " + str(repo[field]) + " != " + str(myrepo[field]))
 

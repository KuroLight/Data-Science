import io
import time
import json
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def retrieve_html(url):
    """
    Return the raw HTML at the specified URL.

    Args:
        url (string):

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """

    params = {
        "query": "python metaclass",
        "source": "chrome"
    }
    response = requests.get(url, params=params)

    return response.status_code, response.content.decode('utf-8')


# example
result = retrieve_html('www.google.com')
print(result)


def read_api_key(filepath):
    """
    Read the Yelp API Key from file.

    Args:
        filepath (string): File containing API Key
    Returns:
        api_key (string): The API Key
    """

    with open(filepath, 'r', encoding='utf-8') as f:
        api_key = f.read().replace('\n', '')
        print(api_key)

        return api_key


def yelp_search(api_key, query):
    """
    Make an authenticated request to the Yelp API.

    Args:
        query (string): Search term

    Returns:
        total (integer): total number of businesses on Yelp corresponding to the query
        businesses (list): list of dicts representing each business
    """

    search_url = 'https://api.yelp.com/v3/businesses/search'
    headers = {
        'Authorization': 'Bearer ' + api_key
    }
    params = {
        'location': query
    }
    rp = requests.get(url=search_url, headers=headers, params=params)
    pprint(rp.json())
    total = rp.json()['total']
    data = rp.json()['businesses']
    return total, data


api_key = read_api_key('../api_key.txt')
num_records, data = yelp_search(api_key, 'Pittsburgh')
print(num_records)
print(list(map(lambda x: x['name'], data)))


def all_restaurants(api_key, query):
    """
    Retrieve ALL the restaurants on Yelp for a given query.

    Args:
        query (string): Search term

    Returns:
        results (list): list of dicts representing each business
    """

    search_url = 'https://api.yelp.com/v3/businesses/search'
    headers = {
        'Authorization': 'Bearer ' + api_key
    }
    params = {
        'location': query,
        'limit': 20,
        'offset': 0,
        'categories': 'restaurants'  # 'restaurants, All'
    }

    rest_list = []
    offset = 0
    cnt = 0
    while True:
        params['offset'] = offset
        rp = requests.get(url=search_url, headers=headers, params=params)

        # defense: no businesses are found
        if 'businesses' not in rp.json().keys():
            break

        businesses = rp.json()['businesses']
        # names.extend(list(map(lambda x: x['name'], businesses)))
        rest_list.extend(businesses)
        if len(businesses) < 20:
            break
        offset += 20
        time.sleep(0.21)
    
    pprint(rp.json())

    return rest_list


data = all_restaurants(api_key, 'Morewood, Pittsburgh')
print(len(data))
pprint(data)


def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.

    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """

    #     url = re.compile(r'(https://www.yelp.com/biz/.*?)[?"]')
    #     m = url.findall(data)
    json_dict = json.loads(data)
    pprint(json_dict)
    if 'businesses' not in json_dict.keys():
        return []
    busi_list = []
    for busi in json_dict['businesses']:
        busi_list.append(busi['url'])
    return busi_list


with open('data2.json', 'rt', encoding='utf-8', newline='\n') as f:
    #     data = str(json.load(f))
    data = f.read()
    print(type(data))

links = parse_api_response(data)
print(len(links))
pprint(links)


def parse_page(html):
    """
    Parse the reviews on a single page of a restaurant.

    Args:
        html (string): String of HTML corresponding to a Yelp restaurant

    Returns:
        tuple(list, string): a tuple of two elements
            first element: list of dictionaries corresponding to the extracted review information
            second element: URL for the next page of reviews (or None if it is the last page)
    """


    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    list_of_dict = []
    for div in soup.find_all('div', class_='review review--with-sidebar'):
        dictt = {}
        dictt['review_id'] = div['data-review-id']
        userid = div['data-signup-object']
        m = re.search(r'user_id:(.*)', userid)
        dictt['user_id'] = m.group(1)
        #         for a in div.find_all('a', class_ = 'user-display-name js-analytics-click'):
        #             m = re.search(r'/user_details\?userid=(.*)', a['href'])
        #             dictt['user_id'] = m.group(1)
        for divv in div.find_all('div', class_='review-wrapper'):
            title = divv.find('div').find('div').find(
                'div').find('div')['title']
            m = re.search(r'([1-5].0) star rating', title)
            print(m.group(1))
            dictt['rating'] = float(m.group(1))

            date_string = divv.find('div').find('div').find('span')
            print(date_string.text)
            #             m = re.search(r'([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})', date_string.text)
            #             year, month, day = m.group(3), m.group(1), m.group(2)
            #             if int(month) < 10: month = '0' + month
            #             if int(day) < 10: day = '0' + day
            #             date = year+'/'+month+'/'+day

            m = re.search(
                r'([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})', date_string.text)

            date = m.group(1)
            dictt['date'] = date

            content = divv.find('div').find('p')
            dictt['text'] = content.text

        list_of_dict.append(dictt)
        pprint(list_of_dict)

    next_page = None
    pagination_links = soup.find('div', class_='pagination-links arrange_unit')
    found_current = False
    if pagination_links:
        baseline = pagination_links.find(
            'div', class_='arrange arrange--baseline')
        for div in baseline.find_all('div'):
            print(div['class'])
            if found_current:
                next_page = div.find(
                    'a', class_='available-number pagination-links_anchor')['href']
                break
            if len(div['class']) >= 3 and div['class'][2] == 'current':
                found_current = True
    # print('find current')

    print(next_page)
    return list_of_dict, next_page

ld, nextpage = parse_page(retrieve_html(
    'https://www.yelp.com/biz/the-porch-at-schenley-pittsburgh')[1])
pprint(ld)
print(nextpage)

def extract_reviews(url):
    """
    Retrieve ALL of the reviews for a single restaurant on Yelp.

    Parameters:
        url (string): Yelp URL corresponding to the restaurant of interest.

    Returns:
        reviews (list): list of dictionaries containing extracted review information
    """
    

    if not url:
        return None

    list_of_dict = []
    while url:
        raw_html_text = retrieve_html(url)[1]
        next_list, url = parse_page(raw_html_text)
        list_of_dict.extend(next_list)

    return list_of_dict



data = extract_reviews(
    'https://www.yelp.com/biz/the-porch-at-schenley-pittsburgh')
print(len(data))
pprint(data[0])

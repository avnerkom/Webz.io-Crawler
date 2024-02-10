import os                               # Operating system module for file and directory operations
import re                               # Regular expression operations
import time                             # Module for time-related functions
import json                             # JSON module for handling JSON data
import asyncio                          # Asynchronous I/O module for concurrent programming
import aiohttp                          # Asynchronous HTTP client/server framework
from bs4 import BeautifulSoup           # Beautiful Soup library for HTML parsing
from typing import Dict, List, Optional # Importing Dict and List types from the typing module
from urllib.parse import urlparse       # Importing urlparse function from urllib.parse module


class WebCrawler:
    def __init__(self):
        self.base_url = None
        self.stored_username = None
        self.stored_password = None
# note:  functions accept an aiohttp.ClientSession object to be used for making HTTP requests, 
#       allowing multiple requests to be made concurrently.

    async def fetch_page_content(self, session: aiohttp.ClientSession, url: str) -> str:
        """Fetches the content of a web page."""
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        async with session.get(url, headers=headers) as response:
            await asyncio.sleep(3)  # Introducing a sleep delay for rate limiting
            return await response.text()

    async def get_parsed_topics_list(self, session: aiohttp.ClientSession, url: str, html_content: str) -> Dict[str, str]:
        """Returns a list of all topics in the site - IE forum message threads."""
        topics_list = []

        def _all_topics_list():
            # Extracting information for each topic (message thread)
            for topic_wrap in topic_wraps:
                topic_info = {}

# Note: I am unsure if you need the high level topics list data as well (i only need the links) so i prepared it and it will be easy
# To Extract information if needed (IE: future proofing :-) can to be comment out / deleted for current requirements).
                # Extracting relevant information from the topic HTML elements
                topic_info['title'] = topic_wrap.find('div', class_='wpforo-topic-title').a.text.strip()
                topic_info['link'] = topic_wrap.find('div', class_='wpforo-topic-title').a['href']
                topic_info['date_time'] = topic_wrap.find('div', class_='wpforo-topic-start-info').text.strip().split(', ')[2]
                topic_info['views'] = topic_wrap.find('div', class_='wpforo-topic-stat-views').text.strip()
                topic_info['posts'] = topic_wrap.find('div', class_='wpforo-topic-stat-posts').text.strip()

                # Check if topic_participants element exists in in some topics it was not present
                topic_participants_element = topic_wrap.find('div', class_='wpf-sbd-count')
                if topic_participants_element:
                    topic_info['participants'] = topic_participants_element.text.strip()
                else:
                    topic_info['participants'] = "No participants"

                topics_list.append(topic_info)

        soup = BeautifulSoup(html_content, 'html.parser')
        is_pagination = soup.find(class_="wpf-page-info")

        if is_pagination is None:
            print('Topic List No pagination - single page')
            _all_topics_list()
        else:
            # If there are multiple pages, handle pagination
            is_pagination_element = soup.find(class_="wpf-page-info")
            is_pagination = getattr(is_pagination_element, 'text', 'Unknown').strip().split(' / ')[1]

            async with asyncio.Semaphore(2):
                tasks = []
                for i in range(int(is_pagination)):
                    print('Grading list of topics', str(int(i)+1) + '/' + str(is_pagination) + ' Pages')
                    page_url = url + '/paged/' + str(int(i+1))
                    tasks.append(self.fetch_page_content(session, page_url))

                page_contents = await asyncio.gather(*tasks) #I've used asyncio.gather() to execute concurrently

                for content in page_contents:
                    soup = BeautifulSoup(content, 'html.parser')
                    topic_wraps = soup.find_all('div', class_='topic-wrap')
                    _all_topics_list()

        print('DONE, Total:', len(topics_list), 'Topics Found!\n')
        return topics_list, str(len(topics_list))

    async def get_forum_topic_content(self, session: aiohttp.ClientSession, url: str, html_content: str) -> List[Dict[str, str]]:
        """Extracts information from forum topics."""
        async def get_all_forum_topics(url: str, html_content: str = None):
            soup = BeautifulSoup(html_content, 'html.parser')

            forum_topics = soup.find_all(class_='wpforo-post')
            extracted_info_list = []

            for topic in forum_topics:
                try:
                    # Extracting information for each topic
                    author_name_element = topic.find(class_='author-name').a
                    author_name = author_name_element.text.strip() if author_name_element else 'Unknown'

                    author_profile_link_element = topic.find(class_='author-name').a
                    author_profile_link = author_profile_link_element['href'] if author_profile_link_element else 'Unknown'

                    author_nicename_element = topic.find(class_='wpf-author-nicename')
                    author_nicename = author_nicename_element.text.strip() if author_nicename_element else 'Unknown'

                    author_posts_element = topic.find(class_='author-posts')
                    author_posts = author_posts_element.text.strip().split(': ')[1] if author_posts_element else 'Unknown'

                    author_title_element = topic.find(class_='author-title')
                    author_title = author_title_element.text.strip() if author_title_element else 'Unknown'

                    wpf_member_title_element = topic.find(class_='wpf-member-title')
                    wpf_member_title = wpf_member_title_element.text.strip() if wpf_member_title_element else 'Unknown'

                    gamipress_wpforo_points_type_element = topic.find(class_='gamipress-wpforo-points-type')
                    gamipress_wpforo_points_type = gamipress_wpforo_points_type_element.text.strip() if gamipress_wpforo_points_type_element else 'Unknown'

                    wpforo_post_content_element = topic.find(class_='wpforo-post-content')
                    wpforo_post_content = wpforo_post_content_element.text.strip() if wpforo_post_content_element else 'Unknown'

                    published_time_element = topic.find(class_='cbleft')
                    published_time = published_time_element.text.strip().split(': ')[1] if wpforo_post_content_element else 'Unknown'

                    # Create a dictionary for the extracted information of this topic
                    extracted_info = {
                        "author_name": author_name,
                        "author_nicename": author_nicename,
                        "author_profile_link": author_profile_link,
                        "published_time": published_time,
                        "author_posts": author_posts,
                        "author_title": author_title,
                        "wpf_member_title": wpf_member_title,
                        "gamipress_points_type": gamipress_wpforo_points_type,
                        "page_link": url,
                        "post_content": wpforo_post_content
                    }

                    extracted_info_list.append(extracted_info)

                except AttributeError:
                    pass
            extracted_info_list = self.remove_special_characters(extracted_info_list)
            return extracted_info_list

        soup = BeautifulSoup(html_content, 'html.parser')
        extracted_info_list = []
        is_pagination = soup.find(class_="wpf-page-info")

        if is_pagination is None:
            print('NO pagination - single page')
            extracted_info_list = await get_all_forum_topics(url, html_content)
        else:
            is_pagination_element = soup.find(class_="wpf-page-info")
            is_pagination = getattr(is_pagination_element, 'text', 'Unknown').strip().split(' / ')[1]

            async with asyncio.Semaphore(2):
                tasks = []
                for i in range(int(is_pagination)):
                    if i == 1:
                        print('     --page_url--', url, '|| PAGE', str(i+1) + '/' + is_pagination)
                        tasks.append(get_all_forum_topics(url, html_content))
                        print('PAGE', str(i+1) + '/' + is_pagination + ' DONE')
                    else:
                        page_url = url + '/paged/' + str(int(i+1))
                        print('     --page_url--', page_url, '|| PAGE', str(i+1) + '/' + is_pagination)
                        page_html_content = await self.fetch_page_content(session, page_url)
                        tasks.append(get_all_forum_topics(url, page_html_content))

                extracted_info_list = await asyncio.gather(*tasks)
        return extracted_info_list

    def remove_special_characters(self, extracted_info_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
            
        """
        Removes special characters and symbols from the values in a list of dictionaries.

        Args:
        - extracted_info_list: List of dictionaries containing information.

        Returns:
        - List of dictionaries with special characters and symbols removed from the values.
        """
        for info in extracted_info_list:
            for key, value in info.items():
                if isinstance(value, str):
                    info[key] = re.sub(r'[^\w\s]', '', value)
        return extracted_info_list

    async def save_post_to_file(self, url: str, data: Dict[str, str], filename_prefix: str) -> None:
        """Saves post data to a JSON file."""
        filename = f'data/{filename_prefix}_{url.split("/")[-1]}.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return filename

    async def login_he_man(self, url: str, username: str, password: str) -> None:

        """Logs in to the forum."""
        login_url = self.get_domain_and_protocol_from_url(url) + '/wp-login.php'

        async with aiohttp.ClientSession() as session:
            payload: dict = {
                'log': username,
                'pwd': password,
                'wp-submit': 'Log In',
                'redirect_to': self.get_domain_and_protocol_from_url(url),
                'testcookie': '1'
            }

            async with session.post(login_url, data=payload) as response:
                if response.status == 200:
                    print('Login successful!')
                else:
                    print('Login failed. Status code:', response.status)
                    print('\nFULL response:', response)

    def get_domain_and_protocol_from_url(self, url: str) -> str:        
        """Extracts  from a given URL string."""
        parsed_url = urlparse(url)
        domain = parsed_url.scheme + '://' + parsed_url.netloc
        return domain

    async def crawl_forum(self, username: Optional[str] = None, password: Optional[str] = None) -> None:

        """Crawls the forum and saves posts to JSON files."""
        os.makedirs('data', exist_ok=True)
        
        # Get URL and user/password credentials from config or CLI
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        self.base_url = config.get('url')
        self.stored_username = config.get('username')
        self.stored_password = config.get('password')

        final_username = username if username else self.stored_username
        final_password = password if password else self.stored_password

        async with aiohttp.ClientSession() as session:
            await self.login_he_man(self.base_url, final_username, final_password)
            page_content = await self.fetch_page_content(session, self.base_url)
            topics_list, total_topics = await self.get_parsed_topics_list(session, self.base_url, page_content)

            for index, topic in enumerate(topics_list):
                print('\n' + str(index+1) + '/' + total_topics, " - Working On Link:", topic['link'])
                topic_content = await self.fetch_page_content(session, topic['link'])
                cur_topic_content = await self.get_forum_topic_content(session, topic['link'], topic_content)
                print('Extracting ' + str(len(cur_topic_content)) + ' items for topic')

                current_epoch_time = str(int(time.time()))
                filename = await self.save_post_to_file(topic['link'], cur_topic_content, f'Webz.io-{current_epoch_time}')
                if filename:
                    print('The file "./' + filename + '" successfully saved')
                else:
                    print('ERROR! The file "./' + filename + '" was NOT saved')

        print('\n-=≡All Done≡=-\n')


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == "crawl_forum":
        asyncio.run(WebCrawler().crawl_forum())
    else:
        print("""
    Webz.io Crawler

    This script crawls a forum and saves posts to JSON files.

    Usage:
        To crawl the forum and save posts to JSON files:
        $ python crawler.py crawl_forum [--username USERNAME] [--password PASSWORD] (both optional)

    The configuration can also be provided via a config file named config.json.
    
    Additionally, you can use '--help' to display this help message.
        """)

Webz.io Crawler (Job Interview Task)
it's important to note that this was done specifically for the "https://foreternia.com/community/announcement-forum" forum but it can be easily adjusted and extended for other similar forums.
The Webz.io Crawler is a small Python script designed as a job interview task for Webz.io to crawl a forum, extract post data, and save it to JSON files. It utilizes asynchronous I/O operations for concurrent programming and relies on the aiohttp library for asynchronous HTTP client/server interactions.


Features
Asynchronous Processing: The crawler leverages asyncio and aiohttp to perform concurrent HTTP requests, enabling efficient crawling of web pages.
Data Extraction: It extracts information from forum topics, including author names, post content, publication times, and other relevant details.
JSON File Output: The extracted post data is saved to JSON files, allowing for easy storage and analysis.
Concurrent Connections: The crawler supports concurrency with up to 2 connections at the same time, enhancing performance during crawling.
Rate Limiting: To prevent blocking and ensure smooth crawling, the crawler pauses for 3 seconds between each document retrieval. Additionally, it employs a user-agent header for HTTP requests.
Usage
Installation: Ensure that you have Python installed on your system along with the required libraries specified in the requirements.txt file. You can install the required libraries using the following command:

$ pip install -r requirements.txt
Configuration: The crawler supports configuration via a config.json file located in the root directory. This file should contain the following parameters:

url: The URL of the forum to be crawled.
username: (Optional) The username for forum authentication.
password: (Optional) The password for forum authentication.
Running the Crawler:

$ python crawler.py crawl_forum [--username USERNAME] [--password PASSWORD]
--username: Optional. Specify the username for forum authentication.
--password: Optional. Specify the password for forum authentication.
Output: The crawler saves the extracted post data to JSON files in the ./data/ directory. Each unique thread is identified by a filename prefix.

Additional Information
Login Support: The crawler supports forum login functionality to access restricted content.
Config File: Configuration details can be provided via a config.json file or through command-line arguments.
Concurrency: The crawler utilizes concurrent connections to optimize performance during crawling.
Rate Limiting: To prevent IP blocking, the crawler pauses for 3 seconds between each document retrieval and uses a user-agent header.
CLI Usage: The --help option provides detailed information on command-line usage, including available options and arguments.
Feel free to customize the README further based on your specific requirements and usage instructions.


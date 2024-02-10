# Webz.io Crawler (Job Interview Task)

The Webz.io Crawler is a Python script designed as a job interview task for Webz.io. It crawls a forum, extracts post data, and saves it to JSON files. Although specifically developed for the "https://foreternia.com/community/announcement-forum" forum, it can be easily adjusted and extended for other similar forums. The crawler employs asynchronous I/O operations for concurrent programming and utilizes the aiohttp library for asynchronous HTTP client/server interactions.

## Features

- **Asynchronous Processing:** Leveraging asyncio and aiohttp, the crawler performs concurrent HTTP requests for efficient crawling of web pages.
- **Data Extraction:** Extracts information from forum topics, including author names, post content, publication times, and other relevant details.
- **JSON File Output:** The extracted post data is saved to JSON files, facilitating easy storage and analysis.
- **Concurrent Connections:** Supports concurrency with up to 2 connections simultaneously, enhancing performance during crawling.
- **Rate Limiting:** Prevents blocking by pausing for 3 seconds between each document retrieval. Additionally, it employs a user-agent header for HTTP requests.

## Usage

### Installation

Ensure Python is installed on your system along with the required libraries specified in the requirements.txt file. Install the required libraries using:

```
$ pip install -r requirements.txt
```

### Configuration

The crawler supports configuration via a config.json file located in the root directory. Parameters include:
- `url`: URL of the forum to be crawled.
- `username`: (Optional) Username for forum authentication.
- `password`: (Optional) Password for forum authentication.

### Running the Crawler

```
$ python crawler.py crawl_forum [--username USERNAME] [--password PASSWORD]
```

- `--username`: (Optional) Specify the username for forum authentication.
- `--password`: (Optional) Specify the password for forum authentication.

### Output

The crawler saves the extracted post data to JSON files in the `./data/` directory. Each unique thread is identified by a filename prefix.

## Additional Information

- **Login Support:** The crawler supports forum login functionality to access restricted content.
- **Config File:** Configuration details can be provided via a config.json file or through command-line arguments.
- **Concurrency:** Utilizes concurrent connections to optimize performance during crawling.
- **Rate Limiting:** To prevent IP blocking, the crawler pauses for 3 seconds between each document retrieval and uses a user-agent header.
- **CLI Usage:** The `--help` option provides detailed information on command-line usage, including available options and arguments.

Feel free to customize the README further based on your specific requirements and usage instructions.

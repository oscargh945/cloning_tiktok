# TikTok Web Scraping to Amazon S3 Script

This Python script allows you to perform web scraping on TikTok to retrieve data related to a specific category or
specific users. The script then sends the data to an Amazon S3 bucket for storage. The script is called mined.py and can
be used with different arguments according to your needs.

## Requirements

Make sure you have the following installed before running the script:

Python 3.x: The programming language used to write the script.
Python Libraries: tiktok-scraper, boto3.
Amazon S3 Credentials: You will need the appropriate access credentials and configuration to connect to Amazon S3 and
send the data.

```
    python mined.py --category Crypto Deportes
```

## The available arguments are:

* ```--category ```: Specify the TikTok category from which you want to retrieve the data. You can choose "Crypto", "
  sports", or other available categories.


* ```--user``` (optional): Allows you to specify a list of TikTok users from whom you want to retrieve the data.

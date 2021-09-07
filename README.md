# Semi-generic Python Web Crawler

## What & Why
### What
This is a semi-generic (some day fully generic, hopefully) web crawler that can be used to crawl any website, given a base url, and three regexes. 
The regexes:
- One for the pages you want to store
- One for the pages you want to crawl
- One that combines the two.

The latter will be created automatically in a future update.

### Why
Coding excersise. 


## How to use
Run `python async_crawler.py` from the project's/script's root directory. It will then crawl all categories from `https://oda.com/`, and store
all products found in a local file `products.txt`. 


## Upcoming features
See [all issues labeled `enhancement`](https://github.com/pdmthorsrud/web_crawler/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) for potentially new features. Leave a thumbs up on the request if it is of interest to you.
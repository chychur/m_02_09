# Scrapy


We will use the [Scrapy](https://scrapy.org/) framework for scraping the site [quotes.toscrape.com](http://quotes.toscrape.com). The result will be two files:
- `qoutes.json` - which contains all information about quotes from all pages of the site;
- `authors.json` - which contains information about all the authors of the specified citations.
Examples of `json` files:

Data from `json` files ware loaded to the cloud Mongo DB. A database consist of two collections:

A database consist of two collections:
- Author
```commandline
{
  "_id": {
    "$oid": "64e8e68bc512f8bf3920dff7"
  },
  "full_name": "Albert Einstein",
  "born_date": "March 14, 1879",
  "born_location": "in Ulm, Germany",
  "description": "In 1879, Albert Einstein was born in Ulm, Germany...
}
```

- Quote
```commandline
{
  "_id": {
    "$oid": "64e8e68bc512f8bf3920dff9"
  },
  "tags": [
    "change",
    "deep-thoughts",
    "thinking",
    "world"
  ],
  "author": {
    "$oid": "64e8e68bc512f8bf3920dff7"
  },
  "quote": "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”"
}
```

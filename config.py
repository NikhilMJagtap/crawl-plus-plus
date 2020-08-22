CrawlerConfig = {

}

DownloadBalancerConfig = {
    "BALANCERS": [
        {
            "HOST": "localhost",
            "PORT": 8000
        },
        {
            "HOST": "localhost",
            "PORT": 8001
        }
    ],
    "DOWNLOADER_INIT_COUNT": 3,
    "DOWNLOADER_MAX_COUNT": 10,
    "DOWNLOADER_UTIL_COUNT": 100,
    "DOWNLOADER_UTIL_THRESH": 80, 
}

ParserConfig = {

}

DBConfig = {
    
}
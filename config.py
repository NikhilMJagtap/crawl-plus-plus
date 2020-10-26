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

Election = {
    "election_frequency" : 60
    "election_timeout" : 5
    "election_success_timeout" : 5
}

ParserConfig = {

}

DBConfig = {
    
}
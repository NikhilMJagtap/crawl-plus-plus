class Endpoint:
    def __init__(self, url, params={}, data={}, headers={}, cookies={}):
        self.url = url
        if type(params) != dict:
            raise AttributeError(f"params should be a dict, found {type(params)}")
        self.query_params = params
        if type(data) != dict:
            raise AttributeError(f"data should be a dict, found {type(data)}")
        self.data = data
        if type(headers) != dict:
            raise AttributeError(f"data should be a dict, found {type(headers)}")
        self.headers = headers
        if type(cookies) != dict:
            raise AttributeError(f"cookies should be a dict, found {type(cookies)}")
        self.cookies = cookies

    def set_cookies(self, cookies):
        self.cookies = cookies

    def set_params(self, key, value):
        self.query_params[key] = value

    def set_headers(self, headers):
        self.headers = headers

    def get_full_url(self):
        url = self.url
        url += "?"
        for query, value in self.query_params.items():
            url += str(query) + "=" + str(value) + "&"
        return url[:-1]

    def get_data(self):
        return self.data

    def get_headers(self):
        return self.headers

    def get_cookies(self):
        return self.cookies

    def __str__(self):
        return "Endpoint: " + self.url
class Api:
    TIME_DOMAIN = 'time-v2.bcity.me'
    OAUTH2_TOKEN_URL_PATH = '/oauth2/token/'
    OAUTH2_AUTHORISE_URL_PATH = '/oauth2/authorise/'
    API_URL_PATH = '/api/'
    DEFAULT_ROW_COUNT = 100 # 100 is the maximum no. of rows the API allows to retrieved at a time.
    UID_GET_ALL = -1
    UID_POST_MANY = -2
from bs4 import BeautifulSoup
import requests
import webbrowser

GITHUB_TAGS = "https://github.com/LSU-Devision/GUI/tags"
GITHUB_USER_GUIDE = "https://github.com/LSU-Devision/GUI/blob/main/Devision%20GUI%20user%20guide.pdf"
CURRENT_VERSION = 1.4


class Scraper:
    """
    class: Scraper
    description: class to scrape the GitHub
    params:
        None
    methods:
        check_internet(self)
        check_version(self)
        get_update_page(self)
        get_soup(self)
    """

    def __init__(self):
        """
        method: __init__
        description: initialize the class
        :return: None
        """
        # initialize the url, page, and soup
        self.url = None
        self.page = None
        self.soup = None

    def check_internet(self):
        """
        method: check_internet
        description: method to check if the internet is available
        :return: true or false depending on if the internet is available
        """
        # initialize the url, page, and soup
        self.url = "https://www.google.com"
        # try to request the url
        try:
            # request the url
            self.page = requests.get(self.url)
        # if the request fails
        except requests.exceptions.ConnectionError:
            # return false
            return False
        # return true
        return True


    def check_version(self):
        """
        method: check_version
        description: method to check if a new version is available
        :return: true or false depending on if a new version is available
        """
        # create a boolean flag to return, default false for no update required
        need_update_flag = False
        # set the url to the tags page
        self.url = GITHUB_TAGS
        # request the tags page
        self.page = requests.get(self.url)
        # parse the tags page
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        # find all the d4 classes
        d4_classes = self.soup.find_all(class_="f4 d-inline")
        # loop through the d4 classes
        for instance in d4_classes:
            # split the text of each d4 class by the / to get the versions
            version_list = instance.text.split("/")
            # loop through the version list
            for versions in version_list:
                # strip the 'v' from the versions
                versions = versions.strip('v')
                # check if the version is greater than the current version
                if CURRENT_VERSION < float(versions):
                    # set the flag to true
                    need_update_flag = True
                    # return the flag as True
                    return need_update_flag
        # return the flag as false
        return need_update_flag

    def get_update_page(self):
        return GITHUB_TAGS

    def get_soup(self):
        return self.soup
    
    # grabs the user guide 
    def get_user_guide(self):
        """
        method: get_user_guide
        Author: Zach James
        description: opens the user guide url in the user's default browser
        :return: void
        """
        webbrowser.open(GITHUB_USER_GUIDE)
        
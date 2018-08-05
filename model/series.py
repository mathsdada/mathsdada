from common_util import Common
from model.match import Match


class Series:
    def extract_matches_list_of_series(self):
        print(self.series_title)
        soup = Common.get_soup_object(self.series_link)
        series_formats = \
            soup.find('div', class_='cb-col-100 cb-col cb-nav-main cb-bg-white').find('div').text.split(".")[0]
        match_info_elements = soup.find_all('div', class_='cb-col-60 cb-col cb-srs-mtchs-tm')
        for match_info_element in match_info_elements:
            match_title = match_info_element.find('a', class_='text-hvr-underline')
            match_venue = match_info_element.find('div')
            match_result = match_info_element.find('a', class_='cb-text-link')
            if (match_title is not None) and ("cricket-scores" in match_title.get('href')) and \
                    (match_venue is not None) and (match_result is not None):
                match_format = Common.get_match_format(match_title.text, series_formats)
                if match_format in Common.match_formats:
                    match_link = match_title.get('href')
                    match_title = match_title.text
                    match_status = Common.get_match_outcome(match_result.text)
                    match_id = match_link.split("/")[2]
                    playing_teams = match_title.split(",")[0].split(" vs ")
                    match_object = Match(match_id, match_title, match_format,
                                         playing_teams, match_venue.text,
                                         match_status, Common.home_page + match_link)
                    self.matches_list.append(match_object)

    def __init__(self, series_id, series_title, series_year, series_link):
        self.series_id = series_id
        self.series_title = series_title
        self.series_year = series_year
        self.series_link = series_link
        self.matches_list = []
        # multiple thread can update squad. so use lock while updating this.
        self.squad = {}
        # self.__extract_matches_list_of_series()

    def get_matches_list(self):
        return self.matches_list
from scraper.common_util import Common
from scraper.model.schedule.series import Series


class Match:
    def __init__(self, title, venue, link, series_object):
        self.title = title
        self.venue = venue
        # teams is a dictionary in below form
        # {'team-1' : [team-1's squad], 'team-2' : [team-2's squad]}
        self.teams = None
        self.format = None
        self.date = None
        self.time = None

        self.series = series_object
        self.link = link

    def __extract_series_object(self, soup):
        series_block = soup.find('div', class_='cb-nav-subhdr cb-font-12').find('a', href=True)
        series_title = series_block.text
        series_link = Common.home_page + series_block.get('href')

        return Series(series_title, series_link)

    def __extract_teams(self, soup):
        teams = {}
        squad_blocks = soup.find_all('div', 'cb-col cb-col-100 cb-minfo-tm-nm')
        if len(squad_blocks) == 3:
            team_a = squad_blocks[0].text.split('\xa0')[0].strip()
            team_a_squad = squad_blocks[1].text.strip()
            team_b_squad = squad_blocks[2].text.strip()
            team_b = soup.find('div', 'cb-col cb-col-100 cb-minfo-tm-nm cb-minfo-tm2-nm').text \
                .split('\xa0')[0].strip()
            teams[team_a] = team_a_squad
            teams[team_b] = team_b_squad
        else:
            raise Exception("No Squad...")
        return teams

    def __extract_match_date_and_time(self, soup):
        match_info = {}
        match_info_items = soup.find_all('div', class_='cb-col cb-col-100 cb-mtch-info-itm')
        for match_info_item in match_info_items:
            key = match_info_item.find('div', class_='cb-col cb-col-27').text
            value = match_info_item.find('div', class_='cb-col cb-col-73').text
            match_info[key] = value
        date = match_info['Date']
        time = match_info['Time']


    def __extract_match_data(self):
        link = self.link.replace("live-cricket-scores", "live-cricket-scorecard")
        soup = Common.get_soup_object(link)
        if self.series is None:
            self.series = self.__extract_series_object(soup)
        self.teams = self.__extract_teams(soup)
        self.format = Common.get_match_format(self.title, self.series.format)
        self.date = None

    def get_series_object(self):
        return self.series

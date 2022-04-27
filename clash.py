from requests import get
from key import CLAHS_ROYALE_KEY


class Clan:
    """get clans raw info from API"""

    def __init__(self, clan_tag:str, init_all:bool=False):
        self.clan_tag = clan_tag
        if init_all:
            self._search_clans = self._request('')
            self._clan_info = self._request(f'/{self.clan_tag}')
            self._clan_members = self._request(f'/{self.clan_tag}/members')
            self._warlog = self._request(f'/{self.clan_tag}/warlog')
            self._riverracelog = self._request(f'/{self.clan_tag}/riverracelog')
            self._currentwar = self._request(f'/{self.clan_tag}/currentwar')
            self._currentriverrace = self._request(f'/{self.clan_tag}/currentriverrace')
        
        else:
            self._search_clans = None
            self._clan_info = None
            self._clan_members = None
            self._warlog = None
            self._riverracelog = None
            self._currentwar = None
            self._currentriverrace = None

    
    def _request(self, url_info=''):
        return get(url=f'https://api.clashroyale.com/v1/clans{url_info}', headers={"Authorization": f"Bearer {CLAHS_ROYALE_KEY}"}).json()

    """the 'get' attributes return the info that is already stored;
    if no info is stored, it calls the 'do's attributes and then return the information.
    
    The 'do' attributes calls the API the fresh information and store it
    
    This prevent multiples API calls"""

    def get_search_clans(self) -> dict:
        if self._search_clans is None:
            self.do_search_clans()
        return self._search_clans

    def do_search_clans(self) -> None:
        self._search_clans = self._request('')


    def get_clan_info(self) -> dict:
        if self._clan_info is None:
            self.do_clan_info()
        return self._clan_info

    def do_clan_info(self) -> None:
        self._clan_info = self._request(f'/{self.clan_tag}')


    def get_clan_members(self) -> dict:
        if self._clan_members is None:
            self.do_clan_members()
        return self._clan_members

    def do_clan_members(self) -> None:
        self._clan_members = self._request(f'/{self.clan_tag}/members')


    def get_warlog(self) -> dict:
        if self._warlog is None:
            self.do_warlog()
        return self._warlog
 
    def do_warlog(self) -> None:
        self._warlog = self._request(f'/{self.clan_tag}/warlog')


    def get_riverracelog(self) -> dict:
        if self._riverracelog is None:
            self.do_riverracelog()
        return self._riverracelog

    def do_riverracelog(self) -> None:
        self._riverracelog = self._request(f'/{self.clan_tag}/riverracelog')


    def get_currentwar(self) -> dict:
        if self._currentwar is None:
            self.do_currentwar()
        return self._currentwar

    def do_currentwar(self) -> None:
        self._currentwar = self._request(f'/{self.clan_tag}/currentwar')


    def get_currentriverrace(self) -> dict:
        if self._currentriverrace is None:
            self.do_currentriverrace()
        return self._currentriverrace

    def do_currentriverrace(self) -> None:
        self._currentriverrace = self._request(f'/{self.clan_tag}/currentriverrace')



class SpecifcInfo:
    """get specifc clan member info by tag.
    Return dict: {'playertag':{info:infovalue}}"""

    def __init__(self, clan_instance:type[Clan], players_tags:list[str]=None) -> None:
        self.clan_instance = clan_instance

        # Colect all tag from the clan members is None is given
        if players_tags is None:
            self.tags = [membro['tag'] for membro in clan_instance.get_clan_members()['items']]
        else:
            self.tags = players_tags
        

    def _extract_from_clan_members(self, tag:str, new_request:bool, dict_key:str) -> list:
        if new_request:
            self.clan_instance.do_clan_members()

        condition = "item['tag'] in self.tags" if tag is None else "item['tag'] == tag"

        return [
            {'tag': item['tag'], dict_key: item[dict_key]}
            for item in self.clan_instance.get_clan_members()['items']
            if eval(condition, {'self': self, 'tag': tag, 'item':item})]

    def get_name(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_clan_members(tag, new_request, 'name')

    def get_role(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_clan_members(tag, new_request, 'role')

    def get_level(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_clan_members(tag, new_request, 'expLevel')

    def get_trophies(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_clan_members(tag, new_request, 'trophies')

    def get_trophies(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_clan_members(tag, new_request, 'clanRank')

    def get_donations_send(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_clan_members(tag, new_request, 'donations')

    def get_donations_received(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_clan_members(tag, new_request, 'donationsReceived')
        

    def _extract_from_currentriverrace(self, tag:str, new_request:bool, dict_key:str) -> list:
        if new_request:
            self.clan_instance.do_currentriverrace()

        condition = "item['tag'] in self.tags" if tag is None else "item['tag'] == tag"

        return [
            {'tag': item['tag'], dict_key: item[dict_key]}
            for item in self.clan_instance.get_currentriverrace()['clan']['participants']
            if eval(condition, {'self': self, 'tag': tag, 'item':item})]


    def get_war_fame(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_currentriverrace(tag, new_request, 'fame')

    def get_war_repair_points(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_currentriverrace(tag, new_request, 'repairPoints')
    
    def get_war_boat_attacks(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_currentriverrace(tag, new_request, 'boatAttacks')

    def get_war_decks_used(self, tag:str=None, new_request:bool=False) -> list:
        return self._extract_from_currentriverrace(tag, new_request, 'decksUsed')

    
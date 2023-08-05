from .riot_api_caller import RiotAPICaller
from .riot_api_helper import RiotAPIHelper
from typing import Literal, List


class QueryContext:
    """
    Keeps track of context of the query so that multiple queries could be run without having to
    enter the same data again and again.
    """

    def __init__(self, in_riot_api_caller: RiotAPICaller):
        self.riot_api_caller = None
        self.region_server = None
        self.region_continent = None
        self.summoner_encrypted_id = None
        self.summoner_account_id = None
        self.summoner_puuid = None
        self.summoner_name = None
        self.matches_list = None
        self.set_riot_api_caller(in_riot_api_caller)

    def set_riot_api_caller(self, in_riot_api_caller: RiotAPICaller):
        """
        Set the RiotAPICaller object
        """
        self.riot_api_caller = in_riot_api_caller

    def set_region_server(self, in_region_server: Literal["br1", "eun1", "euw1", "jp1", "kr",
                                                          "la1", "la2", "na1", "oc1", "ph2", "ru",
                                                          "sg2", "th2", "tr1", "tw2", "vn2"]):
        """
        Set the region of the server.
        E.g. "na1"
        The context will automatically set its region_continent accordingly.
        """
        self.region_server = in_region_server
        self.region_continent = RiotAPIHelper.LOL_SERVER_TO_CONTINENT[in_region_server]

    def get_summoner_by_name(self, in_summoner_name: str) -> dict:
        """
        Gets a summoner from the API and stores this summoner as a part of the current context.
        Returns all the retrieved data from the get_sommoner_by_name RiotAPI call.
        (Uses one RiotAPI call)

        Parameters
        ----------
        in_summoner_name
            Summoner name

        Returns
        -------
            Summoner Info dictionary which contains ids, name, level, etc.
        """

        summoner_info = RiotAPIHelper.get_summoner_by_name(self.riot_api_caller, self.region_server, in_summoner_name)
        self.summoner_name = summoner_info['name']
        self.summoner_encrypted_id = summoner_info['id']
        self.summoner_account_id = summoner_info['accountId']
        self.summoner_puuid = summoner_info['puuid']
        self.summoner_name = summoner_info['name']
        return summoner_info

    def get_summoner_by_puuid(self, in_encrypted_puuid):
        """
        Gets a summoner from the API and stores this summoner as a part of the current context.
        Returns all the retrieved data from the get_summoner_by_puuid RiotAPI call.
        (Uses one RiotAPI call)

        Parameters
        ----------
        in_encrypted_puuid
            Encrypted PUUID of the summoner.

        Returns
        -------
            Summoner Info dictionary which contains ids, name, level, etc.
        """
        summoner_info = RiotAPIHelper.get_summoner_by_puuid(self.riot_api_caller, self.region_server, in_encrypted_puuid)
        self.summoner_name = summoner_info['name']
        self.summoner_encrypted_id = summoner_info['id']
        self.summoner_account_id = summoner_info['accountId']
        self.summoner_puuid = summoner_info['puuid']
        self.summoner_name = summoner_info['name']
        return summoner_info

    def get_matches(self, in_count: int, in_type: Literal["ranked", "normal", "tourney", "tutorial"] = None,
                    in_queue: int = None, in_start_time: int = 0, in_end_time: int = 0, in_start: int = 0) -> List[str]:
        """
        Retrieves a list of matches that fits the given filtering criteria.
        (Uses one RiotAPI call)

        Parameters
        ----------
        in_count
            Number of match ids to download. Valid values 0 and 100.
        in_type
            Type of match from one of {"ranked","normal","tourney","tutorial"}
        in_queue
            Queue type number.
                Some values (not the complete list):
                    420: for Ranked Solo Queue Summoner's Rift
                    440: for Ranked Flex Queue Summoner's Rift
                    400: for Draft Pick
                    430: for Blind Pick
                Check RiotAPI documents on QueueID for a complete list.
        in_start_time
            Epoch timestamp in seconds. The furthest time in the past that you want the data to start from.
        in_end_time
            Epoch timestamp in seconds. The closest time to the future that you want the data to stop.
        in_start
            The start index of the match list, for a given criteria.
            Say you downloaded first 100 matches for a given type and a queue within a specific start and end time range
            with in_start=0, then you can download the next 100 matches by setting in_start=100 and keeping all the
            other parameters the same.

        Returns
        -------
            List of matches
        """
        self.matches_list = RiotAPIHelper.get_matches_list(self.riot_api_caller, self.region_continent,
                                                           self.summoner_puuid,
                                                           in_count, in_type, in_queue, in_start_time, in_end_time,
                                                           in_start)
        return self.matches_list

    def get_all_matches(self, in_type: Literal["ranked", "normal", "tourney", "tutorial"] = None,
                        in_queue: int = None, in_start_time: int = 0, in_end_time: int = 0) -> List[str]:
        """
        Retrieves all matches that fits the given filtering criteria.
        (Uses multiple RiotAPI calls).

        Parameters
        ----------
        in_type
            Type of match from one of {"ranked","normal","tourney","tutorial"}
        in_queue
            Queue type number.
                Some values (not the complete list):
                    420: for Ranked Solo Queue Summoner's Rift
                    440: for Ranked Flex Queue Summoner's Rift
                    400: for Draft Pick
                    430: for Blind Pick
                Check RiotAPI documents on QueueID for a complete list.
        in_start_time
            Epoch timestamp in seconds. The furthest time in the past that you want the data to start from.
        in_end_time
            Epoch timestamp in seconds. The closest time to the future that you want the data to stop.
        Returns
        -------
            The list of all matches that fits the given criteria.
        """
        this_summoner_matches = []
        this_match_list = self.get_matches(100, in_type, in_queue, in_start_time, in_end_time, in_start=0)
        print("Matches:", len(this_match_list))
        print(this_match_list)
        this_summoner_matches.extend(this_match_list)
        while len(this_match_list) == 100:
            this_match_list = self.get_matches(100, in_type, in_queue, in_start_time, in_end_time,
                                               in_start=len(this_summoner_matches))
            print("Matches:", len(this_match_list))
            print(this_match_list)
            this_summoner_matches.extend(this_match_list)
        return this_summoner_matches

    def get_match_info(self, in_match_id: str) -> dict:
        """
        Retrieves match_info structure from the RiotAPI for the given match.
        Returned dictionary contains summary information about the match.
        (Uses one RiotAPI call)

        Parameters
        ----------
        in_match_id
            MatchID which usually has the form "{server}_{gameId}"
            E.g. "NA_123456789"

        Returns
        -------
            JSON like data structure containing match_info
        """
        match_info = RiotAPIHelper.get_match_info(self.riot_api_caller, self.region_continent, in_match_id)
        return match_info

    def get_match_timeline(self, in_match_id: str) -> dict:
        match_timeline = RiotAPIHelper.get_match_timeline(self.riot_api_caller, self.region_continent, in_match_id)
        return match_timeline

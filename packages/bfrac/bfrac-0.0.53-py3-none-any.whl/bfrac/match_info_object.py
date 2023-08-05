class MatchInfoObject:

    def __init__(self, in_match_info_json):
        self.raw_data = in_match_info_json

    def get_summoner_names(self):
        ps = {}
        for p in self.raw_data['info']['participants']:
            if p['teamId'] not in ps:
                ps[p['teamId']] = []
            ps[p['teamId']].append(p['summonerName'])
        return ps

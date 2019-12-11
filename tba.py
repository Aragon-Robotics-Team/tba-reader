def main():
    import tbaapiv3client
    import csv
    TOKEN = "REPLACEME"
    class Api:
        def __init__(self, token):
            self.token = token
            #
            config = tbaapiv3client.Configuration()
            config.api_key['X-TBA-Auth-Key'] = self.token
            self.api = tbaapiv3client.ApiClient(config)
            #
            self.event = tbaapiv3client.EventApi(self.api)
            self.team =  tbaapiv3client.TeamApi(self.api)
    def gen_events():
        EVENTS = {"sf": "casf", "sv": "casj", "cv": "cafr"}
        YEARS = (19, 20)
        d = {}
        for short, long in EVENTS.items():
            for year in YEARS:
                d[str(year) + short] = "20" + str(year) + long
        return d
    EVENTS = gen_events()
    API = Api(TOKEN)
    def get_teams_in_events(*events):
        teams = set()
        for event in events:
            event = EVENTS[event]
            teams.update(API.event.get_event_teams_keys(event))
        teams = sorted(list(teams), key=lambda x: int(x[3:]))
        return teams
    teams = get_teams_in_events("19sf", "19sv")
    #for team in teams:
    #    print(team)
    # team = "frc840"
    #API, teams = main()
    Teams = []
    print(len(teams))
    for i, team in enumerate(teams):
        print(i, team)
        t_awards = API.team.get_team_awards_by_year(team, 2019)
        Teams.append([
            team,
            #t_awards.nickname,
            *[award.name for award in t_awards if award.recipient_list[0].awardee in (None, '')]
        ])
    print("DONE")
    with open("awards.csv", "w", newline='') as file:
        file = csv.writer(file)
        file.writerow(["Number", "Team Awards"])
        file.writerows(Teams)
    return

main()



    Teams = []
    print(len(teams))
    for i, team in enumerate(teams):
        print(i, team)
        team = API.team.get_team(team)
        team_events = API.team.get_team_events_by_year_simple(team.key, 2019)
        Teams.append([
            team.team_number,
            team.nickname,
            team.city,
            team.state_prov,
            team.rookie_year,
            " ".join([x.key for x in team_events])
        ])
    print("DONE")
    with open("teams.csv", "w", newline='') as file:
        file = csv.writer(file)
        file.writerow(["Number", "Name", "City", "State", "Rookie", "Events"])
        file.writerows(Teams)



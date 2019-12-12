def sorted_teams(teams):
    return sorted(teams, lambda team: int(team[3:]))

def get_teams_in_events(api, *events):
        teams = set()

        for event in events:
            teams.update(api.event.get_event_teams_keys(event))

        return sorted_teams(teams)

import csv
from collections import defaultdict
from pprint import pprint
from typing import List

import tba

TEAM = "frc" + str(int(840))
YEAR = 2019
FILENAME = "Event {e.name}.csv"


class CSV_DIALECT(csv.excel):
    lineterminator = "\n"


def gen_api():
    token = tba.read_token()
    api = tba.Api(token, debug=False, pythonanywhere=False)

    return api


def format_teams(alliance):
    return [int(x[3:]) for x in alliance.team_keys]


def main():
    api = gen_api()

    status = api.tba.get_status()
    year = status.current_season
    if not year == YEAR:
        raise RuntimeError(f"Program set to run for {YEAR}, but currently it is {year}")

    print(f"Getting events {TEAM} goes to in {YEAR}")
    events = api.event.get_team_events_by_year_simple(TEAM, YEAR)
    events: List[tba.tbaapiv3client.EventSimple]

    for i, event in enumerate(events):
        print(f"{i+1}. {event.name:<30}{event.key}")

    for event in events:
        print(f"\nProcessing event {event.key}")

        #  https://github.com/the-blue-alliance/the-blue-alliance/blob/master/consts/event_type.py#L2
        # Event type 0 == Regional
        if event.event_type != 0:
            print("    Event is not a Regional: Skipping")
            continue

        print("    Loading Matches")
        matches = api.match.get_event_matches_simple(event.key)
        matches: List[tba.tbaapiv3client.MatchSimple]
        match_l: List[tba.tbaapiv3client.MatchSimple]

        sorted_matches = defaultdict(list)

        for match in matches:
            sorted_matches[match.comp_level].append(
                (match.set_number, match.match_number, match)
            )

        for match_l in sorted_matches.values():
            match_l.sort()

        rows = []

        for match_type in tba.MATCH_ORDER:
            match_l = sorted_matches.get(match_type)

            if match_l is None:
                continue

            for m_set, m_num, match in match_l:
                if m_num == 19:
                    # print()
                red: tba.tbaapiv3client.MatchAlliance = format_teams(
                    match.alliances.red
                )
                blue: tba.tbaapiv3client.MatchAlliance = format_teams(
                    match.alliances.blue
                )

                rows.append(
                    [tba.MATCH_MAPPING[match_type], f"{m_set}.{m_num}"] + red + blue
                )

        filename = FILENAME.format(e=event)

        print(f"    Writing to file {filename}")

        with open(filename, "w") as f:
            f = csv.writer(f, dialect=CSV_DIALECT)
            f.writerow(
                [
                    "Event",
                    event.name,
                    "Start Date",
                    event.start_date,
                    "End Date",
                    event.end_date,
                    "Key",
                    event.key,
                ]
            )

            f.writerow(
                ["Type", "Number", "Red Alliance", "", "", "Blue Alliance", "", ""]
            )

            f.writerows(rows)

    print("\nFinished processing events")


if __name__ == "__main__":
    main()

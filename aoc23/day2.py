def convert_round_string_to_dict(round_string: str) -> dict[str, int]:
    round_dict = {}
    strings = round_string.split(', ')
    for s in strings:
        num, colour = s.split(' ')
        round_dict[colour] = int(num)
    return round_dict


def process_input_2(input_2: list[str]) -> dict[int, list[dict[str, int]]]:
    games = {}
    for line in input_2:
        game_str, rounds_str = line.split(': ')
        game = int(game_str.split(' ')[-1])
        round_strings = rounds_str.split('; ')
        rounds = [convert_round_string_to_dict(round_str) for round_str in round_strings]
        games[game] = rounds

    return games


def check_round_possible(round: dict[str, int], hypothetical: dict[str, int]) -> bool:
    return all([
        round[colour] <= hypothetical[colour]
        for colour in round
    ])


def is_game_possible(game: list[dict[str, int]], hypothetical: dict[str, int]) -> bool:
    return all([
        check_round_possible(round, hypothetical)
        for round in game
    ])


def compute_minimum_set(game: list[dict[str, int]]) -> dict[str, int]:
    minimum_set = {'blue': 0, 'green': 0, 'red': 0}
    for round in game:
        minimum_set = {
            colour: max(minimum_set[colour], round.get(colour, 0))
            for colour in ['blue', 'red', 'green']
        }
    return minimum_set

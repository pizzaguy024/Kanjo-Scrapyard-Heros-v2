RANKS = [
    {"title": "Scrap Rookie", "required_rep": 0},
    {"title": "Oil Burner", "required_rep": 100},
    {"title": "Backroad Menace", "required_rep": 500},
    {"title": "Kanjo Runner", "required_rep": 1500},
    {"title": "Expressway Regular", "required_rep": 3000},
    {"title": "Midnight Threat", "required_rep": 5000},
    {"title": "Street Veteran", "required_rep": 10000},
    {"title": "Scrap Yard Hero", "required_rep": 20000},
    {"title": "Expressway King", "required_rep": 50000},
    {"title": "Kanjo Legend", "required_rep": 100000},
]


def get_rank(reputation):
    current_rank = RANKS[0]
    next_rank = None

    for rank in RANKS:
        if reputation >= rank["required_rep"]:
            current_rank = rank
        else:
            next_rank = rank
            break

    return current_rank, next_rank


def format_rank_progress(reputation):
    current_rank, next_rank = get_rank(reputation)

    if not next_rank:
        return f"""
Rank: {current_rank['title']}
Progress: MAX RANK
"""

    needed = next_rank["required_rep"] - reputation

    return f"""
Rank: {current_rank['title']}
Next Rank: {next_rank['title']}
Reputation Needed: {needed}
"""

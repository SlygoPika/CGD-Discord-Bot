def auto_team_channel_naming(existing_teams):
    team_count = 0
    title = f"Team-{str(team_count).zfill(4)}"

    while title in existing_teams:
        temp_title = f"Team-{str(team_count).zfill(4)}"
        if temp_title not in existing_teams:
            title = temp_title
            return title
        team_count += 1
    return None

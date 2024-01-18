import cogs.utils.constants as constants


def auto_team_channel_naming(existing_teams):
    team_count = 0
    title = f"{constants.NEW_TEAM_NAME_PREFIX}{str(team_count).zfill(4)}"

    while title in existing_teams:
        temp_title = f"{constants.NEW_TEAM_NAME_PREFIX}{
            str(team_count).zfill(4)}"
        if temp_title not in existing_teams:
            title = temp_title
            return title
        team_count += 1
    return None

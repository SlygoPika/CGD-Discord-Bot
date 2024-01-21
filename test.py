import pandas as pd

teams_dict = {
    "ID": [1, 2, 3],
    "Team Name": ["team-1", "team-2", "team-3"],
    "Team Leader": ["hublooo", "test", ""],
    "Team Members": ["hublooo", "hublooo", ""]
}


df = pd.DataFrame(teams_dict)
df.insert
df.to_excel("teams.xlsx", index=False)
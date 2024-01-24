# Discord bot for Concordia Game Development club
Discord.py bot for all CGD-related needs. Hosted on Google Cloud.
### Current functionalities:
*Team Logistics (Used for GGJ 2024)*:
- Allows users to make, create and customize teams using the UI below. When the "Create Team" button is clicked, a new role, text channel, and voice channel that belongs to the team is created.
![alt text](https://github.com/SlygoPika/CGD-Discord-Bot/blob/main/img/teamFormingUI.png)
- Exports team data into a spreadsheet containing team names, members, and the team leader

### Available commands:
*User commands:*
- **SetTeamName**
Sets your team's name. Only available in your channel. 5 minute cooldown. Usage:
$SetTeamName "newTeamName"
- **HandTeamLeaderTo**
Hand over team leader role to another member of your team. Usage:
$HandTeamLeaderTo @newLeader
- **SetTeamEmoji**
Sets your team's emoji. Only available in your channel. 5 minute cooldown. Usage:
$SetTeamEmoji "newTeamEmoji"
- **Help**
Displays a message explaining the available user commands. Usage:
$Help

*Admin commands:*
- **RenameTeam**
Admin Command: Renames an already existing team channel/role. Usage:
$RenameTeam <TeamName> <NewTeamName>
- **ExportTeamData**
Admin Command: Exports the team data to an Excel file. Usage:
$ExportTeamData
- **SetTeamCategory**
Admin command: Sets the category for team channels. Usage:
$SetTeamCategory <TeamCategory>
- **MoveUserToTeam**
Admin Command: Moves a user to a different team. Usage:
$MoveUserToTeam <@User> <Team>
- **DeleteTeam**
Admin Command: Deletes a team. Usage:
$DeleteTeam <Team>
- **ResetTeams**
Admin Command: Removes all existing teams. Usage:
$ResetTeams
- **SwitchTeamLeader**
Admin Command: Switches the team leader of a team. Usage:
$SwitchTeamLeader <@User> <Team>
- **SetReccomendedTeamSize**
Admin command: Sets the reccomended team size Usage:
$SetReccomendedTeamSize <number>
- **PrintTeams**
Admin Command: Prints all existing teams. Usage:
$PrintTeams
- **AddTeam**
Admin command: Adds an already existing team channel/role to the team forming channel. Use in case the bot needs to be rebooted. Usage:
$AddTeam <TeamName>
- **SetTeamFormingChannel**
Admin command: Sets the team forming channel. Usage:
$SetTeamFormingChannel <ChannelName>
- **UnfreezeTeams**
Admin command: Unfreezes the teams so that people can join or leave. Usage:
$UnfreezeTeams
- **FreezeTeams**
Admin command: Freezes the teams so that no one can join or leave. Usage:
$FreezeTeams
- **HelpAdmin**
Admin Command: Displays the admin commands.
- **SetTeamFormingEmoji**
Admin command: Sets the default emoji reaction for creating a team. Default is ✅. Usage:
$SetTeamFormingEmoji <TeamEmoji>
- **HelpAdmin**
Admin command: Displays a message explaining the available user commands. Usage:
$HelpAdmin

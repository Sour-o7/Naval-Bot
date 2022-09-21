from __future__ import print_function
from discord.ext import commands
from apiclient import discovery
from google.oauth2 import service_account
from discord.ext import commands
from pytz import timezone
from datetime import datetime
import discord
import os.path
import os

class LogTime(commands.GroupCog):
    def __init__(self, client) -> None:
        self.client = client
        super().__init__()
        
        scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
        tokens = os.path.join(os.getcwd(), 'naval_keys.json')
        credentials = service_account.Credentials.from_service_account_file(tokens, scopes=scopes)
        self.service = discovery.build('sheets', 'v4', credentials=credentials)

    # Add a and b using HH:MM Format
    async def maths_handler(self, a, b):
        timeList = [a, b]
        totalSecs = 0
        for tm in timeList:
            timeParts = [int(s) for s in tm.split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60
        totalSecs = divmod(totalSecs, 60)[0]
        hours, minutes = divmod(totalSecs, 60)
        return "%d:%02d" % (hours, minutes)
            
    async def update_time_66th(self, author_id, time):
        spreadsheet_id = '11SkMX6xIxmtMfEshO0wWf9u7j0g7g_Gs8LIQyh-UIHo'

        # Get columns H - N
        members = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=("'Roster'!H:N")).execute().get('values')
        members = [[i[0], i[1], i[2], i[3], i[4], i[5], i[6]] if len(i) == 7 else ['', '', '', '', '', '', ''] for i in members]
        # Get author's row number
        row_number = [n[6] for n in members].index(str(author_id))
       
       # Check if author was last seen on today
        last_online = datetime.now(timezone('US/Eastern')).strftime("%#m/%#d")
        if str(members[row_number][0]) != str(last_online):
            # Format new values
            values = [[str(last_online), members[row_number][1], str(int(members[row_number][2]) + 1), await self.maths_handler(members[row_number][3], time), members[row_number][4], members[row_number][5], members[row_number][6]],]
        else:
            # Format new values
            values = [[members[row_number][0], members[row_number][1], members[row_number][2], await self.maths_handler(members[row_number][3], time), members[row_number][4], members[row_number][5], members[row_number][6]],]

        # Update spreadsheet
        range_name = f"'Roster'!H{str(int(row_number) + 1)}:N{str(int(row_number) + 1)}"
        body = {'values': values}
        self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name,valueInputOption='USER_ENTERED', body=body).execute()

    async def update_time_1st(self, author_id, time):
        spreadsheet_id = '1KbICKqX9xpgq4_Jw5JxrvnfxR702rv6y43HG5OxjEnk'
        # Get columns I - J
        members = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=("'Squad Roster'!I:J")).execute().get('values')
        # Get discordid and time
        members = [[i[0], i[1]] if len(i) == 2 else ([i[0], '0:0'] if len(i) == 1 else ['', '']) for i in members]
        # Get Row Number
        row_number = [n[0] for n in members].index(str(author_id))
        
        # Update spreadsheet
        values = [[await self.maths_handler(members[row_number][1], time)],]
        range_name = f"'Squad Roster'!J{str(int(row_number) + 1)}"
        body = {'values': values}
        self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_name,valueInputOption='USER_ENTERED', body=body).execute()

    @commands.hybrid_command(name="time66")
    async def time_66th(self, ctx: commands.Context, hours: int = 0, minutes: int = 0):
        # Extend Reponse TimeFrame
        await ctx.defer()
        # If channel is not 66th timesheets
        if ctx.channel.name != "66th-timesheets":
            await ctx.send("Please use the command in the proper channel", ephemeral=True)
            return
        # Send Message
        message = await ctx.send(f"<@{ctx.author.id}> - {hours} hours and {minutes} minutes")
        # Update time and react to message
        try:
            await self.update_time_66th(ctx.author.id, f"{hours}:{minutes}")
            await message.add_reaction('<ImperialApprovedStamp:503286393674661891>')
        except Exception as e:
            print(e)
            await ctx.channel.send(f"<@295644243945586688> {e}")
            
    @commands.hybrid_command(name="time1st")
    async def time_1st(self, ctx: commands.Context, hours: int = 0, minutes: int = 0):
        # Extend reponse TimeFrame
        await ctx.defer()
        # If channel is not 1st-timesheets
        if ctx.channel.name != "1st-timesheets":
            await ctx.send("Please use the command in the proper channel", ephemeral = True)
            return
        # Send Message
        message = await ctx.send(f"<@{ctx.author.id}> - {hours} hours and {minutes} minutes")
        # Update time and react
        try:
            await self.update_time_1st(ctx.author.id, f"{hours}:{minutes}")
            await message.add_reaction('<ImperialApprovedStamp:503286393674661891>')
        except Exception as e:
            print(e)
            await ctx.channel.send(f"<@295644243945586688> {e}")

# Setup Function          
async def setup(client: commands.Bot) -> None:
    await client.add_cog(LogTime(client))

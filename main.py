import discord
from discord.ext import commands

# Bot setting
intents = discord.Intents.default()
intents.presences = True  # Presence Intent 
intents.members = True    # Member Intent

bot = commands.Bot(command_prefix='!', intents=intents)

ONLINE_ROLE_ID = 123456789012345678  # Online role ID
OFFLINE_ROLE_ID = 234567890123456789  # Offline role ID

@bot.event
async def on_ready():
    print(f'{bot.user.name} has Starting !')

@bot.event
async def on_presence_update(before, after):
    try:
        # Debugging log
        print(f"DEBUG: User: {after.name}, Before: {before.status}, After: {after.status}")

        guild = after.guild
        online_role = guild.get_role(ONLINE_ROLE_ID)
        offline_role = guild.get_role(OFFLINE_ROLE_ID)
      
        if not online_role or not offline_role:
            print("Role not found. Please check the role ID. ")
            return

        # Handling online status
        if after.status in [discord.Status.online, discord.Status.idle, discord.Status.dnd]:
            if offline_role in after.roles:
                await after.remove_roles(offline_role)  # Remove offline role
                print(f"DEBUG: {after.name} - Remove offline role ")
            if online_role not in after.roles:
                await after.add_roles(online_role)  # Remove online role
                print(f"DEBUG: {after.name} - Remove online role")
              
        elif after.status == discord.Status.offline:
            if online_role in after.roles:
                await after.remove_roles(online_role)  # Remove online role
                print(f"DEBUG: {after.name} - Remove online role")
            if offline_role not in after.roles:
                await after.add_roles(offline_role)  # Remove offline role
                print(f"DEBUG: {after.name} - Remove offline role")
    except Exception as e:
        print(f"An error occurred: {e}")


TOKEN = "BOT_TOKEN"
bot.run(TOKEN)

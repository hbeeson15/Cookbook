import discord
import mysql.connector
import formatRec
from dotenv import load_dotenv
load_dotenv()
import os

# connect to SQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = "holly",
    passwd = os.getenv("DB_PASSWORD"),
    database = "Cookbook"
)

# Discord token
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

# tell bot how to respond
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    # command to display all recipes
    if message.content.startswith('!getAll'):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM recipes")
        myresult = mycursor.fetchall()
        for x in myresult:
            await client.send_message(message.channel, formatRec.formatRec(x))
    
    # command to add new recipe to database
    if message.content.startswith('!add'):
        msg = message.content.split("|")
        print (msg)
        commands = (msg[1], msg[2], msg[3], msg[4])
        mycursor = mydb.cursor() 
        val = ("INSERT INTO recipes (r_name, protein_source, ingredients, instructions) VALUES (%s, %s, %s, %s)")
        mycursor.execute(val, commands)

        mydb.commit()
        await client.send_message(message.channel, mycursor.rowcount)        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)    


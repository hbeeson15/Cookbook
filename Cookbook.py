import discord
import mysql.connector
import formatRec
from dotenv import load_dotenv
load_dotenv()
import os
from random import randint

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
        await client.send_message(message.channel, 'Yummy!')

    # command to get a random recipe
    if message.content.startswith('!random'):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM recipes")
       
        myresult = mycursor.fetchall()
        index = randint(0, len(myresult)-1)
        await client.send_message(message.channel, formatRec.formatRec(myresult[index]))

    # command to list all commands
    if message.content.startswith('!help'):
        await client.send_message(message.channel, "Commands: !getAll, !random, !add, !protein, !name" + 
        "\n !add syntax: |name|protein source|ingredients|instructions \n !protein syntax: |protein name (partial or whole)" + 
            "\n !name syntax: |name (partial or whole)")

    # command to query by protein source    
    if message.content.startswith('!protein'):
        msg = message.content.split("|")
        mycursor = mydb.cursor()
        val = ("SELECT * FROM recipes WHERE protein_source LIKE %s")
        param = ('%'+msg[1]+'%',)
        mycursor.execute(val, param)
        myresult = mycursor.fetchall()
        for x in myresult:
            await client.send_message(message.channel, formatRec.formatRec(x))    

    # command to query by name
    if message.content.startswith('!name'):
        msg = message.content.split("|")
        mycursor = mydb.cursor()
        val = ("SELECT * FROM recipes WHERE r_name LIKE %s")
        param = ('%'+msg[1]+'%',)
        mycursor.execute(val, param)
        myresult = mycursor.fetchall()
        for x in myresult:
            await client.send_message(message.channel, formatRec.formatRec(x))
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)    


# -*- coding: utf-8  -*-

import asyncio, discord
import requests
import datetime
import sys
import argparse
import string


ap = argparse.ArgumentParser()
ap.add_argument("-b", "--bot", required=True, help="Discord Bot Token")
args = vars(ap.parse_args())
token = args["bot"]


trust = ["Utilisateur 1", "Utilisateur 2"] #Trusted users for restricted commands 
trust_roles = [""]
ranks = False
client = discord.Client()
ver = "0.1"
lang = "fr"



print("WarezBot " + ver + " " + lang)


@client.event
@asyncio.coroutine
def on_message(message):

    rep = text = msg = message.content
    rep2 = text2 = msg2 = rep.split()
    user = str(message.author)
    user_bot_client = client.user.name
    user_bot = user_bot_client.split("#")[0]
    role_trusted = False
    if type(message.guild) is discord.guild.Guild:
        server_msg = str(message.channel.guild)
        chan_msg = str(message.channel.name)
        for role_name in trust_roles:
            if ":" in role_name and role_name.split(":")[0] == server_msg:
                rank_role = discord.utils.get(message.server.roles, name = ":".join(role_name.split(":")[1:]))
            else:
                rank_role = discord.utils.get(message.guild.roles, name = role_name)
            if type(rank_role) is discord.role.Role and rank_role.id in [r.id for r in message.author.roles]:
                role_trusted = True
        pm = False
    else:
        server_msg = user
        chan_msg = user
        pm = True
    trusted = user in trust or role_trusted
    print(trusted)
    try:
        command = rep2[0].lower()
        params = rep2[0:]
    except IndexError:
        command = ""
        params = ""

    print(user + " (" + server_msg + ") [" + chan_msg + "] : " + rep)

    if ranks and not pm:
        open("msgs_user_" + server_msg + ".txt", "a").close()
        msgs = open("msgs_user_" + server_msg + ".txt", "r")
        msgs_r = msgs.read()
        if user not in msgs_r or user != user_bot_client:
            msgs_w = open("msgs_user_" + server_msg + ".txt", "a")
            msgs_w.write(user + ":0\n")
            msgs_w.close()
            msgs.close()
            msgs = open("msgs_user_" + server_msg + ".txt", "r")
            msgs_r = msgs.read()
        msgs_user = msgs_r.split(user + ":")[1]
        msgs.close()
        user_msgs_n = int(msgs_user.split("\n")[0])
        user_msgs_n += 1
        msgs_r = msgs_r.replace(user + ":" + str(user_msgs_n - 1), user + ":" + str(user_msgs_n))
        msgs = open("msgs_user_" + server_msg + ".txt", "w")
        msgs.write(msgs_r)
        msgs.close()
#Début des commandes

    if command == "!commandtest": #Copiez ce code pour créer une commande
        yield from message.channel.send("Texte à envoyer.")
        game = discord.Game("Dev by Enzobes")
        yield from client.change_presence(status=discord.Status.online, activity=game)
#Fin des commandes
#COMMANDES PERSO
    if command == "!pre":
        #You can use my key or if you make a large amount of request you can ask for a key here : predb.org/about
        r=requests.get(url='https://predb.org/api/enzobes/q2AQ74sPd9kGWQ86/pre/'+ params[1])
        data = r.text
        if data == "":
            yield from message.channel.send("**"+list_nfo[1]+"**" + " n'est pas une team scène !")
        else:
            yield from message.channel.send("**Pre:** " + data)

    if command == "!nfo":

        try:
             yield from message.channel.send("Searching on Srrdb ...")
             r3=requests.get(url='https://www.srrdb.com/api/nfo/' +params[1])
             data3=r3.json()
             srrdb_nfo = data3['nfo']
             srrdb_nfo_link = data3['nfolink']
             print(srrdb_nfo_link)
             if data3['nfo']:
                 yield from message.channel.send("**Nfo Srrdb: **" + str(srrdb_nfo))
                 yield from message.channel.send("**Download Srrdb: **" + str(srrdb_nfo_link))
                 return

             if len(srrdb_nfo) > 0:
                 yield from message.channel.send("No nfo on Srrdb for:" + "**" + params[1] + "**")
                 return
        except KeyError:
            yield from message.channel.send("No nfo found:** " + params[1] + "**")

    if command == "!group":
        yield from message.channel.send("I'm searching ... ")
        r=requests.get(url='https://www.srrdb.com/api/search/group:' +params[1] + '/order:date-desc/skip:5')
        data=r.json()

        if not data['results']:

            yield from message.channel.send("**" + params[1] +"** "+ "is not a scene team !")

        else:
            yield from message.channel.send("**Last 5 releases of " + params[1] +": **\n ")
            for i in data['results']:

                release = i['release']
                yield from message.channel.send("```" + release + "```")
#        no_team = params[1]
#        yield from client.send_message(message.channel, "**"+ no_team +"**" + " n'est pas une team scène !")
    if command == "!imdb":
        yield from message.channel.send("Retrieve information from IMDB ... ")
        r=requests.get(url='https://www.srrdb.com/api/imdb/' + params[1])
        data=r.json()
        try:

            imdb_id = data['releases'][0]['imdb']
            imdb_title = data['releases'][0]['title']
            imdb_title_omdb = imdb_title.replace(" ", "+")
            print(imdb_title_omdb)
            #You can use your own omdbapi.com key
            r2=requests.get(url='http://www.omdbapi.com/?i=tt' + imdb_id + '&apikey=5e539b')
            data2=r2.json()

            print(data2)
            omdb_released = data2['Released']
            omdb_runtime = data2['Runtime']
            omdb_genre = data2['Genre']
            omdb_director = data2['Director']
            omdb_writer = data2['Writer']
            omdb_actor = data2['Actors']
            omdb_plot = data2['Plot']
            omdb_language = data2['Language']
            omdb_country = data2['Country']
            omdb_rating = data2['imdbRating']
            omdb_votes = data2['imdbVotes']
            omdb_dvd = data2['DVD']
            omdb_production = data2['Production']
            omdb_boxoffice = data2['BoxOffice']
            omdb_type = data2['Type']
            omdb_website = data2['Website']
            omdb_awards = data2['Awards']
            omdb_id = data2['imdbID']
            imdb_link = 'https://imdb.com/title/' + omdb_id + "/"
            #imd_src = data2['Ratings'][0]['Source']
            #imd_value = data2['Ratings'][0]['Value']
            #rotten_src = data2['Ratings'][1]['Source']
            #rotten_value = data2['Ratings'][1]['Value']
            #meta_src = data2['Ratings'][2]['Source']
            #meta_value = data2['Ratings'][2]['Value']

            #imdb_link = 'https://www.imdb.com/title/' + omdb_id + "/"

            yield from message.channel.send("**Link:** " + imdb_link + "\n**Title:** " + imdb_title + "\n**IMDB Rating:** " + omdb_rating + "/10" + "\n**IMDB Votes:** " + omdb_votes + "\n**Released:** " + omdb_released + "\n**DVD:** " + omdb_dvd + "\n**Runtime:** " + omdb_runtime + "\n**Genre:** " + omdb_genre + "\n**Director:** " + omdb_director + "\n**Writer:** " + omdb_writer + "\n**Actor:** " + omdb_actor + "\n**Plot:** " + omdb_plot + "\n**Language:** " + omdb_language + "\n**Country:** " + omdb_country + "\n**Awards:** " + omdb_awards + "\n**Production:** " + omdb_production + "\n**Box Office:** " + omdb_boxoffice + "\n**Type:** " + omdb_type +"\n**IMDB ID:** " + imdb_id + "\n**IMDB ID 2**: " + omdb_id + "\n**Website:** " + omdb_website)


        except KeyError:

            yield from message.channel.send("No information for:** " + params[1] + "**")

    if command == "!releases":

        yield from message.channel.send("Retrieve information from PreDB Databases ... ")

        title_movie = params
        params.pop(0)

        for i in params:
            releases = ".".join(params)
        try:
            r=requests.get(url='https://www.srrdb.com/api/search/' + releases + '/order:date-desc/skip:5')
            data=r.json()

            if not data['results']:

                yield from message.channel.send("**" + releases +"** "+ "have no scene releases or check writing! ")

            else:
                yield from message.channel.send("**Last 5 releases for " + releases +": **\n ")
                for i in data['results']:

                    release = i['release']
                    yield from message.channel.send("```" + release + "```")

        except KeyError:

            yield from message.channel.send("No information for:** " + releases + "**")

    if command == "!help":
        yield from message.channel.send("```Markdown\n[1]: !pre [RELEASE TITLE]\n# Return pre information about release\n[2]:!file [RELEASE TITLE]\n# Return Layer13 link, nfo, sfv\n[3]: !nfo [RELEASE TITLE]\n# Search for nfo and if existe, return download link\n[4]: !size [RELEASE TITLE]\n# Return number of file and size of the release\n[5]: !group [GROUP/TAG NAME]\n# Return last 5 releases of this group/tag\n[6]: !imdb [RELEASE TITLE]\n# Retrieve information from IMDb\n[7]: !releases [TV/MOVIE TITLE]\n# Return last 5 release available for this Tv/Movie title```")
        yield from message.channel.send("```Markdown\nYou can have more informations on the official [Github repo](https://github.com/enzobes/WarezBot)```")
        yield from message.channel.send("https://github.com/enzobes/WarezBot")

client.run(token)

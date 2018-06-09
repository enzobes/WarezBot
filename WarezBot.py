# -*- coding: utf-8  -*-

import asyncio, discord
import requests
import datetime
import sys
import argparse



ap = argparse.ArgumentParser()
ap.add_argument("-k", "--key", required=True, help="Layer13 API KEY")
ap.add_argument("-b", "--bot", required=True, help="Discord Bot Token")
args = vars(ap.parse_args())
token = args["bot"]
apikey_layer13 = args["key"]
print(token)

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
    if type(message.server) is discord.server.Server:
        server_msg = str(message.channel.server)
        chan_msg = str(message.channel.name)
        for role_name in trust_roles:
            if ":" in role_name and role_name.split(":")[0] == server_msg:
                rank_role = discord.utils.get(message.server.roles, name = ":".join(role_name.split(":")[1:]))
            else:
                rank_role = discord.utils.get(message.server.roles, name = role_name)
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
        yield from client.send_message(message.channel, "Texte à envoyer.")
        yield from client.change_presence(game=discord.Game(name='Dev by SplitX26'))
    if "il est cool " + user_bot.lower() in rep.lower(): #Ici, le bot peut répondre a des phrases, par exemple, en disant "Il est cool NextBot", le bot répondra "Merci du compliment, vous aussi vous êtes cool !".
        yield from client.send_message(message.channel, "Merci du compliment, vous aussi vous êtes cool ! :)")
#Fin des commandes
#COMMANDES PERSO
    if command == "!pre":
        r=requests.get(url='http://api.layer13.net/v1/?getpre='+ params[1] +'&key='+ apikey_layer13)
        data=r.json()
        try:
            date = data['pretime']
        except KeyError:
            list_nfo = params[1].split("-")
            yield from client.send_message(message.channel, "**"+list_nfo[1]+"**" + " n'est pas une team scène !")
            return
        
        read_date = datetime.datetime.fromtimestamp(int(date)).strftime('%d-%m-%Y %H:%M:%S')
        yield from client.send_message(message.channel, "**ID:** " + data['id'] + "\n**Section:** "+ data['section']+ "\n**RlsName:** " + data['rlsname'] + "\n**Pretime:** " + data['pretime'] + "\n**Predate:**: " + read_date)
        
    if command == "!file":

        
        r=requests.get(url='http://api.layer13.net/v1/?listfiles='+ params[1] +'&key='+ apikey_layer13)
        r2=requests.get(url='http://api.layer13.net/v1/?getpre='+ params[1] +'&key='+ apikey_layer13)

        data=r.json()
        data2=r2.json()
        try:
            url = 'https://layer13.net/rls?id='+ data2['id']
        except KeyError:
            list_nfo = params[1].split("-")
            yield from client.send_message(message.channel, "**"+list_nfo[1]+"**" + " n'est pas une team scène !")
            return
        
        try:
            parsed_nfo = data['0']['filename']
            parsed_sfv = data['1']['filename']
            if parsed_nfo and parsed_sfv :
                yield from client.send_message(message.channel, "**Lien Layer13:** " + url +"\n**NFO:** " + parsed_nfo + "\n**SFV:** " + parsed_sfv)
        except KeyError:
            try:
                parsed_nfo = data['0']['filename']
                print(parsed_nfo)
                if parsed_nfo:
                    yield from client.send_message(message.channel, "**Lien Layer13:** " + url +"\n**NFO:** " + parsed_nfo)
                        
            except KeyError:
                yield from client.send_message(message.channel, "Pas de NFO pour:** " + params[1] + "**")
    
    if command == "!nfo":
        r=requests.get(url='http://api.layer13.net/v1/?listfiles='+ params[1] +'&key='+ apikey_layer13)
        r2=requests.get(url='http://api.layer13.net/v1/?getpre='+ params[1] +'&key='+ apikey_layer13)

        data=r.json()
        data2=r2.json()

        try:
            yield from client.send_message(message.channel,"Recherche sur Layer13 ...")   
            parsed_nfo = data['0']['filename']
            download='http://api.layer13.net/v1/?getfile=' + data2['id'] + "&filename=" + parsed_nfo + "&key=" + apikey_layer13



        except KeyError:

            yield from client.send_message(message.channel, "Pas de nfo sur Layer13 pour :" +"**" + params[1] + "**")
            try:
                yield from client.send_message(message.channel,"Recherche sur Srrdb ...")   
                r3=requests.get(url='https://www.srrdb.com/api/nfo/' +params[1])
                data3=r3.json()
                srrdb_nfo = data3['nfo']
                srrdb_nfo_link = data3['nfolink']
                print(srrdb_nfo_link)
                if data3['nfo']:
                    yield from client.send_message(message.channel,"**NFO Srrdb: **" + str(srrdb_nfo)) 
                    yield from client.send_message(message.channel,"**Download Srrdb: **" + str(srrdb_nfo_link)) 
                    return  

                if len(srrdb_nfo) > 0:
                    yield from client.send_message(message.channel,"Pas de nfo sur Srrdb pour:" + "**" + params[1] + "**")
                    return   
            except KeyError:
                yield from client.send_message(message.channel, "Pas de NFO pour:** " + params[1] + "**")
        try:    
            parsedValue = data['0']['filename']
            yield from client.send_message(message.channel, "NFO trouvé !" + "\n**Files:** " + parsedValue + "\n**Download Layer13**: " + download)

        except KeyError:
            yield from client.send_message(message.channel, "Pas de NFO pour:** " + params[1] + "**")

    if command == "!size":
        r=requests.get(url='http://api.layer13.net/v1/?getpre='+ params[1] +'&key='+ apikey_layer13)
        data=r.json()
        try:
            r2=requests.get(url='http://api.layer13.net/v1/?getfilessize='+ data['id'] +'&key='+ apikey_layer13)
        except KeyError:
            list_nfo = params[1].split("-")
            yield from client.send_message(message.channel, "**"+list_nfo[1]+"**" + " n'est pas une team scène !")
            return
        
        data2=r2.json()
        yield from client.send_message(message.channel, "**Files:** " + data2['files'] + "\n**Size:** "+ data2['size']+ " MB")

    if command == "!group":
        yield from client.send_message(message.channel, "I'm searching ... ")
        r=requests.get(url='https://www.srrdb.com/api/search/group:' +params[1] + '/order:date-desc/skip:1')
        data=r.json()
        print(data['results'])
        if not data['results']:

            yield from client.send_message(message.channel, "**" + params[1] +"** "+ "n'est pas une team scène !")

        else:
            release = data['results'][0]['release']
            yield from client.send_message(message.channel, "**Last release " + params[1] +": ** " + release)
#        no_team = params[1]
#        yield from client.send_message(message.channel, "**"+ no_team +"**" + " n'est pas une team scène !")

client.run(token)

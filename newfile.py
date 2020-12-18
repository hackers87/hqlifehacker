import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
import time
from datetime import datetime
from pytz import timezone
from lomond import WebSocket
from unidecode import unidecode
import colorama
import requests
import json
import re
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed
import aniso8601

webhook_url = "https://discordapp.com/api/webhooks/767205047473274890/gOxEmLADY61rbU3srWU4WQDaDFjmQDUSRqHW_KBPwNZwygji46cqY4BShVd19pqFubV_"

try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")
        

def show_not_on():
    colorama.init()
    # Set up logging
    logging.basicConfig(filename="data.log", level=logging.INFO, filemode="w")

    # Read in bearer token and user ID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e

    print("Getting")
    main_url = f"https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "x-hq-client": "Android/1.3.0"}
    # "x-hq-stk": "MQ==",
    # "Connection": "Keep-Alive",
    # "User-Agent": "okhttp/3.8.0"}

    try:
        response_data = requests.get(main_url).json()
    except:
        print("Server response not JSON, retrying...")
        time.sleep(5)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            
            print("Show not on")
            tim = (response_data["nextShowTime"])
            tm = aniso8601.parse_datetime(tim)
            x =  tm.strftime("%H:%M")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            x_in = x_ind.strftime("%d/%m/%Y")
            x_inn = x_ind.strftime("%H:%M")
    
            



def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    return response_data['active']


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()

    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
           # print(message_data)

            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']

                print(f"\nQuestion number {qcnt} out of {Fullcnt}\n{question}")
                answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                print(f"\n{answers[0]}\n{answers[1]}\n{answers[2]}\n")
                real_question = str(question).replace(" ","+")
                rn = str(question).replace("NOT"," ")
                real_not_plus = str(rn).replace(" ","+")
                rn1 = str(question).replace("not"," ")
                real_nt_plus1 = str(rn1).replace(" ","+")
                google_query = "https://google.com/search?q="+real_question
                option1=f"{answers[0]}"
                opl1 = option1.lower()
                option2=f"{answers[1]}"
                opl2 = option2.lower()
                option3=f"{answers[2]}"
                opl3 = option3.lower()
                op1 = str(option1).replace(" ","+")
                op2 = str(option2).replace(" ","+")
                op3 = str(option3).replace(" ","+")
                if "not" in question:
                	embed=discord.Embed(title=f"Question {qcnt} Of {Fullcnt}   **[NOT Question!]**",description=f"**[{question}]({google_query}**", color=0x00C4FF)
                	embed.add_field(name="**Option 1**",value=f"**[{answers[0]}]({google_query})**")
                	embed.add_field(name="**Option 2**", value=f"**[{answers[1]}]({google_query})**")
                	embed.add_field(name="**Option 3**", value=f"**[{answers[2]}]({google_query})**")
                	embed.set_footer(text=f"HQ Google")
                	hook.send(embed=embed)
                else:
                    embed=discord.Embed(title=f"Question {qcnt} Of {Fullcnt}",description=f"**[{question}]({google_query})**", color=0x00C4FF)
                    embed.add_field(name="**Option 1**",value=f"**[{answers[0]}]({google_query})**")
                    embed.add_field(name="**Option 2**", value=f"**[{answers[1]}]({google_query})**")
                    embed.add_field(name="**Option 3**", value=f"**[{answers[2]}]({google_query})**")
                    embed.set_footer(text=f"HQ Google")
                    hook.send(embed=embed)
                r = requests.get(f"http://www.google.com/search?q={real_question}").text.lower()
                countoption1 = r.count(opl1)
                countoption2 = r.count(opl2)
                countoption3 = r.count(opl3)
                maxcount = max(countoption1, countoption2, countoption3)
                mincount = min(countoption1, countoption2, countoption3)
                sumcount = countoption1+countoption2+countoption3
                if countoption1 == maxcount:
                         embed2=discord.Embed(title=f"",description=f"**Google Results!**", color=0x0048FF)
                         embed2.add_field(name="**• __Options__**",value=f"**1.{answers[0]}** `:` {countoption1} :white_check_mark:\n**2.{answers[1]}** `:` {countoption2}\n**3.{answers[2]}** `:` {countoption3}")
                         hook.send(embed=embed2)
                         hook.send("Discord")
                elif countoption2 == maxcount:
                         embed2=discord.Embed(title=f"",description=f"**Google Results!**", color=0x0048FF)
                         embed2.add_field(name="**• __Options__**",value=f"**1.{answers[0]}** `:` {countoption1}\n**2.{answers[1]}** `:` {countoption2} :white_check_mark:\n**3.{answers[2]}** `:` {countoption3}")
                         hook.send(embed=embed2)
                         hook.send("Discord")
                else:
	                    embed2=discord.Embed(title=f"",description=f"**Google Results!**", color=0x0048FF)
	                    embed2.add_field(name="**• __Options__**",value=f"**1.{answers[0]}** `:` {countoption1}\n**2.{answers[1]}** `:` {countoption2}\n**3.{answers[2]}** `:` {countoption3} :white_check_mark:")               
	                    hook.send(embed=embed2)
	                    hook.send("Discord")
                        

            elif message_data["type"] == "questionSummary":

                answer_counts = {}
                correct = ""
                for answer in message_data["answerCounts"]:
                    ans_str = unidecode(answer["answer"])

                    if answer["correct"]:
                        correct = ans_str
                advancing = message_data['advancingPlayersCount']
                eliminated = message_data['eliminatedPlayersCount']
                nextcheck = message_data['nextCheckpointIn']

                total = int(advancing) + int(eliminated)
                app = (advancing/total) * 100
                apr = round(app, 2)
                epp = (eliminated/total) * 100
                epr = round(epp, 2)

                print(colored(correct, "blue"))
                print(advancing)
                print(eliminated)
                embd=discord.Embed(title=f"Question {qcnt}/{Fullcnt}",description=f"[{question}]({google_query})",color=0xFF0400)
                embd.add_field(name="**Correct Answer :-**",value=f"{correct}")
                embd.add_field(name=f"**Stats :-**",value=f"**• Advancing Players :** {advancing}\n**• Eliminated Players :** {eliminated}",inline=True)
                hook.send(embed=embd)	         	

            elif message_data["type"] == "gameSummary":
                winn = message_data['numWinners']
                priz = str(message_data["winners"][0]['prize'])
                
                embed=discord.Embed(title=f"**Game Summary !**",description=f"**• Payout:** **{priz}**\n**• Total Winners:** **{winn}**\n**• Total Prize Money** : **$5000**",color=0x00FFB9)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/709231606430171196/715022507668799528/giphy.gif")
                embed.set_footer(text="HQ Google")
                hook.send(embed=embed)
                

def get_auth_token():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            auth_token = settings[0].split("=")[1]
        except IndexError:
            print('No Key is given!')
            return 'NONE'

        return auth_token


    while True:
        if show_active():
            url = get_socket_url()
            

            token = get_auth_token()
            if token == 'NONE':
                print('Please enter a valid auth token.')
            else:
                connect_websocket(url, token)

        else:
            show_not_on()
            time.sleep(300)
 
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e                       

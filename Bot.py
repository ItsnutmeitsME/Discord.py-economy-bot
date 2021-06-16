import discord
import random
import json
import os
from discord.ext import commands 
from discord.ext.commands import Bot
import math
import sys
os.chdir("Insert path file here")

client = commands.Bot(command_prefix = '!!')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="ur mom"))
    print("John James is ready")

#####error manegment#####
@client.event
async def on_command_error(ctx, error):
    await ctx.send("Incorrect command. this command does not exist or the formatting is wrong")

############## Member Count ####################
@client.command(aliases=["mc"])

async def member_count(ctx):

    a=ctx.guild.member_count
    b=discord.Embed(title=f"members in {ctx.guild.name}",description=a,color=discord.Color((0xffff00)))
    await ctx.send(embed=b)

##EPIC help command##
@client.command()
async def help(ctx):
    help_emb = discord.Embed(title = "Help", description = "Remember to add a !! before each command.", color = discord.Color.gold())
    help_emb.add_field(name = "Economy Commands ", value = "ask, withdraw, deposit, share, steal, shop, balance, buy ", inline = False )
    help_emb.add_field(name = "Version", value = "1.1")
    await ctx.send(embed = help_emb)

##BOT VERSION##
@client.command()
async def version(ctx):
    p_emb = discord.Embed(title = "Version", description = "1.4", color = discord.Color.gold())
    await ctx.send(embed = p_emb)
    
######################################  EcOnOmY bOt  #################################################


@client.command(aliases=['bal'])
async def balance(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    await open_account(member)

    users = await get_bank_data()

    wallet_amt = users[str(member.id)]["wallet"]
    bank_amt = users[str(member.id)]["bank"]

    embed=discord.Embed(title="{}s balance :coin: :".format(member.name), color=0xe20303)
    embed.add_field(name="Wallet:", value=wallet_amt, inline=False)
    embed.add_field(name="Bank:", value=bank_amt, inline=False)

    await ctx.send(embed=embed)

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("banky.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("banky.json", "r") as f:
        users = json.load(f)
    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("banky.json", "w") as f:
        json.dump(users, f)
    
    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]

    return bal





@client.command()
async def ask(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    amount = random.randrange(1, 300)
    await ctx.send(f"{random.choice(KOOL)} gave you {amount} :coin:'s !!")
    users[str(user.id)]['wallet'] += amount
    with open('banky.json', 'w') as f:
        json.dump(users, f)
        

@client.command(aliases=['with'])
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)


    if amount == None:
        await ctx.send("Please enter an amount NUMB NUT")
        return

    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("U don't have that much money NUMB NUT")
        return

    if amount<0:
        await ctx.send("-_- it must be a positive number u NUMB NUT")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author,-1*amount, "bank")

    await ctx.send(f"You withdrew {amount} :coin:s!")






@client.command(aliases=['dep'])
async def deposit(ctx, amount = None):
    await open_account(ctx.author)


    if amount == None:
        await ctx.send("Please enter an amount NUMB NUT")
        return

    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("U don't have that much money NUMB NUT")
        return

    if amount<0:
        await ctx.send("-_- it must be a positive number u NUMB NUT")
        return

    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount, "bank")

    await ctx.send(f"You deposited {amount} :coin:s!")


@client.command(aliases=['send', 'gift',])
async def share(ctx, member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Please enter an amount NUMB NUT")
        return

    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("U don't have that much money NUMB NUT")
        return

    if amount<0:
        await ctx.send("-_- it must be a positive number u NUMB NUT")
        return

    await update_bank(ctx.author,-1*amount,"wallet")
    await update_bank(member,amount, "wallet")

    await ctx.send(f"You gave {amount} :coin:s!")




@client.command
async def slots(ctx, amount = None):
    await open_account(ctx.author)


    if amount == None:
        await ctx.send("Please enter an amount NUMB NUT")
        return

    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    
    if amount>bal[0]:
        await ctx.send("-_-U don't have that much money NUMB NUT")
        return

    if amount<0:
        await ctx.send("-_- it must be a positive number u NUMB NUT")
        return

    final = []
    for i in range(3):
        a = random.choice(["A", "B", "C"])
        final.append(a)
    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
        await update_bank(ctx.author, 2*amount)
        await ctx.send("U won NUMB NUT")

    else:
        await update_bank(ctx.author, -1*amount)
        await ctx.send("U lost NUMB NUT")

    await ctx.send(f"You lost {amount} :coin:s!")




@client.command()
async def steal(ctx, member:discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member)

    if bal[0]<100:
        await ctx.send("Not worth it m8")
        return


    dolla = random.randrange(0,bal[0])


    await update_bank(ctx.author,dolla)
    await update_bank(member,-1*dolla)

    await ctx.send("You stole & got {} :coin:s!! :zany_face:".format(str(dolla)))




##shop##

mainshop = [{"name":"Xbox","price":100,"description":"gaming"},
            {"name":" doggo","price":100000,"description":"cute doggo"},
            {"name":"PC","price":10000,"description":"Gaming"}]


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)



@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command(aliases = ["inv"])
async def inventory(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)    
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")




##leaderboard for economy bot##

@client.command(aliases = ["lb", "phorbes"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "HAHA u guys are poor except dis guy",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)





@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there! NUMB NUT")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag. NUMB NUT")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag. NUMB NUT")
            return

    await ctx.send(f"You just sold {amount} {item}. ")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]
    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]





@client.command
async def coin(ctx, amount = None):
    await open_account(ctx.author)


    if amount == None:
        await ctx.send("Please enter an amount NUMB NUT")
        return

    
    bal = await update_bank(ctx.author)

    amount = int(amount)
    
    if amount>bal[0]:
        await ctx.send("U don't have that much money NUMB NUT")
        return

    if amount<0:
        await ctx.send("-_- it must be a positive number u NUMB NUT")
        return

    c = ["you won", "you lost"]
    final = []
    for i in range(3):
        a = random.choice(["Head", "Tail"])
        final.append(a)
    await ctx.send(str(final))

    if a == "Head":
        await ctx.send(a)

    if c == "you won":
        await update_bank(ctx.author, 2*amount)
        await ctx.send("U won NUMB NUT")
        await ctx.send(f"You won {amount} :coin:s!")


    else:
        await update_bank(ctx.author, -1*amount)
        await ctx.send("U lost NUMB NUT")

    await ctx.send(f"You lost {amount} :coin:s!")




##Code Runner##
client.run("insert bot token here")

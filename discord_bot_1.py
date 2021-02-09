import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import requests
import json
from datetime import datetime, date, time
import pickle
import random

settings = {
    'token': 'ODA0NDEzMjA1MzcxMTU4NTU4.YBL-LQ.rf5hahRSAfk20V3fgRqnKXfyHDA',
    'bot': 'Оркестр',
    'id': 804413205371158558,
    'prefix': '!'
}

bot = commands.Bot(command_prefix = settings['prefix'])
print('bot has been started!')

with open('data.pickle', 'rb') as f:
    customers= pickle.load(f)

with open('dataZarpl.pickle','rb') as f:
    zarplata = pickle.load(f)
print(zarplata)

dt = datetime.now()
tt = dt.timetuple()
n = dt.strftime("%A")
#customers = {'bot':12000,'bot2':90}
print(n)
if (n  == 'Friday' or n == 'Thursday') and zarplata == 0:
    print('ЗАРПЛАТА!!!!!!!')
    zarplata = 1
    with open('dataZarpl.pickle','wb') as f:
        pickle.dump(zarplata,f)

    for i in customers:
        customers[i] += 500
    with open('data.pickle.pickle','wb') as f:
        pickle.dump(customers,f)
if n == 'Sunday':
    zarplata = 0
    with open('dataZarpl.pickle','wb') as f:
        pickle.dump(zarplata,f)
    #with open('data.pickle','wb') as f:
        #pickle.dump(zarplata,f)
@bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def hello(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Привет, {author.mention}!') # Выводим сообщение с упоминанием автора, обращаясь к переменной author.

@bot.command()
async def get_slot(ctx):
    author2 = ctx.message.author
    author = ctx.message.author.name
    global customers
    if author in customers:
        await ctx.send(f'{author2.mention}, у тебя уже есть банковский счёт!')
    else:

        money = {author:500}
        customers.update(money)
        # сохранение в файл
        with open('data.pickle', 'wb') as f:
            pickle.dump(customers, f)
        print(f'money_slot for {author} was created')
        await ctx.send(f'Готово! На вашем счету 500 рублей')

@bot.command()
async def all_slots(ctx):
    author = ctx.message.author
    embed = discord.Embed(color = 0xff9900, title = 'Все банковские счета.', description = f'{customers}') # Создание Embed'a
    await ctx.send(embed = embed) # Отправляем Embed
    print(f'user {author} asked for all slots')

@bot.command()
async def my_slot(ctx):
    
    author = ctx.message.author
    authorIndex = ctx.message.author.name
    try:
        print(f'User {author} calling for its money_slot')
        embed = discord.Embed(color = 0xff9900, title = 'Ваш счёт.', description = f'{author.mention}, на вашем счету {customers[authorIndex]} рублей') # Создание Embed'a
        await ctx.send(embed = embed) # Отправляем Embed
    except:
        embed = discord.Embed(color = 0xff0000, title = 'Ошибка!', description = f'{author.mention}, у вас нет банковского счета! Чтобы получить его, пропишите команду "$get_slot" ')
        await ctx.send(embed = embed)
@bot.command()
async def give(ctx,name,col):

    global customers
    author = ctx.message.author.name
    try:
        if customers[author] < int(col):
            embed = discord.Embed(color = 0xff0000, title = 'Ошибка!', description = 'Невозможно перевести средства. На вашем счету не достаточно средств для осуществления платежа!') # Создание Embed'a
            await ctx.send(embed = embed)
            print(f'Fail! user {author} can`t add money to user {name}')
        customers[name] += int(col)
        embed = discord.Embed(color = 0x31FF00, title = 'Готово!', description = f'На счёт пользователя {name} перечисленно {col} рублей') # Создание Embed'a
        await ctx.send(embed = embed)
        customers[author] -= int(col)
        
        with open('data.pickle', 'wb') as f:
            pickle.dump(customers, f)
            
        print(f'user {author} added {col} money to user {name}!')
        
    except:
        embed = discord.Embed(color = 0xff0000, title = 'Ошибка!', description = f'Не удалось перевести средства.Возможно у Вас или у пользователя {name} отсутствует банковский счёт, или пользователя {name} не существует.')
        await ctx.send(embed = embed)
        print(f'Fail! user {author} can`t add money to user {name}')

@bot.command()
async def get(ctx,col):
    global customers
    author = ctx.message.author.name
    customers[author] += int(col)
    print(f'Added {col} money to user {author}!')
    await ctx.send(f'Готово! На Ваш щёт переведено {col} рублей')

@bot.command()
async def программист(ctx):
    author = ctx.message.author
    await ctx.send(f'Поздравляю, {author.mention}! Вы открыли секретную команду!')
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

@bot.command()
async def лотерея(ctx):
    author = ctx.message.author
    aindex = ctx.message.author.name
    r = random.randint(0,100)
    if customers[aindex] >= 50:
        customers[aindex] -= 50
        mrand = random.randint(0,3)
        if mrand == 0:
            mes = 'Вы проиграли!'
        elif mrand == 1:
            mes = 'Не в этот раз'
        elif mrand == 2:
            mes = 'Не повезло'
        elif mrand == 3:
            mes = 'Повезёт в следующий раз'
        if r == 0:
            embed = discord.Embed(color = 0x31ff00, title = 'Поздравляю!' , description = f'{author.mention}! Вы потратили 50 монет, но выйграли 10000!')
            await ctx.send(embed=embed)
            await ctx.send('https://www.youtube.com/watch?v=4iDiSXAe7zI')
            customers[aindex] += 10000
        else:
            embed = discord.Embed(color = 0xff0000, title = mes, description = f'{author.mention}! Вы потратили 50 монет, и ничего не выйграли :-(')
            await ctx.send(embed=embed)
        with open('data.pickle','wb') as f:
            pickle.dump(customers,f)
    else:
        embed = discord.Embed(color = 0xff0000, title = 'Ошибка', description = 'На вашем счёте не хватает средств для оплаты билета')
        await ctx.send(embed = embed)
@bot.command()
async def cat(ctx):
    author = ctx.message.author
    response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Кот. Просто кот.') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed
    print(f'User {author} called cat`s picture')

@bot.command()
async def flex(ctx):
    await ctx.send(f'Внимание! Произошли технические шоколадки. Оставайтесь на линии')
    await ctx.send('https://www.youtube.com/watch?v=4iDiSXAe7zI')

bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена

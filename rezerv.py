import random
from itertools import *
from urllib.parse import quote_plus as quote
import pymongo
from random import randint


def handler(event, context):
    konec = ['не хочу играть', 'давай закнчим', 'закрой игру', 'я наигрался', 'выход']
    poka = ['Жду вас снова', 'До встречи)']
    ne_pon = ['Извините, я вас не понмаю', 'Повторите еще раз', 'Повторите пожалуйста']
    frazi = ['Что ж, а я возьму', 'Тогда я возьму', 'Дайте подумать, возьму', 'Беру', 'Ну тогда я беру']
    end = 'false'
    text = []

    class Player:
        def __init__(self, stone, plus, minus):
            self.stone = stone
            self.action_1 = plus
            self.action_2 = minus

        def sum(self):
            self.stone += self.action_1
            collektion.find_one_and_update({'name': 'Alisa'}, {"$set": {"user_stone": f"{self.stone}"}})

        def diff(self):
            self.stone -= self.action_2
            collektion.find_one_and_update({'name': 'Alisa'}, {"$set": {"user_stone": f"{self.stone}"}})

        def is_count(self):
            return str(self.stone) in list(collektion.find())[0].get('win').split("~")

    class Alice:
        def __init__(self, stone, plus, minus):
            self.stone = stone
            self.action_1 = plus
            self.action_2 = minus

        def sum(self):
            self.stone += self.action_1
            collektion.find_one_and_update({'name': 'Alisa'}, {"$set": {"alice_stone": f"{self.stone}"}})

        def diff(self):
            self.stone -= self.action_2
            collektion.find_one_and_update({'name': 'Alisa'}, {"$set": {"alice_stone": f"{self.stone}"}})

        def is_count(self):
            return str(self.stone) in list(collektion.find())[0].get('win').split("~")

        def variants(self, koleno):
            variants_spis = []
            for kol in range(koleno):
                var = []
                com_set = product('01', repeat=kol)
                for i in com_set:
                    var.append(list(i))
                for i in var:
                    start_new = self.stone
                    for j in i:
                        if int(j) == 0:
                            start_new -= self.action_2
                        elif int(j) == 1:
                            start_new += self.action_1
                        if start_new < 0:
                            break
                    if (start_new == count_1) or (start_new == count_2) or (start_new == count_3):
                        variants_spis.append(i)
            return variants_spis

    CERTIFICATE_PATH = "CA.pem"

    MONGO_DB_URI_FOR_CLIENT = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
        user=quote('user'),
        pw=quote('pw'),
        hosts=','.join([
            ''
        ]),
        rs='rs',
        auth_src='db')

    client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT, tlsCAFile=CERTIFICATE_PATH)
    db = client['db1']
    collektion = db['123']

    if event['request']['command'] in konec:
        end = 'true'
        text.append(poka[randint(0, len(poka))])
        collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{0}"}})
    elif event['request']['command'] == 'помощь':
        text.append(
            'В этом навыке можно поиграть в разные игры с камушками.\nДля того что бы выбрать игру, вам нужно сказать меню.\nЕсли вы хотите перезапустить игру, то вам нужно сказать рестарт.\nКогда надоест играть, просто скажите выход.')
    else:
        if event['request']['command'] == 'рандом' and list(collektion.find())[1].get('game') == '0':
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{0.5}"}})

        if event['request']['command'] == 'ним' and list(collektion.find())[1].get('game') == '0':
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1.5}"}})

        if event['request']['command'] == 'рестарт' and list(collektion.find())[1].get('game') in ['2.1', '2.3']:
            text.append('Новая игра\n')
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{2}"}})

        if event['request']['command'] == 'рестарт' and list(collektion.find())[1].get('game') in ['1.1', '1.3']:
            text.append('Новая игра\n')
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1}"}})

        if event['session']['new']:
            text.append(
                'В этом навыке можно поиграть в разные игры с камушками.\nДля того что бы выбрать игру, вам нужно сказать меню.\nЕсли вы хотите перезапустить игру, то вам нужно сказать рестарт.\nКогда надоест играть, просто скажите выход.')
            text.append("Какая игра?\nРандом или Ним")

        if event['request']['command'] == 'меню':
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{0}"}})
            text.append("Какая игра?\nРандом или Ним")

        if list(collektion.find())[1].get('game') == '1.5':
            text.append("Вы помните правила?")
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1.6}"}})
        if list(collektion.find())[1].get('game') == '1.6' and event['request']['command'] in ['да', 'конечно',
                                                                                               'еще бы', 'помню']:
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{2}"}})
            text.append('Удачной игры')
        elif list(collektion.find())[1].get('game') == '1.6' and event['request']['command'] in ['нет', 'неа',
                                                                                                 'не помню']:
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{2}"}})
            text.append('Другие Правила..........')

        if list(collektion.find())[1].get('game') == '0.5':
            text.append("Вы помните правила?")
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{0.6}"}})

        if list(collektion.find())[1].get('game') == '0.6' and event['request']['command'] in ['да', 'конечно',
                                                                                               'еще бы', 'помню']:
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1}"}})
            text.append('Удачной игры')
        elif list(collektion.find())[1].get('game') == '0.6' and event['request']['command'] in ['нет', 'неа',
                                                                                                 'не помню']:
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1}"}})
            text.append('Правила...................')

        if list(collektion.find())[1].get('game') == '2':
            collektion.find_one_and_update({'name': 'tree_stone'}, {"$set": {"count": f"{randint(10, 25)}"}})
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{2.1}"}})
            a = list(collektion.find())[2].get('count')
            text.append(f'Камней всего {a}')
            text.append('Сколько камней вы хотите взять?')
        elif list(collektion.find())[1].get('game') == '2.3':
            text.append("Пожалуйста, перезапустите игру командом рестарт.")
        elif list(collektion.find())[1].get('game') == '2.1':
            try:
                fr = frazi[randint(0, len(frazi))]
                count = int(list(collektion.find())[2].get('count'))
                command = event['request']['command'].split()
                chislo = 'f'
                for i in range(len(command)):
                    if command[i].isdigit():
                        chislo = int(command[i])

                if ((chislo <= 0) or (chislo > 3) or ((count - chislo) < 0)):
                    text.append('Пожалуйста, укажите корректное количество камней')
                else:
                    count -= chislo
                    collektion.find_one_and_update({'name': 'tree_stone'}, {"$set": {"count": f"{count}"}})
                    if count == 0:
                        text.append('Поздравляю, вы победили!\nЕсли хотите сыграть еще раз или перезапустить игру, скажите заново.')
                        collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{2.3}"}})
                    elif count <= 3:
                        if count == 1:
                            text.append(f'{fr} {count} камень')
                        else:
                            text.append(f'{fr} {count} камня')
                        count -= count
                        collektion.find_one_and_update({'name': 'tree_stone'}, {"$set": {"count": f"{count}"}})
                        text.append(
                            'Ура, я победила!\nЕсли хотите сыграть еще раз или перезапустить игру, скажите заново.')
                        collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{2.3}"}})
                    else:
                        alice_step = randint(1, 3)
                        if (count - 3) <= 3:
                            alice_step = 1
                        if count > 3:
                            if alice_step == 1:
                                text.append(f'{fr} {alice_step} камень')
                            else:
                                text.append(f'{fr} {alice_step} камня')
                            count -= alice_step
                            collektion.find_one_and_update({'name': 'tree_stone'}, {"$set": {"count": f"{count}"}})
                            text.append(f'Количество камней в кучке: {count}')
                            text.append('Сколько камней вы хотите взять?')
            except:
                text.append(ne_pon[randint(0, len(ne_pon))])

        if list(collektion.find())[1].get('game') == '1':
            collektion.find_one_and_update({'name': 'Alisa'}, {"$set": {"plus": f"0",
                                                                        "minus": f'0',
                                                                        "minus": f'{0}',
                                                                        'alice_stone': f'{0}',
                                                                        'user_stone': f'{0}',
                                                                        'path': f"{0}",
                                                                        'win': f"{0}"}})

            count_1, count_2, count_3 = random.randrange(20, 24), random.randrange(24, 27), random.randrange(27, 31)
            lst = [count_1, count_2, count_3]

            alice_stone = random.randrange(1, 10)
            user_stone = random.randrange(1, 10)
            if (user_stone == alice_stone) and (user_stone > 1):
                user_stone -= 1
            elif (user_stone == alice_stone) and (user_stone == 1):
                user_stone += 1

            numbers_1 = [3, 5, 7]
            numbers_2 = [2, 4, 6]
            action_1 = random.choice(numbers_1)
            action_2 = random.choice(numbers_2)

            text.append(f'Количество камней, необходимое для победы: {lst[0]} или {lst[1]} или {lst[2]}')
            text.append(f'Количество камней в моей кучке: {alice_stone}\nВ вашей кучке: {user_stone}')
            text.append(f'Команды:\n1) Прибавить {action_1}\n2) Вычесть {action_2}')

            var = Alice(alice_stone, action_1, action_2).variants(15)

            collektion.find_one_and_update({'name': 'Alisa'}, {"$set": {"plus": f"{action_1}",
                                                                        "minus": f'{action_2}',
                                                                        'alice_stone': f'{alice_stone}',
                                                                        'user_stone': f'{user_stone}',
                                                                        'path': f"{''.join(var[0])}",
                                                                        'win': f"{'~'.join(list(map(str, lst)))}"}})
            collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1.1}"}})
        elif list(collektion.find())[1].get('game') == '1.3':
            text.append("Пожалуйста, перезапустите игру командом рестарт.")
        elif list(collektion.find())[1].get('game') == '1.1':
            if event['request']['command'] in ['прибавить', 'вычесть']:
                player = Player(int(list(collektion.find())[0].get('user_stone')),
                                int(list(collektion.find())[0].get('plus')),
                                int(list(collektion.find())[0].get('minus')))
                alisa = Alice(int(list(collektion.find())[0].get('alice_stone')),
                              int(list(collektion.find())[0].get('plus')),
                              int(list(collektion.find())[0].get('minus')))

                path = list(list(collektion.find())[0].get('path'))
                command = event['request']['command']
                if command == 'прибавить':
                    player.sum()
                elif command == 'вычесть':
                    player.diff()
                if path:
                    if int(path[0]) == 0:
                        alisa.diff()
                    elif int(path[0]) == 1:
                        alisa.sum()
                    del path[0]
                    collektion.find_one_and_update({'name': 'Alisa'}, {"$set": {"path": f"{''.join(path)}"}})

                al_stone = list(collektion.find())[0].get('alice_stone')
                pl_stone = list(collektion.find())[0].get('user_stone')
                if alisa.is_count() == 'true' and player.is_count() == 'true':
                    text.append(f'Количество камней в моей кучке: {al_stone}\nВ вашей кучке: {pl_stone}')
                    text.append('\nНичья')
                    text.append('\nЕсли хотите сыграть еще раз или перезапустить игру, скажите рестарт.')
                    collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1.3}"}})
                elif alisa.is_count():
                    text.append(f'Количество камней в моей кучке: {al_stone}\nВ вашей кучке: {pl_stone}')
                    text.append('УРААА Я ПОБЕДИЛА!')
                    text.append('\nЕсли хотите сыграть еще раз или перезапустить игру, скажите рестарт.')
                    collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1.3}"}})
                elif player.is_count():
                    text.append(f'Количество камней в моей кучке: {al_stone}\nВ вашей кучке: {pl_stone}')
                    text.append('Поздравляю, вы победили!')
                    text.append('\nЕсли хотите сыграть еще раз или перезапустить игру, скажите рестарт.')
                    collektion.find_one_and_update({'name': 'main'}, {"$set": {"game": f"{1.3}"}})
                else:
                    text.append(f'Количество камней в моей кучке: {al_stone}\nВ вашей кучке: {pl_stone}')
            else:
                text.append(ne_pon[randint(0, len(ne_pon))])

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': '\n'.join(text),
            'end_session': end
        },
    }
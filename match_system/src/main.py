#! /usr/bin/env python3

import glob
import sys
sys.path.insert(0, glob.glob('../../')[0])

from match_server.match_service import Match

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from queue import Queue
from time import sleep
from threading import Thread

from acapp.asgi import channel_layer  # 这个是用于引用wss的channle函数
from asgiref.sync import async_to_sync  # 由于wss的函数大多都是并行函数,即多线程,而我们下面都是单线程函数,因此这里将多线程改为单线程
from django.core.cache import cache  # 将匹配成功的信息存入redis

queue = Queue()  # 消息队列


class Player:
    def __init__(self, score, uuid, username, photo, channel_name):
        self.score = score
        self.uuid = uuid
        self.username = username
        self.photo = photo
        self.channel_name = channel_name
        self.waiting_time = 0  # 等待时间


class Pool:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        print("add %s %d" % (player.username, player.score))
        self.players.append(player)

    def check_match(self, a, b):
        dt = abs(a.score - b.score)
        a_max_dif = a.waiting_time * 50
        b_max_dif = b.waiting_time * 50
        return dt <= a_max_dif and dt <= b_max_dif

    def match_success(self, ps):
        print("Match Success: %s %s %s" % (ps[0].username, ps[1].username, ps[2].username))
        room_name = "room-%s-%s-%s" % (ps[0].uuid, ps[1].uuid, ps[2].uuid)
        players = []
        for p in ps:
            async_to_sync(channel_layer.group_add)(room_name, p.channel_name)  # 这里实现了进程与进程间的通信,调用了wss的广播信息
            players.append({
                'uuid': p.uuid,
                'username': p.username,
                'photo': p.photo,
                'hp': 100,
            })
        cache.set(room_name, players, 3600)  # 将数据存到redis里,有效时间一个小时
        for p in ps:
            async_to_sync(channel_layer.group_send) (
                room_name,
                {
                    'type': "group_send_event",
                    'event': "create_player",
                    'uuid': p.uuid,
                    'username': p.username,
                    'photo': p.photo,
                }
            )

    def increase_waiting_time(self):
        for player in self.players:
            player.waiting_time += 1

    def match(self):
        while len(self.players) >= 3:
            self.players = sorted(self.players, key=lambda p: p.score)
            flag = False
            for i in range(len(self.players) - 2):
                a, b, c = self.players[i], self.players[i + 1], self.players[i + 2]
                if self .check_match(a, b) and self.check_match(a, c) and self.check_match(b, c):
                    self.match_success([a, b, c])
                    self.players = self.players[:i] + self.players[i + 3:]
                    flag = True
                    break
            if not flag:
                break

        self.increase_waiting_time()


class MatchHandler:
    def add_player(self, score, uuid, username, photo, channel_name):
        print("Add: %s %d" % (username, score))
        player = Player(score, uuid, username, photo, channel_name)
        queue.put(player)
        return 0  # 一定要return 0


def get_player_from_queue():
    try:
        return queue.get_nowait()
    except:
        return None


def worker():
    pool = Pool()
    while True:
        player = get_player_from_queue()
        if player:
            pool.add_player(player)
        else:
            pool.match()
            sleep(1)
# 这里是利用了match停止的1秒,把队列里所有数据"无阻塞的"加入


if __name__ == '__main__':
    handler = MatchHandler()
    processor = Match.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(
         processor, transport, tfactory, pfactory)  # 这个是多线程版,来一个数据开一个进程,并行度最高

    # You could do one of these for a multithreaded server
    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)  这个单线程版,效率低
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)  这个是n线程版,限定线程,超出阻塞

    Thread(target=worker, daemon=True).start()  # 开一个线程

    print('Starting the server...')
    server.serve()  # 开始死循环
    print('done.')

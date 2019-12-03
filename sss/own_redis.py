#! -*- coding:utf-8 -*-
import redis





if __name__ == '__main__':

    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    r.set('name', 'test')
    result = r.get('name')
    print(result)
    print('success')
    exit()
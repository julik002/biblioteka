#!/usr/bin/env python3
# coding:utf-8
import sqlite3


def bd_connect():
    cn = sqlite3.connect('data/БД университетская библиотека.db')
    return cn


class Constants:
    MAX = True

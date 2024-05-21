#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:20:30 2024

@author: chohi
"""

from durable.lang import *

with ruleset('SystemInspection'):
        
    @when_all((m.predicate == '웹서버') & (m.object == '500에러'))
    def check1(c):
        c.assert_fact({'subject' : c.m.subject, 'predicate': '웹서버', 'object': '로그 확인한다.'})
        
    @when_all((m.predicate == '웹서버') & (m.object == '접속오류'))
    def check2(c):
        c.assert_fact({'subject' : c.m.subject, 'predicate': '웹서버', 'object': '디스크 사용량 확인'})
        
    @when_all((m.predicate == '웹서버') & (m.object == '서비스오류'))
    def check3(c):
        c.assert_fact({'subject' : c.m.subject, 'predicate': 'is', 'object': 'mod_jk 확인'})
        
    @when_all(+m.subject)   # m.subject가 한번 이상
    def output(c):
        print('Fact: {0} {1} {2}'.format(c.m.subject, c.m.predicate, c.m.object))
        


assert_fact('SystemInspection', { 'subject': '대민서비스', 'predicate': '웹서버', 'object': '500에러' })








        
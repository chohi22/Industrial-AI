#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
산업인지능 개론

Mini Project #1 Rule-based System 만들기
자신의 현업에서 특정 분야의 문제에 대해 15개 이상의 규칙을 찾아서 Durable_Rules 로 구현

학번 : 2024254022
이름 : 정현일


@author: chohi
"""

from durable.lang import *


with ruleset('Inspection'):
    @when_all((m.predicate == '웹서버') & (m.error == '500에러'))
    def check1(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '웹서버', 'error': '로그 확인한다.' })
		
    @when_all((m.predicate == '웹서버') & (m.error == '접속오류'))
    def check2(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '웹서버', 'error': '디스크 사용량 확인' })

    @when_all((m.predicate == '웹서버') & (m.error == '서비스오류'))
    def check3(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '웹서버', 'error': 'mod_jk 확인' })

    @when_all((m.predicate == 'WAS서버') & (m.error == '서비스오류'))
    def check4(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'WAS서버', 'error': '로그확인' })

    @when_all((m.predicate == 'WAS서버') & (m.error == 'headpdump'))
    def check5(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'WAS서버', 'error': '메모리 사용량 확인' })

    @when_all((m.predicate == 'WAS서버') & (m.error == '서비스느림'))
    def check6(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'WAS서버', 'error': 'CPU 사용량 확인' })

    @when_all((m.predicate == 'DB서버') & (m.error == '접속오류'))
    def check7(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'DB서버', 'error': '로그 확인' })

    @when_all((m.predicate == 'DB서버') & (m.error == '속도느림'))
    def check8(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'DB서버', 'error': 'SQL Hint 확인' })
		
    @when_all((m.predicate == 'DB서버') & (m.error == '서비스오류'))
    def check9(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'DB서버', 'error': 'DB세션 로그 확인' })

    @when_all((m.predicate == '서비스장애') & (m.error == '웹서버'))
    def check10(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '서비스장애', 'error': '웹서버 장애확인' })

    @when_all((m.predicate == '서비스장애') & (m.error == 'WAS서버'))
    def check11(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '서비스장애', 'error': 'was서버 장애확인'})

    @when_all((m.predicate == '서비스장애') & (m.error == 'DB서버'))
    def check12(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '서비스장애', 'error': 'db서버 장애확인'})

    @when_all((m.predicate == '방화벽') & (m.error == '내부망'))
    def check13(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '방화벽', 'error': '내부망 방화벽 확인' })

    @when_all((m.predicate == '방화벽') & (m.error == '외부망'))
    def check14(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '방화벽', 'error': '외부망 방화벽 확인' })
		
    @when_all((m.predicate == '방화벽') & (m.error == '접속안됨'))
    def check15(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': '방화벽', 'error': '아이피 확인' })        
    @when_all(+m.subject)   # m.subject와 operation 한번 이상
    def output(c):
        print('Fact: {0} {1} {2}'.format(c.m.subject, c.m.predicate, c.m.error))


assert_fact('Inspection', { 'subject': '대민서비스', 'predicate': '웹서버', 'error': '서비스오류' }) 
assert_fact('Inspection', { 'subject': '내부서비스', 'predicate': '웹서버', 'error': '접속오류' })
assert_fact('Inspection', { 'subject': '대민서비스', 'predicate': 'WAS서버', 'error': 'headpdump' })
assert_fact('Inspection', { 'subject': '내부서비스', 'predicate': '방화벽', 'error': '내부망' })


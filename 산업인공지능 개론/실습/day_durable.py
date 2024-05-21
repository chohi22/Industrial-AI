#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:20:30 2024

@author: chohi
"""

from durable.lang import *

with ruleset('animal'):
    @when_all(c.first << (m.predicate == 'eats') & (m.object == 'files'),   # << 해당 조건ㅇㄹ 만족하는 대상 지시하는 이름
              (m.predicate == 'lives') & (m.object == 'water') & (m.subject == c.first.subject))
    def frag(c):
        c.assert_fact({'subject' : c.first.subject, 'predicate': 'is', 'object': 'frog'})
        # 사실(fact)의 추가
        
    @when_all(c.first << (m.predicate == 'eats') & (m.object == 'files'),
              (m.predicate == 'lives') & (m.object == 'land') & (m.subject == c.first.subject))
    def chameleon(c):
        c.assert_fact({'subject' : c.first.subject, 'predicate': 'is', 'object': 'chameleon'})
                       
    @when_all((m.predicate == 'eats') & (m.object == 'worms'))
    def bird(c):
        c.assert_fact({'subject' : c.m.subject, 'predicate': 'is', 'objet': 'bird'})
        
    @when_all((m.predicate == 'is') & (m.object == 'frag'))
    def green(c):
        c.assert_fact({'subject' : c.m.subject, 'predicate': 'is', 'object': 'green'})
        
    @when_all((m.predicate == 'is') & (m.object == 'chameleon'))
    def grey(c):
        c.assert_fact({'subject' : c.m.subject, 'predicate': 'is', 'object': 'grey'})
        
    @when_all((m.predicate == 'is') & (m.object == 'bird'))
    def black(c):
        c.assert_fact({'subject' : c.m.subject, 'predicate': 'is', 'object': 'black'})
        
    @when_all(+m.subject)   # m.subject가 한번 이상
    def output(c):
        print('Fact: {0} {1} {2}'.format(c.m.subject, c.m.predicate, c.m.object))
        
assert_fact('animal', {'subject' : 'Kermit', 'predicate' : 'eats', 'object' : 'files'})
assert_fact('animal', {'subject' : 'Kermit', 'predicate' : 'lives', 'object' : 'water'})
#assert_fact('animal', {'subject' : 'Greedy', 'predicate' : 'eats', 'object' : 'files'})
#assert_fact('animal', {'subject' : 'Greedy', 'predicate' : 'lives', 'object' : 'land'})
#assert_fact('animal', {'subject' : 'Tweety', 'predicate' : 'eats', 'object' : 'worms'})






        
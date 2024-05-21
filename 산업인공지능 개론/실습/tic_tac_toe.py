#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
산업인지능 개론

HW1
tic-tac-toe에 Monte Carlo Tree Search를 적용한 프로그램을 직접 실행해 보고 결과 화면을 올리기

학번 : 2024254022
이름 : 정현일


Created on Tue Mar 12 09:16:59 2024

@author: chohi
"""

from collections import namedtuple
from random import choice
from monte_carlo_tree_search import MCTS, Node

TTTB = namedtuple("TicTacToeBoard", "tup turn winner terminal")

class TicTacToeBoard(TTTB, Node):   # TTTB의 속성등ㄹ도 상속
    def find_children(board):   # 전체 가능한 move들 집합으로 반환
        if board.terminal:      # 게임이 끝나면 아무것도 하지 않음
            return set() 
        return { # 그렇지 않으면, 비어있는 곳에서 각각 시도
            board.make_move(i) for i, value in enumerate(board.tup) if value is None        
        }

    def find_random_child(board):   # 무작위로 move 선택
        if board.terminal:
            return Node     # 게임이 끝나면 아무것도 하지 않음
        empty_sports = [i for i, value in enumerate(board.tup) if value is None]
        return board.make_move(choice(empty_sports))
    
    def reward(board):  # 점수 계산
        if not board.terminal:
            raise RuntimeError(f"reward clled on nonterminal board {board}")
        if board.winner is board.turn:
            # 자기 차례이면서 자기가 이긴 상황은 불가능
            raise RuntimeError(f"reward called on unreacheable board {board}")
        if board.turn is (not board.winner):
            return 0    # 상ㅌ대가 이긴 상황
        if board.winner is None:
            return 0.5  # 비긴 상황
        # 일어날 수 없는 상황
        raise RuntimeError(f"board has unknown winner type {board.winner}")
        
    def is_terminal(board): # 게임 종료 여부
        return board.terminal
    
    def make_move(board, index):    # index 위치에 board.turn 표시하기 하기
        tup = board.tup[:index] + (board.turn,) + board.tup[index + 1 :]
        turn = not board.turn   # 순서 바꾸기
        winner = find_winner(tup)   # 승자 또는 미종료 판단
        is_terminal = (winner is not None) or not any(v is None for v in tup)
        return TicTacToeBoard(tup, turn, winner, is_terminal) # 보드 상태 반환
    
    def display_board(board):   # 보드 상태 출력
        to_char = lambda v: ("x" if v is True else ("0" if v is False else " "))
        rows = [
            [to_char(board.tup[3 * row + col]) for col in range(3)] for row in range(3)
            ]
        return ("\n  1 2 3\n" + "\n".join(str(i+1) + " " + " ".join(row) 
                                          for i, row in enumerate(rows)) + "\n")
    
def play_game():    # 게임하기
    tree = MCTS()
    board = new_Board()
    print(board.display_board())
    while True:
        row_col = input("위치 row, col: ")
        row, col = map(int, row_col.split(","))
        index = 3 * (row - 1) + (col - 1)
        if board.tup[index] is not None:    # 비어있는 위치가 아닌 경우
            raise RuntimeError("Invalid move")
        
        board = board.make_move(index)  # index 위치의 보드 상태 변경
        print(board.display_board())
        if board.terminal:  # 게임 종료
            break
        
        for _ in range(50): # 매번 50번의 rollout을 수행
            tree.do_rollout(board)
        board = tree.choose(board) # 최선의 값을 갖는 move 선택하여 보드에 반영
        print(board.display_board())
        if board.terminal:
            print("게임 종료")
            break
        
def winning_combos():   # 이기는 배치 조합
    for start in range(0, 9, 3):    # 행에 3개 연속
        yield(start, start + 1, start + 2)
    for start in range(3):  # 열에 3개 연속
        yield(start, start + 3, start + 6)
    yield(0, 4, 8) # 오른쪽 아래로 가는 대각선 3개
    yield(2, 4, 6) # 왼쪽 아래로 가는 대각선 3개
    

def find_winner(tup):   # X가 이기면 True, 0가 이기면 False, 미종료 상태이면 None 반환
    for i1, i2, i3 in winning_combos():
        v1, v2, v3 = tup[i1], tup[i2], tup[i3]
        if False is v1 is v2 is v3:
            return False
        if True is v1 is v2 is v3:
            return True
    return None
            

def new_Board(): # 비어있는 보다판 생성
    return TicTacToeBoard(tup=(None,) * 9, turn=True, winner=None, terminal=False)

if __name__ == "__main__":
    play_game()
# 빼기, 곱하기, 나누기 함수를 구현하는 Python 코드

def subtract(a, b):
    """빼기 함수: a에서 b를 뺍니다."""
    return a - b


def multiply(a, b):
    """곱하기 함수: a와 b를 곱합니다."""
    return a * b


def divide(a, b):
    """나누기 함수: a를 b로 나눕니다. (b가 0이 아니어야 함)"""
    if b == 0:
        return "0으로 나눌 수 없습니다."
    return a / b


if __name__ == '__main__':
    # 테스트 함수
    a = 10
    b = 5

    print(f"{a} - {b} = {subtract(a, b)}")
    print(f"{a} * {b} = {multiply(a, b)}")
    print(f"{a} / {b} = {divide(a, b)}")
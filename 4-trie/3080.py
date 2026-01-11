from lib import Trie
import sys


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    lines = sys.stdin.readlines()
    i = 0
    while i < len(lines):
        n = int(lines[i].strip())
        i += 1
        
        messages = []
        for j in range(n):
            messages.append(lines[i + j].strip())
        i += n
        
        # Trie 생성 (문자를 bytes로 변환하여 메모리 절약)
        trie: Trie[int] = Trie()
        for msg in messages:
            trie.push(msg.encode())  # str을 bytes로 변환
        
        # 결과 계산 및 출력
        # (문제에 따라 추가 구현 필요)
        print()


if __name__ == "__main__":
    main()
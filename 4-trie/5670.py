from lib import Trie
import sys


"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        # 현재 노드의 children에서 body == element인 노드 찾기
        new_index: int | None = None
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break

        if new_index is not None:
            pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    lines = sys.stdin.readlines()
    i = 0
    while i < len(lines):
        n = int(lines[i].strip())
        i += 1
        
        words = []
        for j in range(n):
            words.append(lines[i + j].strip())
        i += n
        
        # Trie 생성 및 단어 삽입
        trie: Trie[str] = Trie()
        for word in words:
            trie.push(word)
        
        # 각 단어의 버튼 입력 횟수 계산 후 평균
        total = 0
        for word in words:
            total += count(trie, word)
        
        avg = total / n
        print(f"{avg:.2f}")


if __name__ == "__main__":
    main()
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        pointer = 0  # 루트 노드부터 시작
        
        for element in seq:
            # 현재 노드의 children에서 element를 body로 가진 노드 찾기
            found = False
            for child_idx in self[pointer].children:
                if self[child_idx].body == element:
                    pointer = child_idx
                    found = True
                    break
            
            # 찾지 못하면 새 노드 추가
            if not found:
                new_node = TrieNode(body=element)
                self.append(new_node)
                new_idx = len(self) - 1
                self[pointer].children.append(new_idx)
                pointer = new_idx
        
        # 마지막 노드를 단어의 끝으로 표시
        self[pointer].is_end = True



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


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

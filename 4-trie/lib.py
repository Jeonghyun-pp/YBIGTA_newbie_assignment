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
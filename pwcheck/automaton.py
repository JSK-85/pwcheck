"""Aho-Corasick automaton for multi-pattern substring search."""

from collections import deque


class AhoCorasick:
    __slots__ = ("_goto", "_fail", "_out")

    def __init__(self, patterns):
        self._goto = [{}]   # node -> {char: next_node}
        self._fail = [0]    # node -> fallback node on mismatch
        self._out = [None]  # node -> match length if a pattern ends here
        for word in patterns:
            if word:
                self._add(word)
        self._build()

    def _add(self, word):
        node = 0
        for ch in word:
            next_node = self._goto[node].get(ch)
            if next_node is None:
                next_node = len(self._goto)
                self._goto.append({})
                self._fail.append(0)
                self._out.append(None)
                self._goto[node][ch] = next_node
            node = next_node
        word_len = len(word)
        prev = self._out[node]
        self._out[node] = word_len if prev is None or word_len < prev else prev

    def _build(self):
        # BFS to compute failure links to the longest proper suffix
        queue = deque(self._goto[0].values())
        while queue:
            node = queue.popleft()
            for ch, target in self._goto[node].items():
                f = self._fail[node]
                while f and ch not in self._goto[f]:
                    f = self._fail[f]
                fail_target = self._goto[f].get(ch, 0)
                self._fail[target] = fail_target if fail_target != target else 0

                fail_out = self._out[self._fail[target]]
                if fail_out is not None and (self._out[target] is None or fail_out < self._out[target]):
                    self._out[target] = fail_out
                queue.append(target)

    def first_match(self, text):
        """Return (start, end) of the earliest-ending match, or None."""
        node = 0
        for i, ch in enumerate(text):
            while node and ch not in self._goto[node]:
                node = self._fail[node]
            node = self._goto[node].get(ch, 0)
            match_len = self._out[node]
            if match_len is not None:
                return (i - match_len + 1, i + 1)
        return None

    def contains_any(self, text):
        """Return True if text contains any pattern as a substring."""
        return self.first_match(text) is not None


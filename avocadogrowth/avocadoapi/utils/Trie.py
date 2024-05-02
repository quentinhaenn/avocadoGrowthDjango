class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        node = self.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def delete(self, word):
        word = word.lower()
        self._delete_recursive(self.root, word, 0)

    def _delete_recursive(self, node, word, index):
        if index == len(word):
            if not node.is_end_of_word:
                return
            node.is_end_of_word = False
            return
        char = word[index]
        if char not in node.children:
            return
        child_node = node.children[char]
        self._delete_recursive(child_node, word, index + 1)
        if child_node.children == {} and not child_node.is_end_of_word:
            del node.children[char]

    def _from_str(self, string, separator=' '):
        words = string.split(separator)
        for word in words:
            self.insert(word)

    def _from_list(self, words):
        for word in words:
            self.insert(word)

    def initialize(self, data, separator=None):
        if isinstance(data, str):
            if not separator:
                self._from_str(data)
            else:
                self._from_str(data, separator)
        elif isinstance(data, list):
            self._from_list(data)
        else:
            raise ValueError("Data type not supported")

    def find_words(self, prefix):
        node = self.root
        prefix = prefix.lower()
        words = []
        for char in prefix:
            if char not in node.children:
                break
            node = node.children[char]

        if node.is_end_of_word:
            words.append(prefix)

        self._find_words_recursive(node, prefix, words)
        return words

    def _find_words_recursive(self, node, prefix, words):
        if node.is_end_of_word and prefix not in words:
            words.append(prefix)
        for char, child_node in node.children.items():
            self._find_words_recursive(child_node, prefix + char, words)

    def __str__(self):
        self._print_recursive(self.root, "")

    def _print_recursive(self, node, prefix):
        if node.is_end_of_word:
            print(prefix)
        for char, child_node in node.children.items():
            self._print_recursive(child_node, prefix + char)

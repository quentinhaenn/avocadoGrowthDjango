class TrieNode:
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    """
    Trie data structure implementation.

    Supports the following operations:
    - insert(word: str) -> None: Inserts a word into the trie.
    - search(word: str) -> bool: Searches for a word in the trie.
    - starts_with(prefix: str) -> bool: Searches for a prefix in the trie.
    - delete(word: str) -> None: Deletes a word from the trie.
    - find_words(prefix: str) -> List[str]: Finds all words with a given prefix.
    - initialize(data: Union[str, List[str]], separator: Optional[str] = None) -> None:
    Initializes the trie with a list of words or a string of words.
    """
    root = TrieNode()

    @classmethod
    def insert(cls, word):
        """
        Inserts a word into the trie.
        """
        node = cls.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    @classmethod
    def search(cls, word):
        """
        Searches for a word in the trie.
        """
        node = cls.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    @classmethod
    def starts_with(cls, prefix):
        """
        Searches for a prefix in the trie.
        """
        node = cls.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    @classmethod
    def delete(cls, word):
        """
        Deletes a word from the trie.
        """
        word = word.lower()
        cls._delete_recursive(cls.root, word, 0)

    @classmethod
    def _delete_recursive(cls, node, word, index):
        """
        Helper function for deleting a word from the trie.
        """
        if index == len(word):
            if not node.is_end_of_word:
                return
            node.is_end_of_word = False
            return
        char = word[index]
        if char not in node.children:
            return
        child_node = node.children[char]
        cls._delete_recursive(child_node, word, index + 1)
        if child_node.children == {} and not child_node.is_end_of_word:
            del node.children[char]

    @classmethod
    def _from_str(cls, string, separator=" "):
        """
        Initializes the trie with a string of words.
        """
        words = string.split(separator)
        for word in words:
            cls.insert(word)

    @classmethod
    def _from_list(cls, words):
        """
        Initializes the trie with a list of words.
        """
        for word in words:
            cls.insert(word)

    @classmethod
    def initialize(cls, data, separator=None):
        """
        Initializes the trie with a list of words or a string of words.
        """
        if isinstance(data, str):
            if not separator:
                cls._from_str(data)
            else:
                cls._from_str(data, separator)
        elif isinstance(data, list):
            cls._from_list(data)
        else:
            raise ValueError("Data type not supported")

    @classmethod
    def find_words(cls, prefix):
        """
        Finds all words with a given prefix.
        """
        node = cls.root
        prefix = prefix.lower()
        words = []
        for char in prefix:
            if char not in node.children:
                break
            node = node.children[char]

        if node.is_end_of_word:
            words.append(prefix)

        cls._find_words_recursive(node, prefix, words)
        return words

    @classmethod
    def _find_words_recursive(cls, node, prefix, words):
        """
        Helper function for finding all words with a given prefix.
        """
        if node.is_end_of_word and prefix not in words:
            words.append(prefix)
        for char, child_node in node.children.items():
            cls._find_words_recursive(child_node, prefix + char, words)

    def __str__(self):
        self._print_recursive(self.root, "")

    @classmethod
    def _print_recursive(cls, node, prefix):
        """
        Helper function for printing the trie.
        """
        if node.is_end_of_word:
            print(prefix)
        for char, child_node in node.children.items():
            cls._print_recursive(child_node, prefix + char)

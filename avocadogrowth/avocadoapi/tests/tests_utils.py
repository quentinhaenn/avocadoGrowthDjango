from ..utils.trie import Trie
from django.test import TestCase


class TestTrie(TestCase):

    def test_setup(self):
        trie = Trie()
        assert trie is not None

    def test_insert(self):
        trie = Trie()
        trie.insert("python")
        assert trie.search("python")
        assert not trie.search("java")
        trie.insert("java")
        assert trie.search("java")

    def test_start_with(self):
        trie = Trie()
        trie.insert("python")
        trie.insert("java")
        trie.insert("javascript")
        assert trie.starts_with("py")
        assert trie.starts_with("ja")
        assert not trie.starts_with("c")

    def test_delete(self):
        trie = Trie()
        trie.insert("python")
        trie.insert("java")
        trie.insert("javascript")
        trie.insert("c++")
        trie.insert("c#")
        assert trie.search("python")
        trie.delete("python")
        assert not trie.search("python")
        assert trie.search("java")
        trie.delete("java")
        assert not trie.search("java")
        assert trie.search("javascript")
        trie.delete("javascript")
        assert not trie.search("javascript")
        assert trie.search("c++")
        trie.delete("c++")
        assert not trie.search("c++")
        assert trie.search("c#")
        trie.delete("c#")
        assert not trie.search("c#")

    def test_init_from_string(self):
        string = "python java javascript c++ c#"
        string_with_separator = "python,java,javascript,c++,c#"
        string_trie = Trie()
        string_trie.initialize(string)
        string_with_separator_trie = Trie()
        string_with_separator_trie.initialize(string_with_separator, separator=",")
        assert string_trie is not None
        assert string_with_separator_trie is not None
        assert string_trie.search("python")
        assert string_trie.search("java")
        assert string_trie.search("javascript")
        assert string_trie.search("c++")
        assert string_trie.search("c#")
        assert string_with_separator_trie.search("python")
        assert string_with_separator_trie.search("java")
        assert string_with_separator_trie.search("javascript")
        assert string_with_separator_trie.search("c++")
        assert string_with_separator_trie.search("c#")

    def test_init_from_list(self):
        list_of_words = ["python", "java", "javascript", "c++", "c#"]
        trie = Trie()
        trie.initialize(list_of_words)
        assert trie is not None
        assert trie.search("python")
        assert trie.search("java")
        assert trie.search("javascript")
        assert trie.search("c++")
        assert trie.search("c#")

    def test_autocomplete(self):
        trie = Trie()
        trie.insert("python")
        trie.insert("java")
        trie.insert("javascript")
        trie.insert("c++")
        trie.insert("c#")
        auto_python = trie.find_words("py")
        auto_java = trie.find_words("ja")
        auto_c = trie.find_words("c")
        assert auto_python == ["python"]
        assert auto_java == ["java", "javascript"]
        assert auto_c == ["c++", "c#"]

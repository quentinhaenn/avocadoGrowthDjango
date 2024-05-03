from ..utils.trie import Trie
from django.test import TestCase


class TestTrie(TestCase):

    def test_instantiate(self):
        trie = Trie()
        assert trie is not None

    def test_insert(self):
        trie_insert = Trie()
        trie_insert.insert("python")
        assert trie_insert.search("python")
        assert not trie_insert.search("java")
        trie_insert.insert("java")
        assert trie_insert.search("java")

    def test_start_with(self):
        trie_start = Trie()
        trie_start.insert("python")
        trie_start.insert("java")
        trie_start.insert("javascript")
        assert trie_start.starts_with("py")
        assert trie_start.starts_with("ja")
        assert not trie_start.starts_with("c")

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
        trie_list = Trie()
        trie_list.initialize(list_of_words)
        assert trie_list is not None
        assert trie_list.search("python")
        assert trie_list.search("java")
        assert trie_list.search("javascript")
        assert trie_list.search("c++")
        assert trie_list.search("c#")

    def test_autocomplete(self):
        trie_auto = Trie()
        trie_auto.insert("python")
        trie_auto.insert("java")
        trie_auto.insert("javascript")
        trie_auto.insert("c++")
        trie_auto.insert("c#")
        auto_python = trie_auto.find_words("py")
        auto_java = trie_auto.find_words("ja")
        auto_c = trie_auto.find_words("c")
        assert auto_python == ["python"]
        assert auto_java == ["java", "javascript"]
        assert auto_c == ["c++", "c#"]

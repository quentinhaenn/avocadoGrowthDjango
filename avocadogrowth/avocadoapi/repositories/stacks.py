from ..models import Stacks
from .base import BaseRepository
from ..utils.Trie import Trie


class StackRepository(BaseRepository):
    model = Stacks
    trie = Trie()

    @classmethod
    def create_trie(cls):
        stacks = cls.model.objects.all()
        stacks = [stack.tag for stack in stacks]
        cls.trie.initialize(stacks)

    @classmethod
    def autocomplete(cls, query):
        return cls.trie.find_words(query)

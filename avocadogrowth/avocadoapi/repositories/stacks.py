from ..models import Stacks
from .base import BaseRepository
from ..utils.trie import Trie


class StackRepository(BaseRepository):
    """
    Repository class for the Stacks model.

    Methods:
    - create_trie: Initializes the trie with all the stack tags in the database
    - autocomplete: Returns a list of stack tags that match the input query
    """
    model = Stacks
    trie = Trie()

    @classmethod
    def create_trie(cls):
        """
        Initializes the trie with all the stack tags in the database
        """
        stacks = cls.model.objects.all()
        stacks = [stack.tag for stack in stacks]
        cls.trie.initialize(stacks)

    @classmethod
    def autocomplete(cls, query):
        """
        Returns a list of stack tags that match the input query
        """
        return cls.trie.find_words(query)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False
    
class Trie:

    def __init__(self):
        self.root = TrieNode()
    
    def insert(self,word):
        word = word.lower()
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.isEnd = True

    def search(self,word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        
        return node.isEnd


    def find_words_with_prefix(self, prefix):

        prefix = prefix.lower()
        
        def dfs(node, path, words):
            if node.isEnd:
                words.append("".join(path.copy()))  

            for char, next_node in node.children.items():
                path.append(char)
                dfs(next_node, path, words)
                path.pop()  # backtrack

        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  
            node = node.children[char]

        words = []
        dfs(node, list(prefix), words)
        return words


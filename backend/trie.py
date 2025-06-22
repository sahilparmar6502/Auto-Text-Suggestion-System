class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False
        self.word = ""
    
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
        node.word = word

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
    

    def find_closest_match(self, word, max_distance=None):
        """Finds the closest words in the Trie using Edit Distance, allowing multiple misspellings."""
        if max_distance is None:
            max_distance = min(3, len(word) // 2)  # Dynamically adjust allowed distance
        
        closest_matches = []
        
        def dfs(node, current_word, previous_row):
            columns = len(word) + 1
            current_row = [previous_row[0] + 1]
            
            for i in range(1, columns):
                insert_cost = current_row[i - 1] + 1
                delete_cost = previous_row[i] + 1
                replace_cost = previous_row[i - 1] + (0 if (current_word and word[i - 1] == current_word[-1]) else 1)
                
                current_row.append(min(insert_cost, delete_cost, replace_cost))
            
            if current_row[-1] <= max_distance and node.isEnd:
                closest_matches.append((current_row[-1],node.word))
            
            if min(current_row) <= max_distance:
                for char, child_node in node.children.items():
                    dfs(child_node, current_word + char, current_row)

        dfs(self.root, "", list(range(len(word) + 1)))
        
        return sorted(closest_matches, key=lambda x: x[0])[:5]  # Return top 5 closest matches
        # return sorted(closest_matches)[:5]  # Return top 5 closest matches


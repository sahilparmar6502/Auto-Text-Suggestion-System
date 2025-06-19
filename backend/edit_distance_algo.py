class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = None  # Store word at the end node for reference

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word

    def search(self, word):
        """Returns True if word is found, else False."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

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
            
            if current_row[-1] <= max_distance and node.is_end_of_word:
                closest_matches.append((current_row[-1], node.word))
            
            if min(current_row) <= max_distance:
                for char, child_node in node.children.items():
                    dfs(child_node, current_word + char, current_row)

        dfs(self.root, "", list(range(len(word) + 1)))
        
        return sorted(closest_matches, key=lambda x: x[0])[:5]  # Return top 5 closest matches

# Example Usage:
trie = Trie()
dictionary_words = ["hello", "world", "python","programmer", "programming", "dictionary", "example", "developer", "engineer"]
for word in dictionary_words:
    trie.insert(word)

word_to_search = "pragramner"  # Misspelled word
if trie.search(word_to_search):
    print(f"'{word_to_search}' found in Trie.")
else:
    print(f"'{word_to_search}' not found. Suggestions: {trie.find_closest_match(word_to_search)}")

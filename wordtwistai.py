#table id is board
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

board = [ [ " " for i in range(4)] for j in range(4)]

words = []

class TrieNode:
    char = ""
    children = []
    isLeaf = False

    def __init__(self, char):
        self.char = char
        self.children = [None for i in range(26)]
        self.isLeaf = False

def c2i(c):
    return ord(c)-65

def add(word, root):
    currNode = root
    for i in word:
        if not currNode.children[c2i(i)]:
            currNode.children[c2i(i)] = TrieNode(i)
        currNode = currNode.children[c2i(i)]
    currNode.isLeaf = True

def isSafe(x, y, visited):
    return x >= 0 and x <= 3 and y >= 0 and y <= 3 and not visited[x][y]

def searchWords(root, board, x, y, visited, word):
    global wordsn

    if root.isLeaf and len(word) > 2:
        words.append(word)

    if isSafe(x, y, visited):

        visited[x][y] = True

        for i in root.children:
            if i:

                ch = i.char

                if isSafe(x+1, y, visited) and board[x+1][y] == ch:
                    searchWords(i, board, x+1, y, visited, word+ch)

                if isSafe(x-1, y, visited) and board[x-1][y] == ch:
                    searchWords(i, board, x-1, y, visited, word+ch)

                if isSafe(x+1, y+1, visited) and board[x+1][y+1] == ch:
                    searchWords(i, board, x+1, y+1, visited, word+ch)

                if isSafe(x, y+1, visited) and board[x][y+1] == ch:
                    searchWords(i, board, x, y+1, visited, word+ch)

                if isSafe(x-1, y+1, visited) and board[x-1][y+1] == ch:
                    searchWords(i, board, x-1, y+1, visited, word+ch)

                if isSafe(x+1, y-1, visited) and board[x+1][y-1] == ch:
                    searchWords(i, board, x+1, y-1, visited, word+ch)

                if isSafe(x, y-1, visited) and board[x][y-1] == ch:
                    searchWords(i, board, x, y-1, visited, word+ch)

                if isSafe(x-1, y-1, visited) and board[x-1][y-1] == ch:
                    searchWords(i, board, x-1, y-1, visited, word+ch)

        visited[x][y] = False



f = open("sowpods.txt")
dictionary = [i.strip() for i in f.readlines()]
root = TrieNode("*")

for i in dictionary:
    add(i, root)

driver = webdriver.Firefox()
driver.get("http://www.wordtwist.org/init4.php")
start = driver.find_element_by_id('newgameboard').find_element_by_xpath("id('newgameboard')/p/a")
start.click()
start = driver.find_element_by_id("start")
start.click()

b = ""

table = driver.find_element_by_id("board")
rows = table.find_elements_by_xpath("id('board')/tbody/tr")

for e in rows:
    data = e.find_elements_by_xpath("td")
    for d in data:
        b = b + d.text

b = list(b)

for i in range(16):
    board[i//4][i%4] = b[i]

for i in range(4):
    for j in range(4):
        searchWords(root.children[c2i(board[i][j])], board, i, j, [[False for x in range(4)] for y in range(4)], board[i][j])

words = list(set(words))

box = driver.find_element_by_id("word")
for i in words:
    box.send_keys(i)
    box.send_keys(Keys.RETURN)
    sleep(0.1)


#### Word Search
def wordSearch(board, word):
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
            result = wordSearchDirection(board, word, row, col)
            if result != None:
                return result
    return None
    
def wordSearchDirection(board, word, row, col):
    directions = 8
    for dirs in range(directions):
        result = wordSearchDirectionFromCell(board, word, row, col, dirs)
        if result != None: return result
    return None
    
def wordSearchDirectionFromCell(board, word, startrow, startcol, dirs):
    rows, cols = len(board), len(board[0])
    directions = [[-1, -1], [-1, 0], [-1, 1],
                  [0, -1],           [0, 1],
                  [1, -1], [1, 0],   [1, 1]]
    names = ["up-left", "up", "up-right",
             "left",            "right",
             "down-left", "down", "down-right"]
    (drow, dcol) = directions[dirs]
    for i in range(len(word)):
        row = startrow + i*drow
        col = startcol + i*dcol
        if row < 0 or col < 0 or row >= rows or col >= cols or board[row][col] != word[i]:
            return None
    return (word, (startrow, startcol), names[dirs])
    
    
    
def testWordSearch():
    board = [ [ 'd', 'o', 'g' ],
              [ 't', 'a', 'c' ],
              [ 'o', 'a', 't' ],
              [ 'u', 'r', 'k' ],
            ]
    print(wordSearch(board, "dog")) # ('dog', (0, 0), 'right')
    print(wordSearch(board, "cat")) # ('cat', (1, 2), 'left')
    print(wordSearch(board, "tad")) # ('tad', (2, 2), 'up-left')
    print(wordSearch(board, "cow")) # None

testWordSearch()


### Locker Problem

def lockerProblem(lockers):
    isOpen = [False]*(lockers + 1)
    students = lockers
    openLockers = []
    for student in range(1, students + 1):
        for locker in range(student, lockers + 1, student):
            isOpen[locker] = not isOpen[locker]
    for locker in range(1, lockers + 1):
        if isOpen[locker]:
            openLockers.append(locker)
    return openLockers
    
print(lockerProblem(2000))

### Sieve of Eratosthenes

def sieve(n):
    isPrime = [True] * (n+1)
    isPrime[0] = isPrime[1] = False
    prime = []
    for num in range(n+1):
        if isPrime[num] == True:
            prime.append(num)
            for multiple in range(num*2, n+1, num):
                isPrime[multiple] = False
    return prime
    
print(sieve(100))


### RedrawAllWrapper

def runFunction(width = 300, height = 300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.create_rectangle(0, 0, width, height, fill = "white", width = 0)
        canvas.update()
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100
    init(data)
    root = Tk()
    canvas = Canvas(root, width, height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop()
    print("bye!")
    
    
### Tetris

def rotateFallingPiece(data):
    origRows = data.fallingPieceRows
    origCols = data.fallingPieceCols
    origPiece = data.fallingPiece
    origRow = data.fallingPieceRow
    origCol = data.fallingPieceCol
    data.fallingPieceRows, data.fallingPieceCols = data.fallingPieceCols, data.fallingPieceRows
    newPiece = [[0]*data.fallingPieceCols for i in range(data.fallingPieceRows)]
    for row in range(data.fallinPieceRows):
        for col in range(data.fallingPieceCols):
            newPiece[row][col] = data.fallingPiece[col][origCols - 1 - row]
    data.fallingPiece = newPiece
    data.fallingPieceRow = data.fallingPieceRow + origRows//2 - data.fallingPieceRows//2
    data.fallingPieceCol = data.fallingPieceCol + origCols//2 - data.fallingPieceCols//2
    if not isLegalMove(data):
        data.fallingPieceRows = origRows
        data.fallingPieceCols = origCols
        data.fallingPiece = origPiece
        data.fallingPieceRow, data.fallingPieceCol = origRow, origCol
        
def newFallingPiece(data):
    piece = random.randint(0, len(data.Pieces))
    data.fallingPiece = data.Pieces[piece]
    data.fallingColor = data.colors[piece]
    data.fallingPieceRows, data.fallingPieceCols = len(data.fallingPiece), len(data.fallingPiece[0])
    data.fallingRow = 0
    data.fallingRow = data.cols//2 - data.fallingPieceCols//2
    

    
    
    
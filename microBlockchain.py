import hashlib, datetime, sqlite3

con = sqlite3.connect('site.db')
cur = con.cursor()

class Blockchain():
    def __init__(self, index, timestamp, data, previousHash):  #change limit
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.hash = self.hashBlock()
  
    def hashBlock(self):
        sha = hashlib.sha256(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previousHash).encode('utf-8'))
        return sha.hexdigest()

def createGenesisBlock():
    sql = f'INSERT INTO blocks (id, time, data, hash) VALUES (0, "{str(datetime.datetime.now())}", "Genesis Block", "{0}")'
    con.execute(sql)
    con.commit()
    return Blockchain(0, datetime.datetime.now(), 'Genesis Block', 0)

def nextBlock(lastBlock):
    getLastId = 'SELECT MAX(id) FROM blocks'
    cur.execute(getLastId)
    lastBlockData = cur.fetchall()
    index = lastBlockData[0][0] + 1
    timestamp = datetime.datetime.now()
    data = "Conium"
    hash = lastBlock.hash
    sql = f'INSERT INTO blocks (id, time, data, hash) VALUES ({index}, "{str(timestamp)}", "{data}", "{hash}")'
    con.execute(sql)
    con.commit()
    return Blockchain(index, timestamp, data, hash)

blockchain = [createGenesisBlock()]
previousBlock = blockchain[0]

while True:
    blockToAdd = nextBlock(previousBlock)
    blockchain.append(blockToAdd)
    previousBlock = blockToAdd
    print("Block #{} has been added!".format(blockToAdd.index))
    print("Hash: {}\n".format(blockToAdd.hash)) 

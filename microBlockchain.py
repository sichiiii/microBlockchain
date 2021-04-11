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
    return Blockchain(0, datetime.datetime.now(), 'Genesis Block', 0)

def nextBlock(lastBlock):
    index = lastBlock.index + 1
    timestamp = datetime.datetime.now()
    data = "Conium"
    hash = lastBlock.hash
    sql = f'INSERT INTO blocks (id, time, data, hash) VALUES ({index}, "{str(timestamp)}", "{data}", "{str(hash)}")'
    con.execute(sql)
    con.commit()
    return Blockchain(index, timestamp, data, hash)

blockchain = [createGenesisBlock()]
previousBlock = blockchain[0]
numOfBlocks = 5

for i in range(0, numOfBlocks):
    blockToAdd = nextBlock(previousBlock)
    blockchain.append(blockToAdd)
    previousBlock = blockToAdd
    print("Block #{} has been added!".format(blockToAdd.index))
    print("Hash: {}\n".format(blockToAdd.hash)) 

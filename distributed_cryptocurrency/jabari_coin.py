# Module 2 - Create a Cryptocurrency on a Blockchain

# import libraries
import datetime # each block will have timestamp of when block was mined
import hashlib # hash the block
import json # encode the blocks when done hashing
from flask import Flask, jsonify, request # create web app and send/recieve json data
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 - Building a Blockchain

"""
Representation of an entire blockchain.

Here's a sample use case.

Blockchain server is running...
-> API Call -- Mine Block
- Need the prev proof because our proof is based upon the proof of the prev block
- 

"""

MINING_DIFFICULTY = 4 # the larger the value the harder it is to mine
# this adds more target leading zeros
# (in real block chains the number of leading zeros is 18!)

class Blockchain:
    # inits the chain of blocks
    def __init__(self):
        # init the chain. list containing different blocks in blockchain
        self.chain = [] 
        
        # list of transactions before they are added to a block
        self.transactions = []
        
        # create genesis block. each block has proof and key to prev hash
        # note: 0 is '0' because SHA256 lib can only accept strings
        self.create_block(proof = 1, previous_hash = "0") 
        
        # nodes all around the world -- imitating a real blockchain ; set because we do not care about order
        self.nodes = set()
        
    # creates a block and appends it to the blockchain
    def create_block(self, proof, previous_hash):
        """
        Creates a block and adds it to the blockchain.
        
        Parameters
        ----------
        proof : 
            the previous proof value (nonce), needed to get the proof of work
            of the current block
        
        previous_hash:
            string the previous hash value 

        Returns
        -------
        The Block (dict)
        """
        # define new block
        block = {'index': len(self.chain) + 1, # the index of this block
                 'timestamp': str(datetime.datetime.now()), # exact time when mined
                 # timestamp put in string for json formatting
                 'proof': proof,
                 'previous_hash': previous_hash,
                 "transactions": self.transactions
                 } 
        
        
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        """
        Returns the proof of work (nonce) value.

        Parameters
        ----------
        previous_proof : 
            the previous proof value (nonce), needed to get the proof of work
            of the current block

        Returns
        -------
        N/A
        """
        # starting value of proof variable
        new_proof = 1
        found_nonce = False
        
        while found_nonce is False:
            # perform non symmetrical (no adding or multiplying) 
            # problem miners have to solve; this can be customized as we like
            # square to add a bit more complexity
            complex_operation = new_proof**2 - previous_proof**2
            
            # encoding the complex operation thats a string taking the hash of it
            # and getting the hex digits.
            hash_operation = hashlib.sha256(str(complex_operation).encode()).hexdigest()
            
            # check if first N characters are zeros
            # Ex. if MINING_DIFFICULTY=4 check that hash starts with: '0000...'
            if hash_operation[:MINING_DIFFICULTY] == '0' * MINING_DIFFICULTY:
                # return the new proof
                found_nonce = True # not necessary can simply return
                return new_proof
            else:
                # increment new_proof
                new_proof += 1
    
    def hash(self, block):
        """
        Returns the SHA266 hash of a block.

        Parameters
        ----------
        block : Dictionary
            Mapping of blockchain fields to it's values.

        Returns
        -------
        String

        """
        # Encode block in right format for sha256
        encoded_block = json.dumps(block, sort_keys = True).encode()
        # Returns its hash
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0] # start with prev block
        block_index = 1 # start with the second block according to index
        # indexing starts at 0
        
        
        while block_index < len(chain):
            # 1) Test: prev hash == hash of current block
            block = chain[block_index]
            
            # if our previous hash that we calculated (actual) !=
            # previous hash that calculate (verifcation)
            if block['previous_hash'] != self.hash(previous_block):
                return False
        
            # 2) Test: proof of work is valid for each block
            # Get previous proof
            previous_proof = previous_block['proof']
            # Get proof of current block
            proof = block['proof']
            
            complex_operation = proof**2 - previous_proof**2
            hash_operation = hashlib.sha256(str(complex_operation).encode()).hexdigest()
            if hash_operation[:MINING_DIFFICULTY] != '0' * MINING_DIFFICULTY:
                return False
            
            previous_block = block
            block_index += 1
        
        return True


    # Specific to Cryptocurrecny
    def add_transactions(self, sender, receiver, amount):
        # simply add to list of Txns
        self.transactions.append({"sender": sender, "receiver": receiver, "amount":amount})
        
        
        # get previous block to return index
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1
    
    def add_node(self, address):
        """
        Adds node containing the address to the set of nodes.
        
        This is used to decentralize our blockchain.
        
        Ex. http://127.0.0.1:5000/
        Scheme, Netloc (url), Path, Params, etc...

        Parameters
        ----------
        address : TYPE
            URL Address of the node.

        Returns
        -------
        None.

        """
        # parse address of node
        parsed_url = urlparse(address)
        
        # add to node
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        """
        Replaces the chain in this node with the longest chain in the network
        
        Function will be called in specific node.

        Returns
        -------
        Boolean value if the chain was updated.

        """
        # get nodes all around the world
        network = self.nodes
        
        longest_chain = None
        max_length = len(self.chain) # chain of this node
        
        for node in network:
            # make a request to that node for it's chain
            response = requests.get(f"{node}/get_chain")
            if response.status_code == 200:
                length_of_chain = response.json()['length']
                chain = response.json()['chain']
                
                # if this is longest chain and this chain is valid...
                # update to be longest chain
                if length_of_chain > max_length and self.is_chain_valid(chain):
                    max_length = length_of_chain
                    longest_chain = chain
    
        # if chain was replaced
        if longest_chain:
            self.chain = longest_chain
            return True
        else:
            return False

















# Part 2 - Mining our Blockchain 

# Creating a Web App
# See https://flask.palletsprojects.com/en/2.0.x/quickstart/
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create address for the node on Port 5000
# whenever a miner mines a block they get crypto therefore they need an address
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    # Need the previous block so we can access the previous proof
    previous_block = blockchain.get_previous_block()
    
    # The complex problem requires the previous proof to be added
    previous_proof = previous_block['proof']
    
    # Perform the complex equation so that we have proof this block is ready
    proof = blockchain.proof_of_work(previous_proof)
    
    # Get previous hash so that this block references the last block
    previous_hash = blockchain.hash(previous_block)
    
    # Add the transaction to the list of transactions
    blockchain.add_transactions(sender=node_address, receiver="Tim", amount=1)
    
    # ADD!
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200

# Checking if the blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)
    response = {'is_valid': valid}
    
    return jsonify(response), 200
    

# Add a new transaction to the blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    # get values from JSON FILE (how 2 computers can communicate!)
    json = request.get_json()
    # check no missing keys in json request
    transaction_keys = ["sender", "receiver", "amount"]
    
    if not all (key in json for key in transaction_keys):
        return "Some elements of the transaction are missing!", 400
    
    # Add the transaction to this node's blockchain, this returns the index of the BLOCK in the chain.
    index = blockchain.add_transactions(json["sender"], json["receiver"], json["amount"])
    
    # return response
    response = {'message': f"This transaction will be added to Block {index}"}
    return jsonify(response), 201 # HTTP created


## Part 3 - Decentralize our Blockchain

# Connect new nodes to our network
@app.route('/connect_node', methods=['POST'])
def connect_node():
    # get values from JSON FILE (how 2 computers can communicate!)
    json = request.get_json()
    # get addresses to add to our network
    nodes = json.get('nodes')
    if nodes is None:
        return "No nodes in request to add to network", 400
    
    # add each node given in request to each blockchain's network
    for node in nodes:
        blockchain.add_node(node)
    
    # return response
    response = {"message": "Successfully added nodes to network", "total_nodes":list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    chain_was_replaced = blockchain.replace_chain()
 
    response = {'chain_was_replaced': chain_was_replaced, 
                'chain': blockchain.chain}

    
    return jsonify(response), 200
    

# Running the app
app.run(host='0.0.0.0', port=5000)
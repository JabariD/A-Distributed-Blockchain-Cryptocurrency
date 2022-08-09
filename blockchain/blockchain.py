# Module 1 - Create a Blockchain

# import libraries
import datetime # each block will have timestamp of when block was mined
import hashlib # hash the block
import json # encode the blocks when done hashing
from flask import Flask, jsonify # create web app and send/recieve json data

# Part 1 - Building a Blockchain

"""
Representation of an entire blockchain.
"""

MINING_DIFFICULTY = 4 # the larger the value the harder it is to mine

class Blockchain:
    # inits the chain of blocks
    def __init__(self):
        # init the chain. list containing different blocks in blockchain
        self.chain = [] 
        
        # create genesis block. each block has proof and key to prev hash
        # note: 0 is '0' because SHA256 lib can only accept strings
        self.create_block(proof = 1, previous_hash = "0") 
        
    # creates a block and appends it to the blockchain
    def create_block(self, proof, previous_hash):
        # define new block
        block = {'index': len(self.chain) + 1, # the index of this block
                 'timestamp': str(datetime.datetime.now()), # exact time when mined
                 # timestamp put in string for json formatting
                 'proof': proof,
                 'previous_hash': previous_hash
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
                found_nonce = True # not necessary if return
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

# Part 2 - Mining our Blockchain 

# Creating a Web App
# See https://flask.palletsprojects.com/en/2.0.x/quickstart/
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

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
    
    # ADD!
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous hash': block['previous_hash']}
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
    

# Running the app
app.run(host='0.0.0.0', port=5000)
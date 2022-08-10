# The JabariDChain | Create Your Own Blockchain
The JabariDChain is a simple blockchain that supports mining blocks, getting the chain, and checking if the chain is valid.

## Init Method
-   Init the blockchain by:
    -   Creating a list
    -   Creating the first genesis block
        -   Each block needs to get a proof of work and the previous hash to be created
## Create Block
Called after Mine Block
-   Creates block with all of its aspects and appends it to the blockchain
## Get Prev Block 
Gets the previous block
## Mine block
Gets the proof of work that we will need to solve
## Make Proof of Work
-   hard to find but easily to verify
-   to solve the problem with a trial and error approach, we keep incrementing new_proof
    -   we want the string to start with 4 leading zeros. the more leading zeros we impose the harder it is to mine the blocks
    -   note: complex operation should be non symmetrical.
## Blockchain checker
-   Check each block has correct proof of work
-   Check prev hash == hash of next block

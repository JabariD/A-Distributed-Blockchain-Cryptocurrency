
# The Jabaricoin Cryptocurrency
Cryptocurrency’s built upon Blockchain’s so we need an implementation of a basic Blockchain that we will customize.

Remember what makes a Blockchain a cryptocurrency — **Transactions**.
-   Key element that we will add to Blockchain

Then we want to build a **Consensus Function** to make sure each node has the same chain at any time.

Therefore, in addition to the normal blockchain operations (shown [here](https://github.com/JabariD/A-Distributed-Blockchain-Cryptocurrency/tree/main/blockchain)), this cryptocurrency supports adding transactions.

## Adding Transactions
Our Blockchain needs to keep a list of the current Transactions it has. Transactions are ***not born in a block***.
-   Init Txns    
    -   The Txns are appended to a list and as soon as a miner mines the block
    -   THEN all of the Txns are added to this block.
    -   Then the Txns list will be empty and will be able to be reused.
-   Create format for Txns and Append to List of Txns
    -   Sender, Receiver, Amount
	- Return the index of the block that will receive Txns

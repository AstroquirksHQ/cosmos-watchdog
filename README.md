TODO : 

- Add all config in config files
- Add docker for the bot
- Improve Readme
- Add more stuff in the messages (balance, hash, memo)
- use colors https://gist.github.com/kkrypt0nn/a02506f3712ff2d1c8ca7c9e0aed7c06#file-ansi-colors-showcase-md
- Expose discord command to :
   - get balance
   - get list of delegators
   - get stats of my validator
   - get my history

# cosmos-watchdog

## Usage
### Running the Flask Service
To run the Flask service, use the following command:

Copy code
pipenv run dev
This will start the Flask application on http://localhost:5000.

Command-line Tools
Synchronize Transactions
To synchronize transactions related to a given validator, use the following command:

python
Copy code
pipenv run synchronize <address> [--tx-type <transaction-type> ...]
The address argument specifies the validator address, and the optional tx-type argument(s) specify the type(s) of transactions to synchronize (e.g., REDELEGATE, DELEGATE, RESTAKE, UNDELEGATE, UNREDELEGATE). If no tx-type is specified, all transaction types will be synchronized.

Wipe Transactions
To delete transactions related to a given validator, use the following command:

wasm
Copy code
pipenv run wipe [--tx-type <transaction-type> ...] [--from-offset <offset>]
The optional tx-type argument(s) specify the type(s) of transactions to delete (e.g., REDELEGATE, DELEGATE, RESTAKE, UNDELEGATE, UNREDELEGATE). If no tx-type is specified, all transaction types will be deleted. The optional from-offset argument specifies the offset from which to delete transactions.

Posting Notifications to Discord
To post notifications to a Discord channel, run the bot.py file and configure the Discord 
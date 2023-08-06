# web3_auto

This project helps you generate valid checksum address and account for EVM blockchains.

## Installing

    pip install web3_auto

## Usage

    # get valid EVM checksum address
    from web3_auto.to_checksum_address import to_checksum_address
    to_checksum_address(private_key='YOUR PRIVATE KEY')
    to_checksum_address(address='YOUR ADDRESS')
    to_checksum_address(account='YOUR ACCOUNT')
	
	# get EVM account from private key
    from web3_auto.from_key import from_key
    from_key(private_key='YOUR PRIVATE KEY')

	# get EVM account from mnemonic
	from web3_auto.from_mnemonic import from_mnemonic
    from_mnemonic(mnemonic='YOUR MNEMONIC PHRASE')
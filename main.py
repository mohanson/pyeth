import eth

prikey = eth.core.PriKey(1)
pubkey = prikey.pubkey()
print(pubkey.addr())

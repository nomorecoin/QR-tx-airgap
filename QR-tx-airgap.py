from pybitcointools import * # github.com/vbuterin/pybitcointools
import qrcode
import zlib
import qrcode

# NOTE: This is incomplete. No method for decoding QR images is implemented. Investigating modules.

# Hot/Cold tx split-generation for QR-airgapped machines
# Hot: create unsigned tx, compress, compress, encode QR and display
# Cold: decompress, decode unsigned tx from QR image, sign, compress, encode QR and display
# Hot: docompress, decode QR of signed tx from QR, broadcast

# TODO:
# decode QR from image
# decode transaction for confirmation before broadcast

def unsigned_tx(amount,from_addr,to_addr):
    """Create unsigned tx, returns string."""
    h = history(from_addr)
    outs = [{'value': amount, 'address': to_addr}]
    return mktx(h,outs)

def sign_tx(unsigned_tx,priv,i=0):
    """sign unsigned tx, returns string."""
    return(sign(unsigned_tx,i,priv))

def push_tx(signed_tx):
    """Attempt to broadcast tx using blockchain.info/pushtx"""
    return(push(signed_tx))

def c(s):
    """Compress string s, using zlib."""
    return s.encode("zlib")

def d(c):
    """Decompress zlib compressed string c."""
    return c.decode("zlib")

def makeQR(data):
    return qrcode.make(data)

def decodeQR(filename):
    pass
    
# create a complete keypair for testing
# intended use, hot side would have no access to priv
priv = sha256('Your super secure brainwallet phrase')
print(priv)
pub = privtopub(priv)
print(pub)
from_addr = pubtoaddr(pub)
print(from_addr)
to_addr = '1someaddressyouwanttosendto'

# Hot side creates unsigned transaction. Needs no access to private key.
unsigned = unsigned_tx(100000,from_addr,addr)
print(unsigned)
c_unsigned = c(unsigned)
print(c_unsigned)
hot = makeQR(c_unsigned)
hot.save('hot.png')

# Cold side decodes QR, decompresses, signs transaction. Requires private key for from_addr.
#d_unsigned = decodeQR('hot.png')
d_unsigned = d(c_unsigned)
print(d_unsigned)
signed = sign_tx(d_unsigned,priv)
print(signed)
c_signed = c(signed)
print(c_unsigned)
cold = makeQR(c_signed)
cold.save('cold.png')

# Hot, stage 2: decode, decompress, broadcast tx.
#c_signed = decodeQR('cold.png')
d_signed = d(c_signed)
print(d_signed)
push_tx(d_signed)

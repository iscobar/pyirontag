from smartcard.System import readers
from smartcard.util import toHexString

r=readers()
print r

connection = r[0].createConnection()
connection.connect()
SELECT = [0xFF, 0xB0, 0x00, 0x03, 0x00]

data, sw1, sw2 = connection.transmit(SELECT)
print chr(data[1])
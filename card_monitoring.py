from __future__ import print_function
from time import sleep

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

# define the apdus used in this script
GET_RESPONSE = [0XA0, 0XC0, 00, 00]
SELECT = [0xFF, 0xB0, 0x00, 0x03, 0x00]
DF_TELECOM = [0x7F, 0x10]


# a simple card observer that tries to select DF_TELECOM on an inserted card
class selectDFTELECOMObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def __init__(self):
        self.observer = ConsoleCardConnectionObserver()

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            card.connection = card.createConnection()
            card.connection.connect()
            card.connection.addObserver(self.observer)
            apdu = [0xFF,0xCA,0x00,0x00,0x00]
            response, sw1, sw2 = card.connection.transmit(apdu)
            print(response)
        for card in removedcards:
            print("-Removed: ")


if __name__ == '__main__':
    print("Insert or remove a SIM card in the system.")
    print("This program will exit in 60 seconds")
    print("")
    cardmonitor = CardMonitor()
    selectobserver = selectDFTELECOMObserver()
    cardmonitor.addObserver(selectobserver)

    sleep(60)

    # don't forget to remove observer, or the
    # monitor will poll forever...
    cardmonitor.deleteObserver(selectobserver)

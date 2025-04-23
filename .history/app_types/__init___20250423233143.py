from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Coins(Enum):
    BTC = "btc"
    ETH = "eth"
    USDT = "usdt"
    BNB = "bnb"

class TicketStatus(Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'
    CLOSED = 'closed'
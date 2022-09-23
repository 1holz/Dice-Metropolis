## Documentation about the communication between server and client:


# Receivable by server and client:

### {"type": "PING"}
Sends PONG back.

### {"type": "PONG"}
Outputs a connection confirmation.

### {"type": "ERROR", "msg": str}
Indicates that the previous inquiry caused an error. With "msg" being a more
detailed message.

### {"type": "CLOSE"}
Indicates that the other side will close the connection.



# Receivable by server only:

### {"type": "NAME", "name": str}
Sets the name of the player sending the package to "name".

### {"type": "INFO", "player": bool, "src": str|int}
Replies with a list of information from source or generic information if "player" or "src" are
missing. "player" and "src" are optional. "src" can be the name or index of a player or card.
The server will first attempt to interpret str as an int.

### {"type": "DICE", "mode": str}
Selects the dice mode if applicable.

### {"type": "BUY", "card": str|int}
Attempts to buy the card. "card" can be the name or index of a card. The server will first attempt to interpret str as an int. "card" is optional. If "card" is missing nothing will be bought and the buy phase will end.



# Receivable by client only:

### {"type": "PHASE", "phase": int}
Notifies the client of being active and of the current phase. Server expects an appropriate reply to this.

### {"type": "PRINT", "msg": str}
Outputs "msg".

### {"type": "PRINTS", "lines": [(str_id, str_format, args..., )]}
Outputs each tuple as a formatted line.



# Client console input:

### name str
Send a NAME package to the server after some checks.

### info c|p str|int
Requests info for the source.

### dice str
Attempts to set the dice mode to str.

### buy str|int
Attempts to buy the card.

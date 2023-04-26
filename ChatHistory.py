import json

class ChatHistory:
    def __init__(self, filename):
        self._filename = filename
        self._messages = []

    def clearMessages(self):
        self._messages = []

    def loadMessages(self):
        try:
            with open(self._filename, 'r') as f:
                self._messages = json.load(f)
        except:
            print("An exception occured while loading the message history.")
        
    def saveMessages(self):
        try:
            with open(self._filename, 'w') as f:
                json.dump(self._messages, f)
        except:
            print("An exception has occured while saving the message history.")

    def logNewMessage(self, role, content):
        self._messages.append({"role": role, "content": content})
        self.saveMessages()

    def getAllMessages(self):
        return self._messages
    
    def isEmpty(self):
        return (len(self._messages) == 0)
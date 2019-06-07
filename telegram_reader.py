import json


telegram_json_path = 'result.json'
interested_chat_name= 'Acquesi Sparsi'
i = 0

class telegramMessage:
    def __init__(self, author, text):
        self.author = author
        self.text = text
    
    def printMe(self):
        print('From:', self.author , ':',
            self.text)

if __name__ == "__main__":
    with open(telegram_json_path, 'r') as f:
        result = json.load(f)
    for chat in result.get('chats').get('list'):
        if (chat.get('name') == interested_chat_name):
            interested_chat = chat
            print('Chat ', interested_chat_name, 'found')

    if not interested_chat  :
        print('Chat', interested_chat_name, 'not found!!')

    for message in interested_chat.get('messages'):
        if message.get('type') == 'message' and isinstance(message.get('text'), str):
            i = i + 1 
            tmessage = telegramMessage(
                message.get('from'), 
                message.get('text'))
    print('numero messaggi puliti' , i)        
            
            


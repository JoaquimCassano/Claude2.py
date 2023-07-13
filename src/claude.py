import requests, auth


class Claude:
    def __init__(self, cookies:dict) -> None:
        '''COOKIES IS A DICTIONARY, THAT FOLLOWS THIS STRUCTURE: 
        { '__cf_bm':str, 
        'sessionKey':str, 
        'intercom-device-id-lupk8zyo':str, 
        'intercom-session-lupk8zyo':str }. 
        Conversation id is optional. It is used to "remember" the ai of a conversation. '''
        self.cookies = cookies


    def create_chat(self):
        '''Return a chat string UUID'''
        return requests.post("https://claude.ai/api/organizations/2ae460c1-0b38-495b-b8a5-b2c660490f2a/chat_conversations", cookies=self.cookies, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0"}).json()

    def ask(self, question:str, conversation_uuid:str=None):
        '''Return a json object with the answer'''
        last_message_index = 0
        if conversation_uuid == None:
            conversation_uuid = self.create_chat()
            conversation_uuid = conversation_uuid[0]['uuid']

        payload = {"completion":
                        {"prompt":question,
                        "timezone":"America/Sao_Paulo",
                        "model":"claude-2"},
                    "organization_uuid":"2ae460c1-0b38-495b-b8a5-b2c660490f2a","conversation_uuid":"49942b74-ffee-48bb-81ac-45aba4bcd7ab","text":question,"attachments":[]}
        requests.post('https://claude.ai/api/append_message', payload , cookies=self.cookies)
        while True:
            response = requests.get(f"https://claude.ai/api/organizations/2ae460c1-0b38-495b-b8a5-b2c660490f2a/chat_conversations/{conversation_uuid}", cookies=self.cookies, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0"})
            if response.status_code == 200:
                messages = response.json()['chat_messages'] ; messages = [msg for msg in messages if msg['sender'] == 'assistant']
                num_messages = messages[-1]['index']
                if num_messages != last_message_index:
                    return messages[-1]
                
        
if __name__ == '__main__':
    claude = Claude(auth.claude_cookies)
    print('starting chatting...')
    print(claude.ask("Olá! Tudo bem?", '735ec54e-e6d9-49e8-ae27-b563fd115bef'))
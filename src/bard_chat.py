from bardapi import Bard, ChatBard
import auth


bard = ChatBard(token=auth.bard_token)
print('connected. starting chat...')
bard.start()


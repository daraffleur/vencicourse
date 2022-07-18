# tc landing

# TELEGRAM API
1. Create Bot
2. Add Bot to group
3. curl  `https://api.telegram.org/bot<token>/getUpdates`
4. Find Chat ID (message - chat["id"]) 
4. Send msg to the group `curl  https://api.telegram.org/bot<token>/sendMessage -d text="A message from your bot" -d
chat_id=<id>`
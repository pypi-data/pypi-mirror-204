import random
import asyncio
from ShynaDatabase import Shdatabase
import telegram
import os


class NotifyBoss:
    s_data = Shdatabase.ShynaDatabase()
    result = False
    master_telegram_chat_id = os.environ.get('master_telegram_chat_id')
    message = ""
    status = False

    def notify_boss(self):
        try:
            self.s_data.default_database = os.environ.get('notify_db')
            self.s_data.query = "Select * from bot_msg_backup where status='False' order by count ASC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                print("Empty")
            else:
                for item in self.result:
                    print(item[3], item[4])
                    self.message = random.choice(str(item[4]).split("|"))
                    asyncio.run(self.bot_send_msg_to_master(bot_name=str(item[3])))
                    self.s_data.query = "UPDATE bot_msg_backup SET status='True' where count='"+str(item[0])+"'"
                    self.s_data.create_insert_update_or_delete()
        except Exception as e:
            print(e)

    async def bot_send_msg_to_master(self, bot_name):
        bot = telegram.Bot(token=os.environ.get(bot_name))
        await bot.send_message(chat_id=self.master_telegram_chat_id, text=str(self.message))


if __name__ == '__main__':
    NotifyBoss().notify_boss()

import ast
import discord
import requests

from discord_user import *

from config.common_logger import *
from config.environ_config import env

from hatena import hatebu_utils
from a3rt import talk_api


class GenericRoomAction(object):
    def __init__(self, message):
        app_logger.info("GenericRoomAction object has created")
        self.message = message
        self.message_first_query = self.message.content.split(" ")[1]
        self.post_items_arr = []
        self.get_exp = 0

        self.discord_user = GenericDiscordUser(self.message)

    def return_generic_post_items(self):
        if self.message_first_query == "登録":
            self.create_chibamoku_user()

        elif self.message_first_query == "ステータス":
            self.check_status()

        elif self.message_first_query == "hatebu":
            self.hatebu()
        
        else:
            self.get_exp = 100
            self.update_userdata()
            # self.talk_reply()

        return self.post_items_arr

    def create_chibamoku_user(self):
        app_logger.info("CALL : create_chibamoku_user()")

        response = self.discord_user.create_new_discord_user()

        if response.status_code == 201:
            self.post_items_arr = ["ちばもく会へようこそ！\n新規ユーザー登録が完了しました！"]

        else:
            """
            > response.text
            '{"discord_id":["この discord id を持った chiba moku user が既に存在します。"]}'
            """
            self.post_items_arr = ast.literal_eval(response.text)["discord_id"]
    
        # except Exception as e:
        #     #TODO: discord 側にも、エラーをDiscord通知する機能を実装する
        #     # error_notify.error_notifier(sys.exc_info()[0], e.args)
        #     logger.error("Unexpected error {}\n {}".format(sys.exc_info()[0], e.args))

        return

    def check_status(self):
        app_logger.info("CALL : check_status()")

        response = self.discord_user.get_own_userdata()

        if response.status_code == 200:
            self.post_items_arr = [
                self.message.author.mention + " さんのステータスを表示します。" + "\n" \
                + "現在のレベル ： " + str(self.discord_user.level) + "\n" \
                + "総獲得経験値 : " + str(self.discord_user.total_exp) + "\n" \
                + "次のレベルまで : " + str(self.discord_user.next_level_exp - self.discord_user.total_exp) + "\n" \
                + "この調子で頑張りましょう！"
            ]

        else:
            self.post_items_arr = [ast.literal_eval(response.text)["detail"]]

        # except Exception as e:
        #     # error_notify.error_notifier(sys.exc_info()[0], e.args)
        #     logger.error("Unexpected error {}\n {}".format(sys.exc_info()[0], e.args))

        return
    
    def talk_reply(self):
        app_logger.info("CALL : talk_reply()")
        query = self.message_first_query
        reply = talk_api.call_talk_api(query)

        self.post_items_arr.append(reply)
        return

    def hatebu(self):
        app_logger.info("CALL : hatebu()")
        items = hatebu_utils.return_tophatebu_itposts()

        self.post_items_arr = [item[0] + ":" + item[1] for item in items]
        return


    def update_userdata(self):
        app_logger.info("CALL : update_userdata()")
    
        # レベルアップ判定
        if self.discord_user.is_level_up(self.get_exp):
            self.post_items_arr = [
                self.message.author.mention + " さんがレベルアップしました！" + "\n" \
                + "現在のレベル ： " + str(self.discord_user.level) + "\n" \
                + "総獲得経験値 : " + str(self.discord_user.total_exp) + "\n" \
                + "次のレベルまで : " + str(self.discord_user.next_level_exp) + "\n" \
                + "この調子で頑張りましょう！"
            ]

        else:
            self.check_status()
       
        return

    def __del__(self):
        app_logger.info("CALL : Destructor")
        pass
        

class Moku2RoomAction(GenericRoomAction):
    def return_moku2_post_items(self):
        if self.message_first_query == "プロパティ":
            self.post_items_arr = ["ここはもくもく会の部屋です！\nもくもく会に参加すると手に入る経験値は 100 EXP です！"]
        
        else:
            self.return_generic_post_items()

        return self.post_items_arr


class Asakatsu2RoomAction(Moku2RoomAction):
    def return_post_items(self):
        if self.message_first_query == "プロパティ":
            self.post_items_arr = ["ここは朝活もくもく会の部屋です！\n朝活もくもく会に参加すると手に入る経験値は 50 EXP です！"]
        
        else:
            self.return_moku2_post_items()

        return self.post_items_arr

if __name__ == "__main__":
    pass
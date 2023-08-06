import os
from ShynaDatabase import Shdatabase
from Shynatime import ShTime
from nltk import sent_tokenize
from google_speech import Speech
from ShynaTelegramBotNotification import BotNotify


class ShynaSpeak:
    """
    Using google_speech library https://pypi.org/project/google-speech/ and nltk to tokenize every sentence and speak.
    make sure the dependencies for google_speech is installed before using this class.
    sox effect are in place, keep Shyna voice same across the devices.

    There are two methods:
     shyna_speaks: provide sentence(s) to speak out loud
     test_shyna_speaks: run to test everything working fine

    """
    lang = "en"
    sox_effects = ("speed", "1.0999",)
    text = "Hey! Shiv? I hope you can listen to me otherwise doesn't matter what I say or do, you will be only " \
           "complaining"
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    priority = [2, 2, 2]
    s_bot = BotNotify.BotShynaTelegram()

    def shyna_speaks(self, msg):
        try:
            son = self.speak_or_not()
            print(son)
            if int(son) in self.priority:
                for i in sent_tokenize(msg):
                    speech = Speech(i, self.lang)
                    speech.play(self.sox_effects)
            else:
                for i in sent_tokenize(msg):
                    self.s_bot.message = i
                    self.s_bot.bot_send_msg_to_master()
        except Exception as e:
            self.s_bot.message = "Exception at shyna_speak " + str(e)
            print(e)
        finally:
            self.s_data.set_date_system(process_name="rasp_speak_system")

    def test_shyna_speaks(self):
        self.priority = [0, 1, 2]
        self.shyna_speaks(self.text)

    def speak_or_not(self):
        # Flow 5. it checks what is the last status I send her. it is morning, silent, or sleep and return
        # accordingly. Default is set to awake.
        result = "awake"
        try:
            self.s_data.default_database = os.environ.get('alarm_db')
            self.s_data.query = "SELECT greet_string FROM greeting order by count DESC limit 1;"
            cursor = self.s_data.select_from_table()
            if str(cursor).__contains__('Exception') or str(cursor).__contains__('Empty'):
                pass
            else:
                for row in cursor:
                    greet_string = str(row[0])
                    if len(greet_string) > 0:
                        if str(greet_string).lower() == 'wake':
                            result = 2
                        if str(greet_string).lower() == 'silent':
                            result = 1
                        if str(greet_string).lower() == 'sleep':
                            result = 0
                    else:
                        result = 'awake'
        except Exception as e:
            print(e)
            result = 2
            self.s_bot.message = "Exception at speak_or_not " + str(e)
            self.s_bot.bot_send_msg_to_master()
            self.s_bot.message = "Setting speak priority to high"
            self.s_bot.bot_send_msg_to_master()
        finally:
            return result

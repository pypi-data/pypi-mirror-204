import os
import random
from ShynaDatabase import Shdatabase
from google_speech import Speech
from nltk import sent_tokenize


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
    priority = [2, 2, 2]

    def shyna_speaks(self, msg):
        try:
            son = self.speak_or_not()
            msg = random.choice(str(msg).split("|"))
            if str(son) in self.priority:
                for i in sent_tokenize(msg):
                    speech = Speech(i, self.lang)
                    speech.play(self.sox_effects)
            else:
                self.s_data.message = msg
                self.s_data.bot_send_msg_to_master()
        except Exception as e:
            self.s_data.message = "Exception at shyna_speak " + str(e)
            self.s_data.bot_send_msg_to_master()
            print(e)
        finally:
            self.s_data.set_date_system(process_name="rasp_speak_system")

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
            self.s_data.message = "Exception at speak_or_not " + str(e)
            self.s_data.bot_send_msg_to_master()
            self.s_data.message = "Setting speak priority to high"
            self.s_data.bot_send_msg_to_master()
        finally:
            return result

    def get_sentence(self):
        try:
            self.s_data.default_database = os.environ.get('notify_db')
            self.s_data.query = "SELECT * from speak_sentence where status='False' order by count DESC"
            result = self.s_data.select_from_table()
            if str(result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in result:
                    self.s_data.default_database = os.environ.get('notify_db')
                    self.s_data.query = "UPDATE speak_sentence set status='True' where count = '" + str(item[0]) + "'"
                    self.s_data.create_insert_update_or_delete()
                    self.priority = list(str(item[6]).strip("[]").split(","))
                    self.shyna_speaks(msg=item[3])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ShynaSpeak().get_sentence()

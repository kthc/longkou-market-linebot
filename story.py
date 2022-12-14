from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent,
    UnfollowEvent,
    MessageEvent,
    TextMessage,
    TextSendMessage,
    StickerSendMessage,
    LocationMessage,
    LocationSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    QuickReply,
    QuickReplyButton,
    PostbackAction,
    PostbackEvent,
    FollowEvent,
    DatetimePickerAction,
    MessageAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    AudioSendMessage,
    VideoSendMessage,
    ImageSendMessage,
    Sender
)
import re
import random
from app_global import APP_URL
from story_data_collection import roles, audio_dict, video_dict, img_dict


class Story:
    def __init__(self, *args, **kwargs) -> None:
        self.username = ''
        self.story_name = ''
        self.id = -1
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_wrong = []

    def get_pre_message(self):
        return [TextSendMessage(text=text) for text in self.pre_messages]

    def get_main_message(self):
        return [TextSendMessage(text=text) for text in self.main_messages]

    def get_post_message(self):
        return [TextSendMessage(text=text) for text in self.post_messages]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if self.ans == ans or force_correct:
            return True, [TextSendMessage(text=msg, sender=None) for msg in self.post_messages]
        else:
            return False, [TextSendMessage(text=msg, sender=None) for msg in self.reply_messages_wrong]


class SimplePostbackStory(Story):
    def __init__(self, id, *args, msg='', button_label='', text_after_clicked='', sender_name='', **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.data = '$Pass'
        self.label = button_label
        self.display_text = text_after_clicked
        self.main_messages = msg
        self.sender_name = sender_name

    def get_main_message(self):
        if self.display_text == '' or self.display_text is None:
            self.display_text = self.label
        return [
            TextSendMessage(
                text=self.main_messages,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None)
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class AudioStory(Story):
    def __init__(self, id, *args, audio_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.audio_name = audio_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        audio = audio_dict.get(self.audio_name, None)
        if audio_dict.get(self.audio_name, None) is None:
            audio = audio_dict.get('not_found', None)
        print(audio)
        return [
            AudioSendMessage(
                original_content_url=audio['url'],
                duration=audio['duration'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class VideoStory(Story):
    def __init__(self, id, *args, video_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.video_name = video_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        video = video_dict.get(self.video_name, None)
        return [
            VideoSendMessage(
                original_content_url=video['url'],
                preview_image_url=video['preview'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class ImageStory(Story):
    def __init__(self, id, *args, image_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.image_name = image_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        image = img_dict.get(self.image_name, None)
        return [
            ImageSendMessage(
                original_content_url=image['url'],
                preview_image_url=image['preview'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Welcome(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '??????')
        self.id = 0
        self.story_name = 'Welcome'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = [
            f'''?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????sos??????????????????reset???????????????''']
        self.ans = 'go'
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['''??????! ???????????????????????????????????????????????????"GO"???????????????????????????!''']

    def get_main_message(self):
        return [
            TextSendMessage(text=self.main_messages[0]),
            TextSendMessage(
                text='Hi ??????????????????????????????',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                data='$Welcom_Bypass', label='????????????', display_text='???????????????????????????????????????')
                        )
                    ]
                )
            )
        ]


    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if self.ans == ans.lower() or force_correct or ans == '$Welcom_Bypass':
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]
        else:
            if retry_count == 3:
                return False, [TextSendMessage(text='?????????????????????GO??????????????????????????????????????????!')]
            elif retry_count > 3:
                return False, [TextSendMessage(text='??????????????????????????????!???????????????????????????GO??????????????????....')]
            return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]


class Question1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 90
        self.story_name = '?????????'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '??????3'
        self.reply_messages_wrong = [
            "??????????????????????????????",
            "???????????????????????????!",
            "????????????????????????",
            "?????????????????????!",
            "???????????????!"
        ]

    def get_main_message(self):
        return [
            TextSendMessage(
                text='https://youtu.be/Bwy8MbB1oZo',
                # original_content_url=video_dict['Q1']['url'], preview_image_url=video_dict['Q1']['preview'], sender=roles.get(
                #     "BG", None),
                sender=roles.get("BG", None),
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='??????', text='?????????????????????')
                        )
                    ]
                )),
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question1_1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 901
        self.story_name = '?????????'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '2'
        self.reply_messages_wrong = [
            "?????????????????????!"
        ]

    def get_main_message(self):
        return [
            ImageSendMessage(
                original_content_url=img_dict['Q1']['url'], preview_image_url=img_dict['Q1']['preview'], sender=roles.get("BG", None)),
            TextSendMessage(text='???????????????????????????!',
                            sender=roles.get("BG", None)),
            TextSendMessage(
                text='(????????????????????? 1~8 ???????????????)', sender=roles.get("BG", None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''??????????????????????????????{self.ans}''')]
        elif ans == '2':
            return True, []
        else:
            return False, [TextSendMessage(text=self.reply_messages_wrong[0])]


class OneHourLater(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        '''simple_video_maker(10, video_name='OneHourLater', button_label='??????????????????', text_after_clicked='???????????????????????????????????????????????????', sender_name="BG"),'''
        self.id = 902
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = "BG"
        self.video_name = 'OneHourLater'
        self.label = '??????????????????'
        self.display_text = '???????????????????????????????????????????????????'

    def get_main_message(self):
        video = video_dict.get(self.video_name, None)
        return [
            TextSendMessage(text='?????? 1?????????  ???',
            quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                            sender=roles.get("BG", None)),
            # VideoSendMessage(
            #     original_content_url=video['url'],
            #     preview_image_url=video['preview'],
            #     quick_reply=QuickReply(
            #         items=[
            #             QuickReplyButton(
            #                 action=MessageAction(
            #                     label=self.label, text=self.display_text)
            #             )
            #         ]
            #     ),
            #     sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question2(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 91
        self.story_name = '?????????'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '??????'
        self.reply_messages_wrong = [
            "???????????????!",
            "????????????????????????"
        ]

    def get_main_message(self):
        return [
            TextSendMessage(
                # original_content_url=video_dict['Q2']['url'],
                # preview_image_url=video_dict['Q2']['preview'],
                text='https://youtu.be/FkJc2h2uEn4',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='??????', text='??????????????????')
                        )
                    ]
                ),
                sender=roles.get("BG", None)),
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question2_1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 911
        self.story_name = '?????????'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '??????'
        self.reply_messages_wrong = [
            "???????????????!",
            "????????????????????????"
        ]

    def get_main_message(self):
        return [
            ImageSendMessage(
                original_content_url=img_dict['Q2']['url'], preview_image_url=img_dict['Q2']['preview'], sender=roles.get("BG", None)),
            TextSendMessage(text='??????????????????????????????',
                            sender=roles.get("BG", None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        rnd = random.random()
        rnd_reply_idx = 1 if rnd > 0.5 else 0
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''???????????????????????????{self.ans}''')]
        if type(ans) is str:
            if ans in ['??????', '????????????']:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]


class Question3(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 92
        self.story_name = '?????????'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '62???'
        self.reply_messages_wrong = [
            "???????????????!",
            "????????????????????????"
        ]

    def get_main_message(self):
        return [
            # VideoSendMessage(
            #     original_content_url=video_dict['Q3']['url'], preview_image_url=video_dict['Q3']['preview'], sender=roles.get(
            #         "BG", None)
            # ),
            TextSendMessage(
                text='https://youtu.be/aVUP9WBsoTc',
                sender=roles.get("BG", None)
            ),
            TextSendMessage(text='?????????____???????????????',
                            sender=roles.get("BG", None),
                            quick_reply=QuickReply(
                                items=[
                                    QuickReplyButton(
                                        action=PostbackAction(
                                            data='$Q3_Bypass', label='???????????????', display_text='''- ??????????????????????????????????????????\n- ?????????????????????2???\n- 2??????????????????????????????????????????10???\n- ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????\n- ??????????????????????????????2??????????????????????????????????????????''')
                                    )
                                ]
                            ))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        rnd = random.random()
        rnd_reply_idx = 1 if rnd > 0.5 else 0
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''???????????????????????????{self.ans}''')]
        if type(ans) is str:
            if ans in ['62', '62???']:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]


class WakeByPhone(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        '''story.simple_audio_maker(25, audio_name='16', sender_name='??????_09', button_label='??????', text_after_clicked='????????????????????????????????????????????????????????????????????????'),'''
        self.id = 923
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = "BG"
        self.video_name = 'WakeByPhone'
        self.label = '??????'
        self.display_text = '????????????????????????????????????????????????????????????????????????'

    def get_main_message(self):
        audio = audio_dict.get('16', None)
        if audio_dict.get('16', None) is None:
            audio = audio_dict.get('not_found', None)
        return [
            TextSendMessage(text='?????? ?????????????????????  ??? ',
                            sender=roles.get("BG", None)),
            AudioSendMessage(
                original_content_url=audio['url'],
                duration=audio['duration'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='??????', text='????????????????????????????????????????????????????????????????????????')
                        )
                    ]
                ),
                sender=roles.get('??????_09', None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question4(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 93
        self.story_name = '???????????????'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = 'present'
        self.reply_messages_wrong = [
            "???????????????!",
            "????????????????????????"
        ]

    def get_main_message(self):
        return [
            TextSendMessage(text='''prank=??????\nsralt=??????\nsrure=??????\n?????????=_____''',
                            sender=roles.get("BG", None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        rnd = random.random()
        rnd_reply_idx = 1 if rnd > 0.5 else 0
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''???????????????{self.ans}''')]
        if type(ans) is str:
            if ans.lower().strip() == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]


class Question5(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 94
        self.story_name = '????????????'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '7533967'
        self.reply_messages_wrong = [
            "???????????????!",
            "????????????????????????"
        ]

    def get_main_message(self):
        return [
            AudioSendMessage(
                original_content_url=audio_dict['Q5']['url'],
                duration=audio_dict['Q5']['duration'],
                sender=roles.get('??????', None),
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                data='$Q5_Bypass', label='??????...', display_text='''?????????????????????????????????????????????\n???https://onlinetonegenerator.com/dtmf.html''')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []

class Question5_1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 941
        self.story_name = '????????????'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '7533967'
        self.reply_messages_wrong = [
            "???????????????!",
            "????????????????????????"
        ]

    def get_main_message(self):
        return [
            AudioSendMessage(
                original_content_url=audio_dict['24']['url'],
                duration=audio_dict['24']['duration'],
                sender=roles.get('??????', None),
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                data='$Q5_Bypass', label='??????', display_text='''????????????????????????...''')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        rnd = random.random()
        rnd_reply_idx = 1 if rnd > 0.5 else 0
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''???????????????{self.ans}''')]
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                if retry_count == 3:
                    return False, [
                        TextSendMessage(
                            text='...',
                            quick_reply=QuickReply(
                                items=[
                                    QuickReplyButton(
                                        action=PostbackAction(
                                            data='$Q5_Bypass', label='???????????????', display_text='''???????????????????????????7533??????????????????????????????????????????????????????''')
                                    )
                                ]
                            )
                        ),
                    ]
                elif retry_count > 3:
                    False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]

class Ending(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '??????')
        self.id = 99
        self.story_name = 'Ending'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["????????????"]
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['????????????????????????!']

    def get_main_message(self):
        main_msg = [
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='???????????????',
                    text='?????????????????????',
                    actions=[
                        MessageTemplateAction(
                            label='???????????????',
                            text=f'???????????????:https://sites.google.com/view/kthc?pli=1'
                        ),
                        MessageTemplateAction(
                            label='????????????',
                            text=f'????????????:https://drive.google.com/file/d/1KG0nVTn0Y9sMRT-go2oPpwWtqB4QIEU5/view'
                        ),
                        MessageTemplateAction(
                            label='???????????????',
                            text=f'???????????????:https://youtu.be/ytUI_zoh0pA'
                        ),
                        MessageTemplateAction(
                            label='??????????????????',
                            text=f'??????????????????:https://youtu.be/5_GfMCdeyf4'
                        ),
                    ]
                )
            )
        ]
        return main_msg

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return False, []


def simple_msg_maker(id, msg='', button_label='', text_after_clicked='', sender_name=''):
    return SimplePostbackStory(id, msg=msg, button_label=button_label, text_after_clicked=text_after_clicked, sender_name=sender_name)


def simple_audio_maker(id, audio_name='', sender_name='', button_label='', text_after_clicked='',):
    return AudioStory(id, audio_name=audio_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)


def simple_video_maker(id, video_name='', sender_name='', button_label='', text_after_clicked='',):
    return VideoStory(id, video_name=video_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)


def simple_image_maker(id, image_name='', sender_name='', button_label='', text_after_clicked='',):
    return ImageStory(id, image_name=image_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)

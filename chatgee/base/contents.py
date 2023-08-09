# -*- coding: utf-8 -*-
"""
Contents Generator For Kakaotalk Messages
"""

from base.module_kakaotalk import ChatGee_KakaoTalk


# Greetings
def generate_greetings(ChatGee_Config, content):
    """New user message"""
    response = ChatGee_KakaoTalk.insert_card(
        title=ChatGee_Config['CONTENTS']['GREETINGS']['TITLE'],
        description=ChatGee_Config['CONTENTS']['GREETINGS']['TEXTS'])
    try:
        content = content['userRequest']['utterance']
        content = ''.join(str(e) for e in content)
        response = ChatGee_KakaoTalk.insert_button_text(response, '📓 사용설명서 보기', '📓 사용설명서')
        response = ChatGee_KakaoTalk.insert_button_text(response, '이전 말 다시 적기 ✍🏻', content)
    except KeyError:
        response = ChatGee_KakaoTalk.insert_button_text(response, '📓 사용설명서 보기', '📓 사용설명서')
        response = ChatGee_KakaoTalk.insert_button_text(response, '넌 뭐니??!', "넌 뭐니??!")

    return response

# Advertisement
def generate_advertisement(ChatGee_Config, response):
    """Advertisement message"""
    response = ChatGee_KakaoTalk.plus_card(response, title='',
                                description=ChatGee_Config['CONTENTS']['ADVERTISEMENT']['TEXTS'])
    response = ChatGee_KakaoTalk.insert_button_url(
        response, '더알고 싶으시면 🚀', ChatGee_Config['CONTENTS']['ADVERTISEMENT']['LINK'])
    if len(ChatGee_Config['CONTENTS']['SUPPORT_LINK']) != 0:
        ChatGee_KakaoTalk.insert_button_url(
            response, '후원하기🧋🧋', ChatGee_Config['CONTENTS']['SUPPORT_LINK'])

    return response

# Document
def generate_documents(ChatGee_Config):
    """How-to Document message"""
    response = ChatGee_KakaoTalk.insert_carousel_card(title = '📓 사용설명서 for 🌱🐤',
                                    description = '안녕하세요!! 운동을 시작한 당신에게 도움이 될 기능을 알려드리겠습니다.😎👀',
                                    width=30, height=None)

    response = ChatGee_KakaoTalk.plus_carousel_card(response, title = "",
                                    description = ChatGee_Config['CONTENTS']['EXPLAIN']['TEXTS'])
    if len(ChatGee_Config['CONTENTS']['SUPPORT_LINK']) != 0:
        ChatGee_KakaoTalk.insert_carousel_button_url(
            response, '후원하기🧋🧋', ChatGee_Config['CONTENTS']['SUPPORT_LINK'])
        
    response = ChatGee_KakaoTalk.plus_carousel_card(response,title = '',
                                    description =
                                    '🤖 내 정보입력을 통해 맞춤형 답변을 받을 수 있어요!\n'
                                    '   ‣ 나이, 성별, 키, 몸무게를 입력하시면\n'
                                    '   ‣ 당신에게 맞는 정보를 제공해드릴게요\n'
                                    ,width=None, height=None)
    ChatGee_KakaoTalk.insert_carousel_button_text(response, '내 정보입력', '내 정보입력')

    response = ChatGee_KakaoTalk.plus_carousel_card(response,title = '',
                                    description =
                                    '🤖 헬궁에게 루틴 추천을 받아보세요\n'
                                    '   ‣ 저에게 루틴 추천해줘라고 물어보시면\n'
                                    '   ‣ 당신에게 맞는 루틴을 추천해드릴게요\n'
                                    '💩 만약 너무 어렵거나 쉽다면 다시 질문해 주세요\n'
                                    ,width=None, height=None)
    ChatGee_KakaoTalk.insert_carousel_button_text(response, '맞춤형 운동 루틴 추천', '맞춤형 운동 루틴 추천')


    response = ChatGee_KakaoTalk.plus_carousel_card(response, title = "",
                                    description =
                                    '운동만큼 먹는 것도 중요하겠죠?\n'
                                    '저에게 식단 추천해줘라고 물어보시면\n'
                                    '당신에게 맞는 식단을 추천해드릴게요😊!,',
                                    image_url=None, width=None, height=None)
    ChatGee_KakaoTalk.insert_carousel_button_text(response, '맞춤형 식단 추천', '맞춤형 식단 추천')
    
    response = ChatGee_KakaoTalk.plus_carousel_card(response, title = "",
                                    description =
                                    '본격적으로 운동을 시작한 당신\n'
                                    '   ‣저에게 다이어트 식품, 닭가슴살 추천해줘 \n'
                                    '   라고 물어보시면 당신에게 맞는 상품을 알려드릴게요 \n',
                                    image_url=None, width=None, height=None)
    ChatGee_KakaoTalk.insert_carousel_button_text(response, '닭가슴살 추천해줘', '닭가슴살 추천')
    ChatGee_KakaoTalk.insert_carousel_button_text(response, '다이어트 식품 추천해줘', '다이어트 식품 추천')
    
    response = ChatGee_KakaoTalk.plus_carousel_card(response, title = "",
                                    description =
                                    '물론 당신의 집 주변 헬스장도 알려드립니다.\n'
                                    'OO시 OO동 근처 헬스장 추천해줘라고 질문해주시면\n'
                                    '저희가 주변 헬스장을 찾아드릴게요\n',
                                    image_url=None, width=None, height=None)
    ChatGee_KakaoTalk.insert_carousel_button_text(response, '헬궁과 대화하기', '헬궁과 대화하기')
    
    response = ChatGee_KakaoTalk.plus_carousel_card(response, title = "",
                                    description =
                                    '🧠 헬궁은 이전 대화를 기억해요\n'
                                    '   ‣ 최대 10개 대화 핑퐁을 기억 🤓\n'
                                    '   ‣ 💫 새로운 시작 = 이전기억 삭제',
                                    image_url=None, width=None, height=None)
    ChatGee_KakaoTalk.insert_carousel_button_text(response, '💫 새로운 시작', '💫 새로운 시작')

    return response

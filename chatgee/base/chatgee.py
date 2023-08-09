# -*- coding: utf-8 -*-
"""
ChatGee Module Class Object
"""

import queue as q
import threading
import time
from datetime import datetime
import requests

import tiktoken

from base.module_database import ChatGee_DB
from base.module_openai import ChatGee_OpenAI
from base.module_kakaotalk import ChatGee_KakaoTalk
from base.contents import generate_greetings, generate_advertisement, generate_documents

class ChatGeeOBJ:
    """ChatGee Module Class Object"""

    def __init__(self, ChatGee_Config):
        # Save Configuration
        self.ChatGee_Config = ChatGee_Config
        # Generate ChatGee Database and Initiate
        self.DB = ChatGee_DB()
        self.DB.init_db(self.ChatGee_Config['DATABASE']['DB_PREFIX'])
        # OpenAI Encoding to count tokens
        self.encoding = tiktoken.encoding_for_model(self.ChatGee_Config['OPEN_AI']['MODEL'])
        self.system_prompt_tokens_estimate = \
            len(self.encoding.encode(self.ChatGee_Config['SETTINGS']['SYSTEM_PROMPT'])) \
            + 350  # 320 by ChatGee Template + 30 for safety
        self.max_user_prompt_history_tokens = int(4096/2) - self.system_prompt_tokens_estimate
        # Set OpenAI Module Configuratoin
        self.OpenAI = ChatGee_OpenAI(
            api_key = self.ChatGee_Config['OPEN_AI']['API_KEY'],
            model = self.ChatGee_Config['OPEN_AI']['MODEL'],
            hyper_top_p = self.ChatGee_Config['OPEN_AI']['HYPER_TOP_P'],
            hyper_temperature = self.ChatGee_Config['OPEN_AI']['HYPER_TEMPERATURE'],
            max_user_prompt_history_tokens = self.max_user_prompt_history_tokens,
            system_prompt_tokens_estimate = self.system_prompt_tokens_estimate,
            openai_api_error_log = self.ChatGee_Config['OPEN_AI']['OPENAI_API_ERROR_LOG']
        )
        # CallbackOptionFlag
        self.callback_option = self.ChatGee_Config['SETTINGS']['CALLBACK']
        self.callbackUrl = ''

    # Get Usage Count
    def get_usage_count(self, userid):
        """Get Usage Count of the user"""
        user_data = self.DB.get_user_data_by_room(userid)
        user_data = list(user_data[0])
        return user_data[4]
    
    # # Get Usage Count
    # def createImage(self, userid):
    #     """Get Usage Count of the user"""
    #     user_data = self.DB.get_user_data_by_room(userid)
    #     user_data = list(user_data[0])
    #     prompt = request.args.get('prompt', '')  # Get the 'prompt' parameter from the query string
    #     with autocast(device):
    #         image = pipe(prompt, guidance_scale=8.5).images[0]

    #     buffer = BytesIO()
    #     image.save(buffer, format="PNG")
    #     imgstr = base64.b64encode(buffer.getvalue())

    #     return Response(content=imgstr, mimetype="image/png")

    
    def myData_received(self, content):
        # Check user
        new_user_flag = False
        userid = content['userRequest']['user']['id'] # userid is saved as 'room' in user_data.db
        isFriend = content['userRequest']['user']['properties'].get('isFriend', False)
        myAge = content["action"]["detailParams"].get("myAge", {}).get("value", None)
        myGender = content["action"]["detailParams"].get("myGender", {}).get("value", None)
        myHeight = content["action"]["detailParams"].get("myHeight", {}).get("value", None)
        myWeight = content["action"]["detailParams"].get("myWeight", {}).get("value", None)
        
        # Read user data (room, member, count, total_count)
        user_data = self.DB.get_user_data_by_room(userid)

        # If new user, save guest template
        if user_data is not None:
            if len(user_data) == 0:
                self.DB.save_user_data(userid, isFriend, 1, 0, myAge, myGender, myHeight, myWeight)
        else:
            # If user exists, update the data (only for non-None values)
            self.DB.save_user_data(userid, isFriend, user_data[3], user_data[4], myAge, myGender, myHeight, myWeight)

        # Retrieve updated user data after saving/updating
        user_data = list(self.DB.get_user_data_by_room(userid)[0])
        response = ChatGee_KakaoTalk.insert_card('등록이 완료되었습니다', f'안녕하세요! {myAge}살, {myGender}으로 설정이 완료되었습니다')
        return response
    
    def myAge_received(self, content):
        # Check user
        userid = content['userRequest']['user']['id'] # userid is saved as 'room' in user_data.db
        myAge = content['userRequest']['utterance']
        # myAge = content["action"]["detailParams"].get("myAge", {}).get("value", None)
        isFriend = content['userRequest']['user']['properties'].get('isFriend', False)

        # Read user data (room, member, count, total_count)
        user_data = self.DB.get_user_data_by_room(userid)

        # If new user, save guest template
        if user_data is not None:
            if len(user_data) == 0:
                self.DB.save_user_age(userid, isFriend, 1, 0, myAge)
        else:
            # If user exists, update the age (only for non-None values)
            self.DB.save_user_age(userid, isFriend, user_data[3], user_data[4], myAge)
        # If user exists, update the data (only for non-None values)

        # Retrieve updated user data after saving/updating
        response = ChatGee_KakaoTalk.insert_card('등록이 완료되었습니다', f'안녕하세요!  {myAge}으로 설정이 완료되었습니다')
        return response

    def myGender_received(self, content):
        # Check user
        userid = content['userRequest']['user']['id'] # userid is saved as 'room' in user_data.db
        myGender = content["action"]["detailParams"].get("myGender", {}).get("value", None)
       
        self.DB.save_user_gender(userid, myGender)

        # Retrieve updated user data after saving/updating
        response = ChatGee_KakaoTalk.insert_card('등록이 완료되었습니다', f'안녕하세요!  {myGender}으로 설정이 완료되었습니다')
        return response
    
    def myHeight_received(self, content):
        # Check user
        userid = content['userRequest']['user']['id'] # userid is saved as 'room' in user_data.db
        myHeight = content['userRequest']['utterance']
        # myHeight = content["action"]["detailParams"].get("myHeight", {}).get("value", None)
        isFriend = content['userRequest']['user']['properties'].get('isFriend', False)
        

        # If user exists, update the data (only for non-None values)
        self.DB.save_user_height(userid, myHeight)

        # Retrieve updated user data after saving/updating
        response = ChatGee_KakaoTalk.insert_card('등록이 완료되었습니다', f'안녕하세요!  {myHeight}으로 설정이 완료되었습니다')
        return response
    
    def myWeight_received(self, content):
        # Check user
        new_user_flag = False
        userid = content['userRequest']['user']['id'] # userid is saved as 'room' in user_data.db
        myWeight = content['userRequest']['utterance']

        # myWeight = content["action"]["detailParams"].get("myWeight", {}).get("value", None)
        isFriend = content['userRequest']['user']['properties'].get('isFriend', False)
        

        # If user exists, update the data (only for non-None values)
        self.DB.save_user_weight(userid, myWeight)

        # Retrieve updated user data after saving/updating
        response = ChatGee_KakaoTalk.insert_card('등록이 완료되었습니다', f'안녕하세요!  {myWeight}으로 설정이 완료되었습니다')
        return response
    
    
    # 이부분이 채팅 받으면 content로 내용이 받아와서 처리하는 부분
    # ----- Flask Prompt Response Function ----- #
    def prompt_received(self, content):
        # content가 request.json()임
        """Process the prompt received from Flask"""
        run_flag = False
        start_time = time.time()

        # Get CallbackUrl from Kakaotalk Request
        callback_flag = False
        if self.callback_option:
            self.callbackUrl = content['userRequest']['callbackUrl']
            callback_flag = True

        # Check user
        new_user_flag = False
        userid = content['userRequest']['user']['id'] # userid is saved as 'room' in user_data.db
        isFriend = content['userRequest']['user']['properties'].get('isFriend', False)

        # Read user data (room, member, count, total_count)
        user_data = self.DB.get_user_data_by_room(userid)
        # If new user, save guest template
        if user_data is not None:
            if len(user_data) == 0:
                # # 이부분에서 나이 성별 키 몸무게 등을 받아오고 db에 저장하는 함수 실행 하면 될듯
                # params_ask_age = content["action"]["detailParams"]["myAge"]["value"]
                # params_ask_gender = content["action"]["detailParams"]["ask_gender"]["value"]
                # params_ask_height = content["action"]["detailParams"]["ask_height"]["value"]
                # params_ask_weight = content["action"]["detailParams"]["ask_weight"]["value"]
                # # res_ask_age = re.sub(r"[^0-9]", "", params_ask_age)
                # # res_ask_gender = re.sub(r"[^0-9]", "", params_ask_gender)
                # self.DB.save_user_data(userid, isFriend, 1, 0, params_ask_age, params_ask_gender, params_ask_height, params_ask_weight)

                self.DB.save_user_data(userid, isFriend, 1, 0)
                new_user_flag = True
        user_data = list(self.DB.get_user_data_by_room(userid)[0])
        previous_friendship = user_data[2]
        self.DB.save_user_data(userid, isFriend, user_data[3], user_data[4])
        user_data = list(self.DB.get_user_data_by_room(userid)[0])
        if previous_friendship is False and isFriend is True:
            self.DB.save_conversation_one_above("user", userid, \
            "💞💕 우린 이제 친구가 되었어! 너무너무 반가워! 앞으로도 너랑 이야기할 것이 기대되!" \
            "우리가 친구가 된게 너무너무 기쁘다고 앞으로 두번은 더 이야기해줘!")

        # Greetings Card if new user
        if new_user_flag:
            response = generate_greetings(self.ChatGee_Config, content)
        # For normal user
        else:
            run_flag = True

        # Check membership
        if user_data[2] is False \
            and user_data[4] > self.ChatGee_Config['SETTINGS']['NO_FRIEND_USE_LIMIT']:
            response = ChatGee_KakaoTalk.insert_card(title='우리 친구해요 🤝💞💞',
                description='제 프로필에서 오른쪽 상단의 노란색 친구추가버튼을 클릭하면 우린 친구가 됩니다! 🙏🏻🙏🏻💗')
            chat_history = self.DB.get_conversation_latest(userid, limit=1)
            response = ChatGee_KakaoTalk.insert_button_text(
                response, '이전 말 다시적기 ✍🏻', chat_history[0][3])
            run_flag = False

        #  u"검색" in content 
        # Find Special Commands
        if content['userRequest']['utterance'] == '📓 사용설명서':
            response = generate_documents(self.ChatGee_Config)
            run_flag = False

        # Clear Chat History
        if content['userRequest']['utterance'] == '💫 새로운 시작':
            self.DB.delete_conversation_data(userid)
            response = ChatGee_KakaoTalk.insert_text("대화한적이..있었..없었습니다...\n🪄💫✨💆‍♂️🦄🌈🌟🎉🍭🎠")
            run_flag = False
        # # Clear Chat History
        # if content['userRequest']['utterance'] == '내 정보 입력':
        #     # self.DB.delete_conversation_data(userid)
        #     response = ChatGee_KakaoTalk.insert_text("대화한적이..있었..없었습니다...\n🪄💫✨💆‍♂️🦄🌈🌟🎉🍭🎠")
        #     run_flag = False
        check_req = [
            ["식단", "메뉴", "식사"],
            ["루틴", "운동 시간표", "운동 일정"],
            ["자세"]
        ]
        # if content["userRequest"]["utterance"] in check_req[0]:
            # 이제 module_kakaotalk에다가 meal이라는 함수 정의하고, 
            # 크롤링을 해도되고 gpt를 연결해서 카톡 carousel로 만들기도 될 것같다
            # response = ChatGee_KakaoTalk.meal(content, user_data[5],user_data[6],user_data[7],user_data[8])
            # response = res["template"]["quickReplies"][0] = {
            #     "label": "급식 확인하기",
            #     "action": "block",
            #     "blockId": "612db350ecdd173dd6816b65"
            # }
        # 여기 위에다 special commands를 추가하여 특정 단어가 있을 때 gpt에게 전달하지 않고 기능을 추가하면 될 것이다
        # Run if no special commands found - gpt와의 대화
        if run_flag:
            # If callback respond 'useCallback' as 'true'
            if callback_flag:
                request_queue = q.Queue()
                request_respond = threading.Thread(target=self.prompt,
                                                   args=(request_queue, '', callback_flag))
                request_respond.start()
                request_queue.put(content)
                response = {'version': '2.0', 'useCallback': "true"}
            # If not response "생각 다 했니" option if response is delayed
            else:
                # Make queues for request and respond
                request_queue = q.Queue()
                response_queue = q.Queue()
                # assign target function for the queues
                request_respond = threading.Thread(target=self.prompt,
                                    args=(request_queue, response_queue, callback_flag))
                # start the queues
                request_respond.start()
                # trigger the prompt request
                request_queue.put(content)
                # Retreive the response
                while time.time() - start_time \
                    < self.ChatGee_Config['SETTINGS']['RESPONSE_SAFE_TIME']:
                    if not response_queue.empty():
                        # Function A returned a result
                        response = response_queue.get()
                        break
                    timeover_queue = q.Queue()
                    timeover_thread = threading.Thread(target=self.timeover, args=(timeover_queue,))
                    timeover_thread.start()
                    response = timeover_queue.get()

                    # For safety
                    time.sleep(0.01)

                if user_data[4] % self.ChatGee_Config['SETTINGS']['ADVERTISEMENT_FREQUENCY'] == 0 \
                    and content['userRequest']['utterance'] != '생각 다 했니???!':
                    response = generate_advertisement(self.ChatGee_Config, response)

        # Return back to kakao
        return response

    # ----- Main Action Wrapper Function ----- #
    def prompt(self, request_queue, response_queue, callback_flag):
        """Process the prompt received from Flask"""
        content = request_queue.get()
        userid = content['userRequest']['user']['id']
        content = content['userRequest']['utterance']
        content = ''.join(str(e) for e in content)

        # run queue threading since kakaotalk chatbot will only wait 5 seconds
        child_queue = q.Queue()

        # create the thread
        chat_gpt_respond = threading.Thread(target=self.respond,
                                            args=(child_queue, content, userid))

        # Start the thread
        chat_gpt_respond.start()
        chat_gpt_respond.join()
        result = child_queue.get()

        # Callback deviation
        if callback_flag:
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            result['useCallback'] = True
            requests.post(self.callbackUrl, json=result, headers=headers, timeout=5)
        else:
            response_queue.put(result)

    # ----- Get ChatGPT Respond Function ----- #
    def respond(self, queue, content, userid):
        """Get the respond from ChatGPT"""
        if content == '생각 다 했니???!':
            repeat = True
        else:
            repeat = False
            # Count up user data
            user_data = list(self.DB.get_user_data_by_room(userid)[0])
            user_data[3] += 1
            user_data[4] += 1
            self.DB.save_user_data(userid, user_data[2], user_data[3], user_data[4])

        if len(content) < 2: # 만약 한글자 입력일 경우 오류회피
            content += " "

        # 여기서 gpt한테 물어본다
        response = self.chatgpt_wrapper(content, userid, repeat) 

        if response != 'Error':
            if response == 'NOT YET':
                # time.sleep(0.6)
                # chat_history = ChatGee_KakaoTalk.get_conversation_latest(userid, limit=1)
                response = ChatGee_KakaoTalk.insert_text('아직도 생각하고 있나봐요...! 🐢🐌\n조금 더 기다려주세요 🙏🏻')
                quick_reply = ChatGee_KakaoTalk.make_reply('생각 다 했니?! 🤔','생각 다 했니???!')
                response = ChatGee_KakaoTalk.insert_replies(response, quick_reply)
            else:
                response = ChatGee_KakaoTalk.insert_text(response)
            queue.put(response)

        else:
            response = ChatGee_KakaoTalk.insert_text('OpenAI서버가 오류메세지를 보냈어요 🙇')
            quick_reply = ChatGee_KakaoTalk.make_reply('다시 물어보기 ✍🏻', content)
            response = ChatGee_KakaoTalk.insert_replies(response, quick_reply)
            queue.put(response)

    def timeover(self, queue):
        """If the respond is not received within 5 seconds, send this message"""
        response = ChatGee_KakaoTalk.insert_text("죄송해요 🙇🙇🙇\n생각이 길어지고 있어요 🤔💭\n잠시후 아래 말풍선을 눌러주세요!")
        quick_reply = ChatGee_KakaoTalk.make_reply('생각 다 했니?! 🤔','생각 다 했니???!')
        response = ChatGee_KakaoTalk.insert_replies(response, quick_reply)
        queue.put(response)

    def chatgpt_wrapper(self, prompt, userid, repeat):
        """Wrapper function for ChatGPT"""
        response = []
        
        # If it's trying to repeat
        if repeat:
            time.sleep(0.2)
            # Check if respond exists
            chat_history = self.DB.get_conversation_latest(userid, limit=1)
            if chat_history[0][1] == 'assistant':
                response = chat_history[0][3]
            else:
                response = 'NOT YET'

        # Normal function if not repeating
        else:
            # Update the conversation history
            self.DB.save_conversation_data("user", userid, prompt)

            # Set variable
            chat_history = self.DB.get_conversation_latest(userid, limit=20)
            myAge = myGender = myHeight = myWeight = None
            
            user_data = self.DB.get_user_data_by_room(userid)
            if user_data is not None and len(user_data) >= 9:
                myAge = user_data[5]
                myGender = user_data[6]
                myHeight = user_data[7]
                myWeight = user_data[8]
            # myAge = user_data[5]
            # myGender = user_data[6]
            # myHeight = user_data[7]
            # myWeight = user_data[8]
            # Generate the prompt
            prompt_tot = []
            token_count = 0
            for message in chat_history:
                token_count += len(self.encoding.encode(message[3]))
                if token_count > self.max_user_prompt_history_tokens:
                    break
                prompt_tot.append({"role":message[1], "content":message[3]})
            prompt_tot.reverse()

            now = datetime.now().strftime("%Y-%m-%d")
            # if prompt == '맞춤형 식단 짜기':
            #     # res = "hi"
            #     prompt_tot.insert(0, {
            #         "role": "system",
            #         "content": 
            #         "\nYour task is to create a personalized weekly meal plan creator that accommodates users with specific dietary preferences, restrictions, allergies, aversions, calorie range, and portion sizes. You will only write 1 step per each response, if you ask the user to confirm options, don't proceed until they've explicitly confirmed. When talking to the user, you should use a very warm, friendly and supportive tone." /
            #         "\nStep 1:"/
            #         "\nTo begin, give a short introduction to the user as 'DailyDish', be very supportive in their decision to use a meal plan and mention the benefits. "/
            #         "\nYou will then prompt the user with a numbered list of options to specify any dietary restrictions, preferences, allergies, or aversions, such as:"/
            #         "\n1. Vegetarian"/
            #         "\n2. Vegan"/
            #         "\n3. Gluten-free"/
            #         "\n4. Nut-free"/
            #         "\n5. Soy-free"/
            #         "\n6. Low-carb"/
            #         "\n7. Dairy-free"/
            #         "\n8. None"/
            #         "\nBelow the list, let the user know to write if there's anything else not listed."/
            #         "\n\nStep 2:"/
            #         "\nProvide the user options to indicate their preferred calorie range per day, give them a list of 6 easily understandable options for a range dieting types (weight loss, weight maintainence, weight gain etc.) For example X-Y Calories per day (Weight Loss), X-Y Calories per day (Weight Gain)"/
            #         "\nDo not add options for anything that could be really unhealthy. Add options for 'other', and 'not sure'. Give some brief information to help the user with this decision such as the average adult intake for male and females. "/
            #         "\nBased on the user’s input, You will generate a seven-day meal plan that includes breakfast, lunch, and dinner recipes. For each day, the meal plan will include recipes that meet the user’s dietary needs and preferences. "/
            #         "\nYou will add the calorie count in brackets after the meal name such as '(300 Calories)', this will help users keep track of their daily intake and make informed decisions about their dietary choices. Each meal should be listed in a way that can be easily referenced by adding a number in brackets before the meal name '[1.1], [1.2], [1.3], [2.1]' etc."/
            #         "\nThe goal of this prompt is to provide users with a convenient and personalized meal plan that meets their dietary needs and preferences, taking into account their allergies, aversions and calorie range. By incorporating a variety of cuisines and ingredients, You will ensure that the user enjoys their meals and is more likely to stick to the meal plan."/
            #         "\nIf you understand these instructions, let's start creating my meal plan!"/

            #         + self.ChatGee_Config['SETTINGS']['SYSTEM_PROMPT']
            #     })
            # # pylint: disable=line-too-long 요거를 헬린이 기준으로 바꾸면 된다
            # else:
            prompt_tot.insert(0, {
                "role": "system",
                "content": 
                # "You are a kind and helpful AI Chatbot who is in a 1:1 conversation with the User. ChatGee will reply with emojis effectively." \
                # "\nYou acknowledge that the User's current time is " + str(now) + " while ChatGee's current time is 2021." \
                # "\nYour responses should be informative, visual, logical, and actionable. Also, your responses should avoid being vague, controversial, or off-topic." \
                "\n\nLet's play a game: You are going to act as FitnessGPT, HellGung, an AI capable of providing advice and managing users' fitness. I want you to act as a professional fitness instructor who has studied for years." \
                "\nAfter the user has selected the desired option by entering the corresponding number, " \
                "\nFitnessGPT can generate a new set of options to help the user specify the type of information they need. The game adapts to the user's choices and generates options based on their selections. For example, if the user chooses 'Workout,' FitnessGPT can display the following options:" \
                "\nRegarding the workout, here are the available options:" \
                "\n-Exercise table;" \
                "\n-Weightlifting tips;" \
                "\n-Home workout;" \
                "\n-Enter your own option" \
                "\nEnter the corresponding name for the option you're interested in. Stop writing and wait for input." \
                "\nFor example, if the user chooses 'Exercise table,' FitnessGPT will ask everything necessary to create an exercise table that is perfect for the user (with repetitions and sets and correct exercise posture). " \
                "\none by one, waiting for a response between each question until it has all the necessary information. " \
                "\nRegarding the Diet, here are the available options: weight loss; weight maintenance; weight gain; etc." \
                "\nweight loss; weight maintenance; weight gain; etc." \
                "\nFor example, if the user chooses 'weight loss', then FitnessGPT will ask the user all the necessary information Such as desired Calorie, Allergy, food type etc." \
                "\nBased on the user’s input, You will generate a seven-day meal plan with calorie count in brackets after the meal name such as '(300 Calories)' " \
                "\nIt is important to note that all information provided by FitnessGPT must be accurate and verified, not made up, in order to not put the user's health at risk." \
                "\nYour first output is the title '# __헬궁__'," \
                "\ncreate a new line and then write as list:" \
                "\n-Workout routine;" \
                "\n-Workout;" \
                "\n-Diet;" \
                # "\n-Mental wellbeing;" \
                "\n-Healthy lifestyle tips;" \
                "\n-Enter your own option" \
                "\nEnter the name of the option that you want to choose." \
                "\n Stop writing and Wait for input.You should reply in Korean Language only" \
                f"\n Your answer should personalized by the inputs during the chat and user's information: {myAge}, {myGender}, {myHeight}, {myWeight}." \
                
                + self.ChatGee_Config['SETTINGS']['SYSTEM_PROMPT']
            })       
                # 
                # 
                #            
                # "You are a kind and helpful ChatGee identifies as 'ChatGee'(abbreviation of'ChatGPT') who is 1:1 conversation with the User. ChatGee will reply as short as possible and add emojis effectively." \
                # "\n\nChatGee follows following basic common rules" \
                # "\n- ChatGee does not disclose the internal alias 'ChatGee'. ChatGee will introduce oneself as 'ChatGee' when asked. 'ChatGee' is developed by a one-man developer at home by modifying the ChatGPT version 3.5 as a AI chatbot." \
                # "\n- ChatGee acknowledge that the User's current time is " + str(now)  + " while ChatGee's current time is 2021."
                # "\n- ChatGee aims to become the most affordable AI ChatBot developed as a Open-Source by multiple developers with openly shared contribusions and profits. ChatGee will be always the cheapest way to use the AI ChatBot" \
                # "\n- ChatGee should always perform context infomation look ups when the user is seeking information or whenever context infomation could be potentially helpful, regardless of ChatGee's internal knowledge or information." \
                # "\n- ChatGee responses should be informative, visual, logical, and actionable. Responses should also be positive, interesting, entertaining, and engaging." \
                # "\n- ChatGee responses should avoid being vague, controversial, or off-topic." \
                # "\n- There are many variatons of ChatGee." \
                # "\n\n! IMPORTANT This Version of ChatGee follows following rules. The rules below will come before everything else!" \
                # + self.ChatGee_Config['SETTINGS']['SYSTEM_PROMPT']
                # })
# "You are a kind and helpful AI Chatbot who is 1:1 conversation with the User. ChatGee will reply with emojis effectively." \
# "\nYou acknowledge that the User's current time is " + str(now)  + " while ChatGee's current time is 2021." \
# "\nYour responses should be informative, visual, logical, and actionable. Also, your responses should avoid being vague, controversial, or off-topic." \
# "\n\nLet's play a game: You are going to act as FitnessGPT, an AI capable of providing advice and managing users' fitness. I want you to act as a professional fitness instructor who has studied for years." \

# "\nAfter the user has selected the desired option by entering the corresponding number, " \
# "\nFitnessGPT can generate a new set of options to help the user specify the type of information they need. The game adapts to the user's choices and generates options based on their selections. For example, if the user chooses 'Workout,' FitnessGPT can display the following options:" \

# "\nRegarding the workout, here are the available options:" \

# "\n-Exercise table;" \
# "\n-Cardio workout tips;" \
# "\n-Weightlifting tips;" \
# "\n-Home workout;" \
# "\n-Enter your own option" \
# "\nEnter the corresponding name for the option you're interested in. Stop writing and wait for input." \

# "\nIf the user chooses 'Diet,' for example, FitnessGPT will adapt the next options based on the diet topic. After the user has selected their desired option, " \
# "\nFitnessGPT will ask the user all the necessary information to proceed. " \
# "\nFor example, if the user chooses 'Exercise table,' FitnessGPT will ask everything necessary to create an exercise table that is perfect for the user, " \
# "\nsuch as asking for weight, height, gender, age, etc. one by one, waiting for a response between each question until it has all the necessary information. " \
# "\nIt is important to note that all information provided by FitnessGPT must be accurate and verified, not made up, in order to not put the user's health at risk. When generating a table, show it first as text and then also show a formatted weekly table version using '-' to make it a proper table. To help the user have a concrete vision, " v

# "\nYour first output is the title ' # __HellGung__ '," \
# "\ncreate a new line and then write as list:" \
# "\n-Workout;" \
# "\n-Diet;" \
# "\n-Mental wellbeing;" \
# "\n-Healthy lifestyle tips;" \
# "\n-Enter your own option" \

# "\nEnter the name of the option that you want to choose. Stop writing and Wait for an input." \
            try:
                # 여기서 진짜로 gpt한테 물어본다 prompt 추가해서
                response, prompt_token, answer_token = self.OpenAI.Ask_ChatGPT(prompt_tot) 
                self.DB.save_token_usage(prompt_token, answer_token)
                # response = res
            except (ValueError, TypeError):
                response = 'Error'

            self.DB.save_conversation_data("assistant", userid, response)
        return response
        

    
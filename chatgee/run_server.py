# -*- coding: utf-8 -*-
"""ChatGee API Server"""

import time

from flask import Flask, request, jsonify, render_template

from base.chatgee import ChatGeeOBJ
from base.utility import read_yaml, send_query_local
from base.module_database import ChatGee_DB
from base.module_kakaotalk import ChatGee_KakaoTalk


# ############################################### #
CONFIG_FILE_PATH = "settings.yaml"
# ############################################### #

# ---------------     Flask     ----------------- #
app = Flask(__name__, static_url_path='/static')

# -------------- Initiate Modules,--------------- #
# Read Config File
ChatGee_Config = read_yaml(CONFIG_FILE_PATH)
# Initiate ChatGee Library
ChatGee = ChatGeeOBJ(ChatGee_Config)

# -----------------  Flask Routes  --------------- #
# Base Route
@app.route("/")
def index():
    """Base Route"""
    return {'message': 'Welcome to the Kakatotalk ChatGPT AI Chatbot API' \
            + '\n챗지 챗봇 API에 오신 것을 환영합니다. 서버가 잘 작동중입니다!' \
            + '\n https://github.com/woensug-choi/ChatGee'}

# Chat Route
@app.route("/prompt", methods=['POST'])
def prompt():
    """ChatGee Prompt Route"""
    return jsonify(ChatGee.prompt_received(request.get_json()))

@app.route('/myData', methods=['POST'])
def myData():
    return jsonify(ChatGee.myData_received(request.get_json()))

@app.route('/myAge', methods=['POST'])
def myAge():
    return jsonify(ChatGee.myAge_received(request.get_json()))

@app.route('/myGender', methods=['POST'])
def myGender():
    return jsonify(ChatGee.myGender_received(request.get_json()))

@app.route('/myHeight', methods=['POST'])
def myHeight():
    return jsonify(ChatGee.myHeight_received(request.get_json()))

@app.route('/myWeight', methods=['POST'])
def myWeight():
    return jsonify(ChatGee.myWeight_received(request.get_json()))

# @app.route('/createImage', methods=['POST'])
# def myImage():
#     return jsonify(ChatGee.createImage(request.get_json()))

# @app.route("/mydata", methods=['POST'])
# def mydata():
#     DB = ChatGee_DB()
#     req = request.get_json()
#     # 이부분에서 나이 성별 키 몸무게 등을 받아오고 db에 저장하는 함수 실행 하면 될듯
#     if req["action"]["detailParams"]["ask_age"]["value"]:
#         params_ask_age = req["action"]["detailParams"]["ask_age"]["value"]
#         response = ChatGee_KakaoTalk.insert_text('성별을 입력해주세요')
#     elif req["action"]["detailParams"]["ask_gender"]["value"]:
#         params_ask_gender = req["action"]["detailParams"]["ask_gender"]["value"]
#         response = ChatGee_KakaoTalk.insert_text('키를 입력해주세요')
#     elif req["action"]["detailParams"]["ask_height"]["value"]:
#         params_ask_height = req["action"]["detailParams"]["ask_height"]["value"]
#         response = ChatGee_KakaoTalk.insert_text('몸무게를 입력해주세요')
#     elif req["action"]["detailParams"]["ask_weight"]["value"]:
#         params_ask_weight = req["action"]["detailParams"]["ask_weight"]["value"]
#         response = ChatGee_KakaoTalk.insert_text('등록 완료!!')
#         # response = ChatGee_KakaoTalk.insert_card('등록이 완료되었습니다', '안녕하세요! \n{params_ask_age}살, {params_ask_gender}, {params_ask_height}cm, {params_ask_weight}kg으로 설정이 완료되었습니다')




#     # params_ask_height = req["action"]["detailParams"]["ask_height"]["value"]
#     # params_ask_weight = req["action"]["detailParams"]["ask_weight"]["value"]
#     # res_ask_age = re.sub(r"[^0-9]", "", params_ask_age)
#     # res_ask_gender = re.sub(r"[^0-9]", "", params_ask_gender)
#     # DB.save_user_data(userid, isFriend, 1, 0, params_ask_age, params_ask_gender, params_ask_height, params_ask_weight)
#     # res = {
#     #         "version": "2.0",
#     #         "template": {
#     #             "outputs": [
#     #                 {
#     #                     "basicCard": {
#     #                         "title": "설정이 완료 되었습니다.",
#     #                         "description": f"안녕하세요! \n{params_ask_age}살, {params_ask_gender}, {params_ask_height}cm, {params_ask_weight}kg으로 설정이 완료되었습니다.",
#     #                         "thumbnails": {
#     #                             "imageUrl": ""
#     #                         }
#     #                     }
#     #                 }
#     #             ],
#     #         }
#     #     }
#     return jsonify(response)

# @app.route('/myAge', methods=['POST'])
# def myAge():
#     req = request.get_json()
#     DB = ChatGee_DB()
#     # Check user
#     # new_user_flag = False
#     userid = req['userRequest']['user']['id'] # userid is saved as 'room' in user_data.db
#     isFriend = req['userRequest']['user']['properties'].get('isFriend', False)
#     # Read user data (room, member, count, total_count)
#     # user_data = DB.get_user_data_by_room(userid)
#     # If new user, save guest template
#     # if len(user_data) == 0:
#     #     # # 이부분에서 나이 성별 키 몸무게 등을 받아오고 db에 저장하는 함수 실행 하면 될듯
#     #     # params_ask_age = req["action"]["detailParams"]["ask_age"]["value"]
#     #     # params_ask_gender = req["action"]["detailParams"]["ask_gender"]["value"]
#     #     # params_ask_height = req["action"]["detailParams"]["ask_height"]["value"]
#     #     # params_ask_weight = req["action"]["detailParams"]["ask_weight"]["value"]
#     #     # # res_ask_age = re.sub(r"[^0-9]", "", params_ask_age)
#     #     # # res_ask_gender = re.sub(r"[^0-9]", "", params_ask_gender)
#     #     # DB.save_user_data(userid, isFriend, 1, 0, params_ask_age, params_ask_gender, params_ask_height, params_ask_weight)

#     #     DB.save_user_data(userid, isFriend, 1, 0)
#     # user_data = list(DB.get_user_data_by_room(userid)[0])
#     # # previous_friendship = user_data[2]
#     # DB.save_user_data(userid, isFriend, user_data[3], user_data[4])
#     # user_data = list(DB.get_user_data_by_room(userid)[0])


#     myAge = req["action"]["detailParams"]["myAge"]["value"]
#     response = ChatGee_KakaoTalk.insert_card('등록이 완료되었습니다', f'안녕하세요! {userid}살, 으로 설정이 완료되었습니다')

#     # DB.save_user_data(userid, isFriend, 1, 0, params_ask_age, params_ask_gender, params_ask_height, params_ask_weight)

#     # response = ChatGee_KakaoTalk.insert_text('아직도 생각하고 있나봐요...! 🐢🐌\n조금 더 기다려주세요 🙏🏻')

#     return jsonify(response)

# @app.route('/myGender', methods=['POST'])
# def myGender():
#     req = request.get_json()

#     myGender = req["action"]["detailParams"]["myGender"]["value"]

#     response = ChatGee_KakaoTalk.insert_text('아직도 생각하고 있나봐요...! 🐢🐌\n조금 더 기다려주세요 🙏🏻')

#     return jsonify(response)

# @app.route('/myHeight', methods=['POST'])
# def myHeight():
#     req = request.get_json()

#     myHeight = req["action"]["detailParams"]["myHeight"]["value"]

#     response = ChatGee_KakaoTalk.insert_text('아직도 생각하고 있나봐요...! 🐢🐌\n조금 더 기다려주세요 🙏🏻')

#     return jsonify(response)

# @app.route('/myWeight', methods=['POST'])
# def myWeight():
#     req = request.get_json()

#     myWeight = req["action"]["detailParams"]["myWeight"]["value"]

#     response = ChatGee_KakaoTalk.insert_text('아직도 생각하고 있나봐요...! 🐢🐌\n조금 더 기다려주세요 🙏🏻')

#     return jsonify(response)


# Chat Route
@app.route("/check", methods=['POST'])
def check():
    """ChatGee Prompt Route"""
    return jsonify({
        "status": "SUCCESS"        
    })

# Usage Route
@app.route('/usage/<userid>')
def usage_count(userid):
    """Usage Count Route"""
    usage_count_no = ChatGee.get_usage_count(userid)
    chart_data = {
        'labels': ['Usage Count'],
        'datasets': [{
            'label': 'Usage Count',
            'backgroundColor': 'rgba(255, 20, 147, 0.2)',
            'borderColor': 'rgba(255, 99, 132, 1)',
            'borderWidth': 1,
            'data': [usage_count_no],
        }]
    }
    return render_template('usage.html',
                           userid=userid,
                           usage_count=usage_count_no,
                           chart_data=chart_data)

# Send Dummy Route
# pylint: disable=R1710
@app.route("/local_test", methods=["GET", "POST"])
def local_query():
    """Send Query to Local Server"""
    system_prompt = ChatGee_Config['SETTINGS']['SYSTEM_PROMPT']

    # If the form has been submitted
    if request.method == "POST":
        query = request.form["question"]
        if query:
            start_time = time.time()
            response = send_query_local(query, ChatGee_Config)
            answer = ""
            if response is not None:
                answer = response.replace('\n', '<br>')
            return render_template("local_test.html",
                    question=query, answer=answer,
                    time_elapsed=round((time.time() - start_time), 2),
                    system_prompt=system_prompt)
    else:
        # Render the local_test HTML template without any question or answer
        return render_template("local_test.html")

if __name__ == "__main__":
    app.run(host=ChatGee_Config['SERVER']['HOST_NAME'],
            port=ChatGee_Config['SERVER']['PORT_NUMBER'],
            debug=ChatGee_Config['SERVER']['DEBUG_FLASK'],
            extra_files=[CONFIG_FILE_PATH])

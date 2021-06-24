from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from .models import User, DataEntry
from django.core.exceptions import ValidationError
import logging
import random
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logging.debug('debug msg')
logging.info('info msg')


# Create your views here.
def message(request):
    def gen_response(code: int, data: str):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    # GET的完整实现已经给出，同学们无需修改
    if request.method == 'GET':
        '''limit = request.GET.get('limit', default='100')
        offset = request.GET.get('offset', default='0')
        if not limit.isdigit():
            return gen_response(400, '{} is not a number'.format(limit))
        if not offset.isdigit():
            return gen_response(400, '{} is not a number'.format(offset))'''
        order_number = DataEntry.objects.all().count() + 1
        return gen_response(200, [
                {
                    'number': order_number,
                    'age': "100",
                    'sex': "child",
                    'handiness': "right"
                }
                # for trial in DataEntry.objects.all().order_by('-pk')[int(offset) : int(offset) + int(limit)]
            ])

    elif request.method == 'POST':
        # 从cookie中获得user的名字，如果user不存在则新建一个
        # 如果cookie中没有user则使用"Unknown"作为默认用户名
        '''name = request.COOKIES['user'] if 'user' in request.COOKIES else 'Unknown'
        user = User.objects.filter(name=name).first()
        if not user:
            user = User(name = name)
            try:
                # 注意在调用full_clean()时Django会自动检测字段的有效性，这个有效性检测包括检测CharField是否满足最大长度限制
                user.full_clean()
                # 存入数据库
                user.save()
            except ValidationError as e:
                return gen_response(400, "Validation Error of user: {}".format(e))'''
        # logging.debug(str(request.body))
        # 验证请求的数据格式是否符合JSON规范(请求体可通过json.loads()即可），如果不符合则返回code 400，data字段内容自定义即可
		# --------------------------------------------------------------------------------------------
        try:
           Data = json.loads(request.body)
           logging.debug("-------------------------------loading ok")
        except ValueError as e:
            logging.debug("==============================loading fail")
            return gen_response(400, "Validation Error of Request Body:{}".format(e))

        # 验证请求数据是否满足接口要求，若通过所有的验证，则将新的消息添加到数据库中。如果不符合要求则返回code 400，data字段内容自定义即可
        # PS: 请求数据体应该为{"title": "something", "content": "someting"} ，请确保title和content字段存在，并且title和content均有最大长度限制
		# PS: 检测方式可以参考user，使用Django提供的full_clean()方法进行检测
        # --------------------------------------------------------------------------------------------

        logging.debug(str(Data))
        sex = ""
        data = []
        handiness = ""
        try:
            name = Data['name']
            age = Data['age']
            sex = Data['gender']
            data = Data['data']
            handiness = Data['handiness']
            logging.debug("----------------------------------name age sex data ok")
        except KeyError as e:
            logging.debug("----------------------------------name age sex data fail")
            '''if data is None:
                return gen_response(400, "DATA is null")
            if name is None or name == "":
                return gen_response(400, "Name is null")
            if handiness is None or handiness == "":
                return gen_response(400, "Handiness is null")'''
            if sex is None or sex == "":
                logging.debug("---------------------------------- sex is none")
                name = Data['name']
                age = Data['age']
                data = Data['data']
                handiness = Data['handiness']
                if random.random() < 0.5:
                    sex = "female"
                else:
                    sex = "male"


        logging.debug(str(Data))
        logging.debug(data)
        newUser = User(name=name, sex=sex, age=age, handiness=handiness)
        newUser.save()
        trial = DataEntry(user=newUser, data=str(data))
        logging.debug("----------------------------------trial established")
        fileID = DataEntry.objects.all().count() + 1
        logging.debug("----------------------------------ID:" + str(fileID))
        try:
            # trial.full_clean()
            logging.debug("----------------------------------trial ok")
            file = open("Statistics/ID_" + str(fileID) + '.txt', 'w')
            file.write('ID Date gender age handiness kind user truth accurate\n')
            # logging.debug(data)
            for item in data:
                file.write(name+" " + str(newUser.register_date) + " " + sex + " " + str(age) + " " + handiness + " " + item['kind'] + " " + item['user'] + " " + item['truth'] + " " + str(item['accurate'])+"\n")
            trial.save()
        except ValidationError as e:
            logging.debug("----------------------------------trial fail")
            return gen_response(400, "Validation Error of user: {}".format(e))

        # 添加成功返回code 201
        return gen_response(201, "message was sent successfully")

    else:
        return gen_response(405, 'method {} not allowd'.format(request.method))

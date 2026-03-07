import json
import hashlib
class Controller:
    def execute(self, param):
        data = param
        try:
            if "data" in data and data["data"] is not None:
                content_array = data.get("data")
                company_name = data.get("company")
                if content_array is not None and len(content_array) > 0:
                    data_list = []
                    for i in range(1, len(content_array)):
                        map_data = {}
                        data_array = content_array[i]
                        vid = hashlib.md5(f"{data_array[0]}-{data_array[1]}:00-{data_array[3]}-{data_array[2]}".encode('utf-8')).hexdigest()
                        map_data["vid"] = vid
                        map_data["car_no"] = data_array[0]
                        map_data["proccess_time"] = data_array[5]
                        map_data["violation_time"] = data_array[1]
                        map_data["violation_address"] = data_array[2]
                        map_data["violation_content"] = data_array[3]
                        map_data["proccess_status"] = data_array[4]
                        map_data["pay_status"] = data_array[6]
                        if data_array[5] != "":
                            map_data["proccess_time"] = data_array[5]
                        else:
                            map_data["proccess_time"] = None
                        # 处理不同的交通违规情况
                        if data_array[3] in ["驾驶机动车在限速60公里/小时以下的公路上行驶超过规定车速未达到50%的",
                                                "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车行驶超过规定时速未达到10%的",
                                                "驾驶中型以上载货汽车在高速公路、城市快速路以外的道路上行驶超过规定时速未达到10%的",
                                                "非紧急情况时在高速公路应急车道上行驶的",
                                                "驾驶中型以上载客载货汽车、校车、危险物品运输车辆以外的机动车超过规定时速未达10%的",
                                                "机动车在设置“严管路段”、“消防车通道”以及应急、救援、抢险、救护等生命通道标识化区域和路段违反停放、临时停车规定的",
                                                "驾驶中型以上载客载货汽车、校车、危险物品运输车辆以外的其他机动车在道路限速值低于60公里/小时的道路上超过规定车速50%以下的"]:
                            map_data["violation_points"] = "0"
                            map_data["violation_fines"] = "0"
                        elif data_array[3] in [
                            "机动车违反规定临时停车，驾驶人在现场拒绝立即驶离，妨碍其它车辆、行人通行的",
                            "禁鸣区鸣喇叭",
                            "机动车乘坐人未使用安全带"]:
                            map_data["violation_points"] = "0"
                            map_data["violation_fines"] = "50"
                        elif data_array[3] in [
                            "机动车不走机动车道",
                            "不按导向车道行驶",
                            "机动车违规使用专用车道",
                            "信号灯路口越停车线停车",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在限速60公里/小时以下的道路上行驶超过规定时速10%以上（含）未达到20%的",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路上行驶超过规定时速百分之十以上未达到百分之二十的",
                            "驾驶中型以上载客载货汽车、校车、危险物品运输车辆以外的机动车在道路限速值在60公里/小时以上80公里/小时以下的道路上行驶超过规定时速10%以上未达20%的",
                            "驾驶中型以上载客载货汽车、校车、危险物品运输车辆以外的其他机动车在道路限速值在60公里/小时以上80公里/小时以下的道路上行驶超过规定时速10%以上未达20%的",
                            "违反规定停放、临时停车且驾驶人不在现场或驾驶人虽在现场拒绝立即驶离，妨碍其他车辆、行人通行的",
                            "驾驶机动车在高速公路、城市快速路以外的道路上不按规定车道行驶的",
                            "机动车从匝道进入高速公路时不按规定使用灯光的"]:
                            map_data["violation_points"] = "0"
                            map_data["violation_fines"] = "100"
                        elif data_array[3] in [
                            "机动车违反规定停放，驾驶人不在现场，妨碍其它车辆、行人通行的",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在限速60公里/小时以上80公里/小时以下的道路上行驶超过规定时速10%以上（含）未达到20%的"]:
                            map_data["violation_points"] = "0"
                            map_data["violation_fines"] = "150"
                        elif data_array[3] in [
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在限速80公里/小时以上100公里/小时以下的道路上行驶超过规定时速10%以上（含）未达到20%的",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在限速100公里/小时以上的道路上行驶超过规定时速10%以上（含）未达到20%的",
                            "驾驶中型以上载客载货汽车、校车、危险物品运输车辆以外的机动车在道路限速值为80公里/小时以上（不含80公里/小时）的道路上行驶超过规定时速10%以上未达20%的",
                            "铁路路口不按规定行驶",
                            "机动车从匝道驶离高速公路时不按规定使用灯光的",
                            "在高速公路上骑、轧车行道分界线的"]:
                            map_data["violation_points"] = "0"
                            map_data["violation_fines"] = "200"
                        elif data_array[3] in ["驾驶人未按规定使用安全带的",
                                               "违反规定掉头"
                                                  ]:
                            map_data["violation_points"] = "1"
                            map_data["violation_fines"] = "150"
                        elif data_array[3] in [
                            "不按规定使用灯光",
                            "违反禁止标线指示",
                            "违反禁令标志指示"
                            ]:
                            map_data["violation_points"] = "1"
                            map_data["violation_fines"] = "100"
                        elif data_array[3] == "危险路段掉头":
                            map_data["violation_points"] = "1"
                            map_data["violation_fines"] = "150"
                        elif data_array[3] in ["人行道不停车让行的",
                                                "驾车时有其他妨碍安全驾驶的行为的",
                                                "驾车有接拨手持电话等妨碍安全驾驶行为",
                                                "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路、城市快速路以外的道路上行驶超过规定时速20%以上未达到50%的"]:      
                            map_data["violation_points"] = "3"
                            map_data["violation_fines"] = "50"
                        elif data_array[3] in [
                            "驾车接拨手持电话",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路、城市快速路以外的道路(限速60公里/小时以下的)上行驶超过规定时速20%以上（含）未达到50%的",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路、城市快速路以外的道路上行驶超过规定时速百分之二十以上未达到百分之五十的",
                            "驾驶机动车时利用手持电话上网、查看与发送短信或者观看电视"]:
                            map_data["violation_points"] = "3"
                            map_data["violation_fines"] = "100"
                        elif data_array[3] == "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路、城市快速路以外的道路（限速60公里/小时以上80公里/小时以下）行驶超速20%以上（含）未达50%的":
                            map_data["violation_points"] = "3"
                            map_data["violation_fines"] = "150"
                        elif data_array[3] in [
                            "逆向行驶",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路、城市快速路以外的道路（限速80公里/小时以上100公里/小时以下）行驶超速20%以上（含）未达50%"]:
                            map_data["violation_points"] = "3"
                            map_data["violation_fines"] = "200"
                        elif data_array[3] in ["驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路、城市快速路以外的道路(限速60公里/小时以下的)上行驶超过规定时速20%以上",
                                                "遇行人正在通过人行横道时未停车让行的"]:

                            map_data["violation_points"] = "3"
                            map_data["violation_fines"] = "200"
                        elif data_array[3] in [
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在城市快速路（限速60公里/小时以上80公里/小时以下的）上行驶超过规定时速20%以上（含）未达到50%的",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路(限速60公里/小时以上80公里/小时以下的)上行驶超过规定时速20%以上（含）未达到50%的",
                            "驾驶机动车违反道路交通信号灯通行的"]:
                            map_data["violation_points"] = "6"
                            map_data["violation_fines"] = "150"
                        elif data_array[3] in [
                            "驾驶机动车不按交通信号灯指示通行的",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路(限速80公里/小时以上100公里/小时以下的)上行驶超过规定时速20%以上（含）未达到50%的",
                            "占用应急车道行驶的",
                            "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路(限速100公里/小时以上的)上行驶超过规定时速20%以上（含）未达到50%的"]:
                            map_data["violation_points"] = "6"
                            map_data["violation_fines"] = "200"
                        elif data_array[3] == "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路、城市快速路以外的道路(限速60公里/小时以下的)上行驶超过规定时速50%以上（含）100%以下的":
                            map_data["violation_points"] = "6"
                            map_data["violation_fines"] = "400"
                        elif data_array[3] == "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在高速公路、城市快速路以外的道路(限速60公里/小时以上80公里/小时以下)上行驶超速50%以上（含）100%以下":
                            map_data["violation_points"] = "6"
                            map_data["violation_fines"] = "600"
                        elif data_array[3]in ["驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车在城市快速路上行驶超过规定时速20%以上未达到50%的"]:
                            map_data["violation_points"] = "6"
                            map_data["violation_fines"] = "50"
                        elif data_array[3] == "驾驶校车、中型以上载客载货汽车、危险物品运输车辆以外的机动车行驶超过规定时速百分之十以上未达到百分之二十的":
                            if company_name == "四川恒创富远汽车销售有限公司自贡分公司":
                                map_data["violation_points"] = "0"
                                map_data["violation_fines"] = "200"
                            elif company_name in ["江苏优福信汽车科技有限公司","南京弘扬希望科技有限公司"]:
                                map_data["violation_points"] = "0"
                                map_data["violation_fines"] = "50"
                        elif data_array[3] == "不按规定停车":
                            if company_name in ["江苏优福信汽车科技有限公司","南京弘扬希望科技有限公司"]:
                                map_data["violation_points"] = "0"
                                map_data["violation_fines"] = "100"
                            else:
                                map_data["violation_points"] = "0"
                                map_data["violation_fines"] = "50"
                        if data_array[3] == "无需交款":
                            map_data["violation_points"] = "0"
                            map_data["violation_fines"] = "0"

                        map_data["company"] = company_name
                        map_data["resource"] = "交管"
                        data_list.append(map_data)

                    #if data_list:
                    #    # 模拟 Monitor.rpaData 的功能
                    #    print("Sending data:", json.dumps(data_list))

            result = data_list
            return result
        except Exception as e:
            print("Error:", e)
            return []
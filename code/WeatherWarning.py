import requests
import json

import pathlib
import os

# 気象庁 API取得
urlWarning = "https://www.jma.go.jp/bosai/warning/data/warning/250000.json"

# requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
responseWarning = requests.get(urlWarning)

# response.json()でJSONデータに変換して変数へ保存
jsonDataWarning = responseWarning.json()


cityNumtoENname = {
    "2542500" : "aisho",
    "2520400" : "omihachiman",
    "2520101" : "otsuS",
    "2520102" : "otsuN",
    "2520600" : "kusatsu",
    "2520900" : "koka",
    "2544200" : "koura",
    "2521100" : "konan",
    "2521200" : "takashima",
    "2544300" : "taga",
    "2544100" : "toyosato",
    "2520300" : "nagahama",
    "2521300" : "higashiomi",
    "2520200" : "hikone",
    "2538300" : "hino",
    "2521400" : "maibara",
    "2520700" : "moriyama",
    "2521000" : "yasu",
    "2520800" : "ritto",
    "2538400" : "ryuoh"
}
cityENnametoJPname = {
        "愛荘町":"aisho",
        "近江八幡市":"omihachiman",
        "大津市":"otsu",
        "草津市":"kusatsu",
        "甲賀市":"koka",
        "甲良町":"koura",
        "湖南市":"konan",
        "高島市":"takashima",
        "多賀町":"taga",
        "豊郷町":"toyosato",
        "長浜市":"nagahama",
        "東近江市":"higashiomi",
        "彦根市":"hikone",
        "日野町":"hino",
        "米原市":"maibara",
        "守山市":"moriyama",
        "野洲市":"yasu",
        "栗東市":"ritto",
        "竜王町":"ryuoh",
}

# レスポンス用JSONデータ
WeatherWarningDataJson = {
    "updateTime":jsonDataWarning["reportDatetime"],
    "comment":jsonDataWarning["headlineText"],
    "wather" : {},
    "cityWarning": {}
}

for data in jsonDataWarning["areaTypes"][1]["areas"]:
    cityENname = cityNumtoENname[data["code"]]
    WeatherWarningDataJson["cityWarning"][cityENname] = {"caution" : [],"warning" : [],"emergency" : []}
    
    # 天気IDの辞書
    warningsCode = {
        "00" : "未登録のデータ",
        "01" : "未登録のデータ",
        "02" : "未登録のデータ",
        "03" : "大雨警報",
        "04" : "洪水警報",
        "05" : "未登録のデータ",
        "06" : "未登録のデータ",
        "07" : "未登録のデータ",
        "08" : "未登録のデータ",
        "09" : "未登録のデータ",
        "10" : "大雨注意報",
        "11" : "未登録のデータ",
        "12" : "未登録のデータ",
        "13" : "未登録のデータ",
        "14" : "雷注意報",
        "15" : "強風注意報",
        "16" : "波浪注意報",
        "18" : "洪水注意報",
        "19" : "高潮注意報",
        "20" : "濃霧注意報",
    }

    for wData in data["warnings"]:
        # 解除 発表
        if not wData["status"] == "解除":
            if wData["code"] in ["03","04"]:
                WeatherWarningDataJson["cityWarning"][cityENname]["warning"].append(warningsCode[wData["code"]])
            elif wData["code"] in ["10","11","12","13","14","15","16","17","18","19","20"]:
                WeatherWarningDataJson["cityWarning"][cityENname]["caution"].append(warningsCode[wData["code"]])
        
    #caution 注意報
    #warning 警報
    #emergency 特別警報


# 天気予報取得
urlWeather = "https://www.jma.go.jp/bosai/forecast/data/forecast/250000.json"
# requests.getを使うと、レスポンス内容を取得できるのでとりあえず変数へ保存
responseWeather = requests.get(urlWeather)

# responseWeather.json()でJSONデータに変換して変数へ保存
jsonDataWeather = responseWeather.json()
print("-------------")
print(jsonDataWeather[0])

for areaWeather in jsonDataWeather[0]["timeSeries"][0]["areas"]:
    weatherIDList = {
        "100" : "晴れ",
        "101" : "晴れ 時々 曇り",
        "102" : "晴れ 時々 雨",
        "104" : "晴れ 時々 雪",
        "110" : "晴れ のち 曇り",
        "112" : "晴れ のち 雨",
        "115" : "晴れ のち 雪",
        "200" : "曇り",
        "201" : "曇り 時々 晴れ",
        "202" : "曇り 時々 雨",
        "204" : "曇り 時々 雪",
        "210" : "曇り のち 一時晴れ",
        "212" : "曇り のち 一時雨",
        "215" : "曇り のち 一時雪",
        "300" : "雨",
        "301" : "雨 時々 晴れ",
        "302" : "雨 時々 曇り",
        "303" : "雨 時々 雪",
        "308" : "豪雨(?)",
        "311" : "雨 のち 一時晴れ",
        "313" : "雨 のち 一時曇り",
        "314" : "雨 のち 一時雪",
        "400" : "雪",
        "401" : "雪 時々 晴れ",
        "402" : "雪 時々 曇り",
        "403" : "雪 時々 雨",
        "406" : "豪雪(?)",
        "411" : "雪 のち 一時晴れ",
        "413" : "雪 のち 一時曇り",
        "414" : "雪 のち 一時雪",
        "500" : "晴れ",
        "501" : "晴れ 時々 曇り",
        "502" : "晴れ 時々 雨",
        "504" : "晴れ 時々 雪",
        "510" : "晴れ のち 曇り",
        "512" : "晴れ のち 雨",
        "515" : "晴れ のち 雪"
    }
    WeatherWarningDataJson["wather"][areaWeather["area"]["name"]] = {
        "weatherDataCode" : [
            [
                areaWeather["weatherCodes"][0],
                areaWeather["weatherCodes"][1],
                areaWeather["weatherCodes"][2]
            ],
            [
                weatherIDList[areaWeather["weatherCodes"][0]],
                weatherIDList[areaWeather["weatherCodes"][1]],
                weatherIDList[areaWeather["weatherCodes"][2]]
            ]
        ],
        "weatherDataText" : [
            areaWeather["weathers"][0].replace("　", " "),
            areaWeather["weathers"][1].replace("　", " "),
            areaWeather["weathers"][2].replace("　", " ")
        ],
        "weatherDataWind" : [
            areaWeather["winds"][0],
            areaWeather["winds"][1],
            areaWeather["winds"][2]
        ]
    }


print(WeatherWarningDataJson)

# 相対パスで指定した後、絶対パスに変換
jsonPath = pathlib.Path('../data/WeatherWarning.json')
jsonPath = jsonPath.resolve()

print(jsonPath)

with open(jsonPath, 'w') as f:
    json.dump(WeatherWarningDataJson, f, indent=4, ensure_ascii=False)
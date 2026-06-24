import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime , timedelta , date
import os 
import math
from pathlib import Path
import tkinter as tk

def file_read():
    global date_list,weather_list
    research()
    try:
        df = pd.read_csv(path)
        df = df.sort_values('Date',ignore_index=True,ascending=True)
    except FileNotFoundError:
        print('CSVファイルを新規作成します。')
        date_list = []
        weather_list = []
        data = {'Date':date_list,'Weather':weather_list}        
        df = pd.DataFrame(data)
        file_write(data)
    except:
        print('想定外のエラー')
    finally:
        return df   
  
def file_write(data):
    try:
        df = pd.DataFrame(data)
        df = pd.concat([df],ignore_index=True)
        df['Date'] = pd.to_datetime(df['Date'])
        sortData = df.sort_values('Date',ignore_index=True,ascending=True)
        sortData.to_csv(path,index = True)
    except:
        print('書き込みに失敗しました。\n想定外のエラーです。')
        sortData = 'None'
    finally:
        return sortData
    
def research():
    global path,found_path_weathernews,found_path_data_save
    filename_to_find_weathernews = "weathernews_CUI.py"
    filename_to_find_data_save = 'weather_data_save.csv'
    search_start_dir = Path.home()#検索を開始するディレクトリを指定

    found_path_weathernews = None
    for path_weathernews in search_start_dir.rglob(filename_to_find_weathernews):# rglobはジェネレータを返すため、forループで順に試す
        found_path_weathernews = path_weathernews.resolve()
        print(f'ディレクトリ：{search_start_dir}から検索中（1/2）…')
    found_path_data_save = None
    for path_data_save in search_start_dir.rglob(filename_to_find_data_save):# rglobはジェネレータを返すため、forループで順に試す
        found_path_data_save = path_data_save.resolve()
        print(f'ディレクトリ：{search_start_dir}から検索中（2/2）…')

    if not found_path_weathernews:
        found_path_weathernews = '存在しません。'
        path_bool = False
    elif not found_path_data_save:
        found_path_data_save = '存在しません。'
        path_bool = False
    else:
        path_bool = True
    
    parent_dir = found_path_weathernews.parent #親ディレクトリを取得
    new_floud_path_weathernews = parent_dir / filename_to_find_data_save #(/) 演算子で新しいパスを構築
    path = new_floud_path_weathernews
    return path_bool
    
def weather_log():
    research()
    df = file_read()
    date_list = df['Date'].tolist()
    weather_list = df['Weather'].tolist()
        
    input_weather_info = int(input("天気はどうでしたか？ 晴れ：１ 曇り：２ 雨：３ 雪：４"))
    
    try:
        if input_weather_info == 1:
            weather_list.append('sun')
        elif input_weather_info == 2:
            weather_list.append('cloud')
        elif input_weather_info == 3:
            weather_list.append('rain')
        elif input_weather_info == 4:
            weather_list.append('snow')
        else:
            print('正しい値を入力してください')
    except ValueError:
        print('正しい値を入力してください')
    now = datetime.now()
    date_list.append(now)
    data = {'Date': date_list, 'Weather': weather_list}
    file_write(data)
    return 
    
def weather_log_check():
    df = file_read()
    categories_name = ['Weather data']
    sun_day_list = len(df[df['Weather'] == 'sun'])
    cloud_day_list = len(df[df['Weather'] == 'cloud'])
    rain_day_list = len(df[df['Weather'] == 'rain'])
    snow_day_list = len(df[df['Weather'] == 'snow'])
    total_day = len(df['Weather'])
    if total_day == 0:
        print('データがありません。\nデータを記録してください。また、同じディレクトリにCSVファイルがあるかどうか確認してください。')
        return

    df = pd.concat([df],ignore_index=True) 
    df['Date'] = pd.to_datetime(df['Date'])
    df['date_floor'] = df['Date'].dt.floor('D')
    date_list_dataframe = df['Date'].tolist()
    date_list = df['date_floor'].tolist()
    weather_list = df['Weather'].tolist()
    data = {'Date': date_list_dataframe, 'Weather': weather_list}
    sortData = file_write(data)
    
    x_indices = np.arange(len(categories_name))
    width = 0.25
    plt.figure(figsize = (10, 6))
    plt.bar(x_indices - width, sun_day_list, width, label='Sun', color='skyblue')
    plt.bar(x_indices, cloud_day_list, width, label='Cloud', color='coral')
    plt.bar(x_indices + width, rain_day_list, width, label='Rain', color='seagreen')
    plt.bar(x_indices + 2*width, snow_day_list, width, label='Snow', color='lightblue')
    plt.xticks(x_indices, categories_name)
    plt.legend()
    plt.figure(figsize = (10,6))
    plt.xticks(fontsize=8)
    plt.plot(date_list,weather_list)
    plt.tight_layout()
    plt.show()
    return print(f'\n{sortData}\n\n晴れ{sun_day_list}日間,曇り{cloud_day_list}日間,雨{rain_day_list}日間,雪{snow_day_list}日間\n合計{total_day}日間記録しています。')

def weather_calcuration():
    global p_1,p_2,p_3,p_4,p_5,today_weather_value,tomorrow,tomorrow_1,tomorrow_2,tomorrow_3,tomorrow_4
    
    df = file_read()
    df['Previous_Weather'] = df['Weather'].shift(1)

    try:
        transition_matrix = pd.crosstab(df['Previous_Weather'], 
                                df['Weather'], 
                                normalize='index') #百分率で返す
        p_1 = np.array([
            [transition_matrix.loc['sun','sun'], transition_matrix.loc['sun', 'cloud'], transition_matrix.loc['sun','rain'], transition_matrix.loc['sun', 'snow']],
            [transition_matrix.loc['rain','rain'], transition_matrix.loc['rain', 'sun'], transition_matrix.loc['rain','cloud'], transition_matrix.loc['rain', 'snow']],
            [transition_matrix.loc['cloud','cloud'], transition_matrix.loc['cloud', 'sun'], transition_matrix.loc['cloud','rain'], transition_matrix.loc['cloud', 'snow']],
            [transition_matrix.loc['snow','snow'], transition_matrix.loc['snow', 'sun'], transition_matrix.loc['snow','rain'], transition_matrix.loc['snow', 'cloud']]
        ])#1日後
        p_2 = p_1 @ p_1 #2日後の天気
        p_3 = p_2 @ p_1 #3日後の天気
        p_4 = p_3 @ p_1 #4日後の天気
        p_5 = p_4 @ p_1 #5日後の天気
    except (ValueError,TypeError):
        return print('データが足りないため予測することが出来ません。')

    today = date.today()
    tomorrow = today + timedelta(days = 1)
    tomorrow_1 = today + timedelta(days = 2)
    tomorrow_2 = today + timedelta(days = 3)
    tomorrow_3 = today + timedelta(days = 4)
    tomorrow_4 = today + timedelta(days = 5)
    today_weather = df['Weather'].tail(1)
    today_weather_value = today_weather.values

def weather_tomorrow():
    if today_weather_value == 'sun':
        baseline = max(math.floor(100 * p_1[0,0]) / 100 ,math.floor(100 * p_1[0,1]) / 100 ,math.floor(100 * p_1[0,2]) / 100 ,math.floor(100 * p_1[0,3]) / 100 )
        if math.floor(100 * p_1[0,0]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[0,1]) / 100  == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[0,2]) / 100  ==  baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[0,3]) / 100  == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            print('想定していないエラーです。')
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[0,0]) / 100}で晴れとなり、{math.floor(100 * p_2[0,1]) / 100}で曇りとなり、{math.floor(100 * p_2[0,2]) / 100}で雨となり、{math.floor(100 * p_2[0,3]) / 100}で雪となる'
    elif today_weather_value == 'rain':
        baseline = max(math.floor(100 * p_1[1,0]) / 100 ,math.floor(100 * p_1[1,1]) / 100 ,math.floor(100 * p_1[1,2]) / 100 ,math.floor(100 * p_1[1,3]) / 100 )
        if math.floor(100 * p_1[1,0]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[1,1]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[1,2]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[1,3]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            print('想定していないエラーです。')
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[1,0]) / 100}で雨となり、{math.floor(100 * p_2[1,1]) / 100}で晴れとなり、{math.floor(100 * p_2[1,2]) / 100}で曇りとなり、{math.floor(100 * p_2[1,3]) / 100}で雪となる'
    elif today_weather_value == 'cloud':
        baseline = max(math.floor(100 * p_1[2,0]) / 100 ,math.floor(100 * p_1[2,1]) / 100 ,math.floor(100 * p_1[2,2]) / 100 ,math.floor(100 * p_1[2,3]) / 100 )
        if math.floor(100 * p_1[2,0]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[2,1]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[2,2]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[2,3]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            print('想定していないエラーです。')
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[2,0]) / 100}で曇りとなりo、{math.floor(100 * p_2[2,1]) / 100}晴れとでとなり、{math.floor(100 * p_2[2,2]) / 100}で雨となり、{math.floor(100 * p_2[2,3]) / 100}で雪となる'
    elif today_weather_value == 'snow':
        baseline = max(math.floor(100 * p_1[2,0]) / 100 ,math.floor(100 * p_1[2,1]) / 100 ,math.floor(100 * p_1[2,2]) / 100 ,math.floor(100 * p_1[2,3]) / 100 )
        if math.floor(100 * p_1[3,0]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        elif math.floor(100 * p_1[3,1]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[3,2]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[3,3]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        else:
            print('想定していないエラーです。')
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[3,0]) / 100}で雪となり、{math.floor(100 * p_2[3,1]) / 100}で晴れとなり、{math.floor(100 * p_2[3,2]) / 100}で雨となり、{math.floor(100 * p_2[3,3]) / 100}で曇りとなる'
        
    return print(f'{tomorrow_weather}\n{tomorrow_1_weather}')
    
def weather_check_matrix():
    print('早見表\n'
          's > s , s > c , s > r , s > sn\n'
          'r > r , r > s , r > c , r > sn\n'
          'c > c , c > s , c > r , c > sn\n'
          'sn > sn , sn > s , sn > r , sn > c\n'
          f'{tomorrow}\n'
          f'{p_1}\n'
          f'{tomorrow_1}\n'
          f'{p_2}\n'
          f'{tomorrow_2}\n'
          f'{p_3}\n'
          f'{tomorrow_3}\n'
          f'{tomorrow_4}\n'
          f'{p_5}')

def reset():
    file_path = research()
    if file_path == True:
        select_reset = str(input(f'パス1(Python file)：{found_path_weathernews} \nパス2(CSV file)：{found_path_data_save})\n保存データが存在しますが、本当にリセットしますか？（Y/n）'))
        can_not_reset = 'リセットに失敗しました。\nファイルは存在します。'
    elif file_path == False:
        select_reset = str(input('本当にリセットしますか？（Y/n）'))
        can_not_reset = 'リセットに失敗しました。\nファイルが存在しません。'
        
    if select_reset == 'Y':
        try:
            os.remove(path)
            print('リセットしました。')
        except:
            print(can_not_reset)
    else:
        return print('キャンセルしました。')

def weather_control():
    try:
        input_control = int(input('==================== Weather AI System ====================\n'
                                  '記録：１ 確認：２ 予報：３ 終了：４ リセット：５ ファイル検索：６'))
        if input_control == 1:
            weather_log()
        elif input_control == 2:
            weather_log_check()
        elif input_control == 3:
            weather_calcuration()
            weather_tomorrow()
        elif input_control == 4:
            os._exit(0)
        elif input_control == 5:
            reset()
        elif input_control == 6:
            research()
            print(f'パス1(Python file)：{found_path_weathernews} \nパス2(CSV file)：{found_path_data_save}')
        elif input_control == 7:
            weather_calcuration()
            weather_check_matrix()
        else:
            print('正しい値を選択してください') 
    except ValueError as e:
        print(e)
        print('正しい値を選択してください')
    finally:
        print("プログラムを終了します。")
    
while True:
    weather_control()

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime , timedelta , date
import os 
import math
from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
import time
import customtkinter as ck
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tqdm import tqdm
import pathlib
import datetime as dt
import weather_config
import psutil

def file_read():
    global date_list,weather_list
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    try:
        df = pd.read_csv(path)
        df = df.sort_values('Date',ignore_index=True,ascending=True)
    except FileNotFoundError:
        txtBox.insert(tk.END,'\nCSVファイルを新規作成します。\n')
        txtBox.see(tk.END)
        txtBox.configure(state = "disabled")
        date_list = []
        weather_list = []
        data = {'Date':date_list,'Weather':weather_list}        
        df = pd.DataFrame(data)
        file_write(data)
    except:
        txtBox.insert(tk.END,'\n想定外のエラー\n')
        txtBox.see(tk.END)
        txtBox.configure(state = "disabled")
    finally:
        return df   
  
def file_write(data):
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    sortData = None
    try:
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        sortData = df.sort_values('Date',ignore_index=True,ascending=True)
        sortData.to_csv(path,index = False)
    except ValueError as e:
        print(e)
    except UnboundLocalError as e:
        print(e)
    except:
        txtBox.insert(tk.END,'\n書き込みに失敗しました。\n\n想定外のエラーです。\n')
        txtBox.see(tk.END)
        txtBox.configure(state = "disabled")
        sortData = 'None'
    finally:
        return sortData
 
def research():
    global path,path_bool,found_path_weathernews,found_path_data_save,found_path_tflite,found_path_config
    t1 = time.perf_counter()
    pbar = tqdm(total = 100)
    filename_to_find_weathernews = "weathernews_GUI.py"
    filename_to_find_data_save = 'weather_data_save.csv'
    filename_to_find_tflite = "weather_model.tflite"
    filename_to_find_config = "weather_config.py"
    search_start_dir = Path.home()#検索を開始するディレクトリを指定
    pbar.n = 10
    pbar.refresh()
    progressbar.set(0.10)
    root_progress.update()
    
    found_path_weathernews = None
    found_path_data_save = None
    found_path_tflite = None
    found_path_config = None
    pbar.n = 20
    pbar.refresh()
    progressbar.set(0.20)
    root_progress.update()
    
    for path_weathernews in search_start_dir.rglob(filename_to_find_weathernews):# rglobはジェネレータを返すため、forループで順に試す
        found_path_weathernews = path_weathernews.resolve()
        print(f'ディレクトリ：{search_start_dir}から検索中（1/4）…')
        pbar.n = 30
        pbar.refresh()
        progressbar.set(0.30)
        root_progress.update()
    for path_data_save in search_start_dir.rglob(filename_to_find_data_save):# rglobはジェネレータを返すため、forループで順に試す
        found_path_data_save = path_data_save.resolve()
        print(f'ディレクトリ：{search_start_dir}から検索中（2/4）…')
        pbar.n = 40
        pbar.refresh()
        progressbar.set(0.40)
        root_progress.update()
    for path_tflite in search_start_dir.rglob(filename_to_find_tflite):# rglobはジェネレータを返すため、forループで順に試す
        found_path_tflite = path_tflite.resolve()
        print(f'ディレクトリ：{search_start_dir}から検索中（3/4）…')
        pbar.n = 50
        pbar.refresh()
        progressbar.set(0.50)
        root_progress.update()
    for path_config in search_start_dir.rglob(filename_to_find_config):# rglobはジェネレータを返すため、forループで順に試す
        found_path_config = path_config.resolve()
        print(f'ディレクトリ：{search_start_dir}から検索中（4/4）…')
        pbar.n = 60
        pbar.refresh()
        progressbar.set(0.60)
        root_progress.update()
        
    if not found_path_weathernews:
        found_path_weathernews = '存在しません。'
        path_bool = False
    elif not found_path_data_save:
        found_path_data_save = '存在しません。'
        path_bool = False
    elif not found_path_tflite:
        found_path_tflite = '存在しません。'
        path_bool = False
    elif not found_path_config:
        found_path_config = "存在しません"
    else:
        path_bool = True
    pbar.n = 70
    pbar.refresh()
    progressbar.set(0.70)
    root_progress.update()
    
    parent_dir = found_path_weathernews.parent #親ディレクトリを取得
    pbar.n = 80
    pbar.refresh()
    progressbar.set(0.80)
    root_progress.update()
    new_floud_path_weathernews = parent_dir / filename_to_find_data_save#(/) 演算子で新しいパスを構築
    pbar.n = 90
    pbar.refresh()
    progressbar.set(0.90)
    root_progress.update()
    path = new_floud_path_weathernews
    pbar.n = 100
    pbar.refresh()
    progressbar.set(1.0)
    root_progress.update()
    time.sleep(1)
    
    progressbar.set(0)
    root_progress.update
    t2 = time.perf_counter()
    elap_time = t2 - t1
    print(f"起動時間{elap_time: .2f}")
    return path_bool  

def research_display():
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    txtBox.insert(tk.END,f'\nパス1(Python File)：\n{found_path_weathernews} \n\nパス2(CSV File)：\n{found_path_data_save}\n\nパス3(TensorFlowLite File)\n{found_path_tflite}\n\nパス4(Config File)\n{found_path_config}\n')
    txtBox.see(tk.END)
    txtBox.configure(state = "disabled")
    
def weather_log():
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    df = file_read()
    date_list = df['Date'].tolist()
    weather_list = df['Weather'].tolist()
        
    def weather_choice(weather_type):
        weather_list.append(weather_type) # リストに追加
        wait_var.set(1)
    txtBox.insert(tk.END,"\n天気はどうでしたか？ 晴れ：１ 曇り：２ 雨：３ 雪：４\n")
    txtBox.see(tk.END)
    txtBox.configure(state = "disabled")
    wait_var = tk.IntVar() #操作待機
    button_sun.bind('<Button-1>',lambda e : weather_choice('sun'))#操作待機解除
    button_cloud.bind('<Button-1>',lambda e: weather_choice('cloud'))
    button_rain.bind('<Button-1>',lambda e: weather_choice('rain'))
    button_snow.bind('<Button-1>',lambda e :weather_choice('snow'))
    button_sun.wait_variable(wait_var)

    now = datetime.now()
    date_list.append(now)
    data = {'Date': date_list, 'Weather': weather_list}
    file_write(data)
    txtBox.insert(tk.END,'\n書き込みに成功しました\n')
    txtBox.see(tk.END)
    txtBox.configure(state = "disabled")
    return 

def weather_log_image():
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    root_image = ck.CTk()
    root_image.withdraw() 
    root_image.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="今日の天気の画像を選択してください",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    root_image.destroy() 
    
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'# ログ抑制
    files = [found_path_tflite]
    df = file_read()
    date_list = df['Date'].tolist()
    weather_list = df['Weather'].tolist()
    
    model_path = files[0] if files else None#モデル検索
    if not model_path:
        print("tflite ファイルが見つかりません。")
        return
    class_names = ['sun', 'cloud', 'rain', 'snow']
        
    try:
        with open(model_path, 'rb') as f: #モデル読み込み（日本語パス文字化け対策済み）
            model_content = f.read()
        interpreter = tf.lite.Interpreter(model_content=model_content)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
    except Exception as e:
        print(f"モデル読み込みエラー: {e}")
        return
    image_path = file_path
    if not image_path:
        print("画像が選択されませんでした。終了します。")
        return

    try:
        img = image.load_img(image_path, target_size=(224,224))#画像選択と処理
        img_array = image.img_to_array(img)
        normalized_img = (img_array.astype(np.float32) / 127.5) - 1  # 正規化 (MobileNetV2などを想定して -1〜1 に正規化)
        input_tensor = np.expand_dims(normalized_img, axis=0)
        interpreter.set_tensor(input_details[0]['index'], input_tensor) #推論
        interpreter.invoke()
        score = interpreter.get_tensor(output_details[0]['index'])[0]
        predicted_idx = np.argmax(score)
        predicted_label = class_names[predicted_idx] if predicted_idx < len(class_names) else str(predicted_idx)
    except Exception as e:
        print(f"画像処理エラー: {e}")
        return
    
    weather_list.append(predicted_label)
    now = datetime.now()
    date_list.append(now)
    data = {'Date': date_list, 'Weather': weather_list}
    file_write(data)
    txtBox.insert(tk.END,'\n書き込みに成功しました\n')
    txtBox.see(tk.END)
    txtBox.configure(state = "disabled")
    return 
    
def weather_log_check():
    df = file_read()
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    sun_day_list = len(df[df['Weather'] == 'sun'])
    cloud_day_list = len(df[df['Weather'] == 'cloud'])
    rain_day_list = len(df[df['Weather'] == 'rain'])
    snow_day_list = len(df[df['Weather'] == 'snow'])
    total_day = len(df['Weather'])
    if total_day == 0:
        txtBox.insert(tk.END,'\nデータがありません。\n\nデータを記録してください。\n\nまた、同じディレクトリにCSVファイルがあるかどうか確認してください。\n')
        txtBox.see(tk.END)
        txtBox.configure(state = "disabled")
        return

    df = pd.concat([df],ignore_index=True) 
    df['Date'] = pd.to_datetime(df['Date'])
    df['date_floor'] = df['Date'].dt.floor('D')
    date_list_dataframe = df['Date'].tolist()
    date_list = df['date_floor'].tolist()
    weather_list = df['Weather'].tolist()
    data = {'Date': date_list_dataframe, 'Weather': weather_list}
    sortData = file_write(data)
    
    fig = Figure(figsize = (5,6), dpi =100)
    ax1 = fig.add_subplot(211)
    ax1_categories_name = ['Figure1 weather count']
    ax1_x_indices = np.arange(len(ax1_categories_name))
    width = 0.2
    ax1.bar(ax1_x_indices - width, sun_day_list, width, label='Sun', color='skyblue')
    ax1.bar(ax1_x_indices, cloud_day_list, width, label='Cloud', color='coral')
    ax1.bar(ax1_x_indices + width, rain_day_list, width, label='Rain', color='seagreen')
    ax1.bar(ax1_x_indices + 2*width, snow_day_list, width, label='Snow', color='lightblue')
    ax1.xaxis.label.set_visible(False)
    ax1.get_xaxis().set_visible(False)
    ax1.set_title('Figure1 weather count')
    ax1.legend()
    
    ax2 = fig.add_subplot(212)
    ax2.plot(date_list,weather_list)
    ax2.set_title('Figure2 relation weather and date')
    ax2.legend()
    
    canvas = FigureCanvasTkAgg(fig, master = txtBox)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    try:
        txtBox._textbox.window_create(tk.END, window=canvas_widget)
    except AttributeError:
        txtBox.window_create(tk.END, window=canvas_widget)
    txtBox.insert(tk.END,f'\n{sortData}\n\n晴れ{sun_day_list}日間,曇り{cloud_day_list}日間,雨{rain_day_list}日間,雪{snow_day_list}日間\n\n合計{total_day}日間記録しています。\n')
    txtBox.see(tk.END)
    txtBox.configure(state = "disabled")
    return

def weather_calcuration():
    global p_1, p_2, p_3, p_4, p_5,today_weather_value, past_weather_value,tomorrow, tomorrow_1, tomorrow_2, tomorrow_3, tomorrow_4, p_1_result, p_2_result, p_3_result, p_4_result, p_5_result, p_1min,p_2min,p_3min,p_4min,p_5min,p_1max,p_2max,p_3max,p_4max,p_5max,p_1avg,p_2avg,p_3avg,p_4avg,p_5avg, p_1sen, p_2sen, p_3sen,p_4sen, p_5sen, p_1var, p_2var, p_3var, p_4var, p_5var, p_1std, p_2std, p_3std, p_4std, p_5std

    df = file_read()

    df['Prev'] = df['Weather'].shift(1)
    df['Prev2'] = df['Weather'].shift(2)
    df = df.dropna()

    df['State'] = df['Prev2'] + "_" + df['Prev']

    try:
        trans_prob = pd.crosstab(df['State'], df['Weather'], normalize='index')

        expected_states = [
            f"{w1}_{w2}" 
            for w1 in ['sun', 'cloud', 'rain', 'snow'] 
            for w2 in ['sun', 'cloud', 'rain', 'snow']
        ]
        trans_prob = trans_prob.reindex(index=expected_states, columns=['sun', 'cloud', 'rain', 'snow'], fill_value=0) # 枠に合わせて表を強制整形し、空白を0で埋める
        m = trans_prob 
        
        p_1 = np.array([
            # 0: sun_sunからの遷移
            [m.loc['sun_sun','sun'], m.loc['sun_sun','cloud'], m.loc['sun_sun','rain'], m.loc['sun_sun','snow'], 0,0,0,0, 0,0,0,0, 0,0,0,0],
            # 1: cloud_sun からの遷移
            [m.loc['cloud_sun','sun'], m.loc['cloud_sun','cloud'], m.loc['cloud_sun','rain'], m.loc['cloud_sun','snow'], 0,0,0,0, 0,0,0,0, 0,0,0,0],
            # 2: rain_sun からの遷移
            [m.loc['rain_sun','sun'], m.loc['rain_sun','cloud'], m.loc['rain_sun','rain'], m.loc['rain_sun','snow'], 0,0,0,0, 0,0,0,0, 0,0,0,0],
            # 3: snow_sun からの遷移
            [m.loc['snow_sun','sun'], m.loc['snow_sun','cloud'], m.loc['snow_sun','rain'], m.loc['snow_sun','snow'], 0,0,0,0, 0,0,0,0, 0,0,0,0],

            # 4: sun_cloudからの遷移
            [0,0,0,0, m.loc['sun_cloud','sun'], m.loc['sun_cloud','cloud'], m.loc['sun_cloud','rain'], m.loc['sun_cloud','snow'], 0,0,0,0, 0,0,0,0],
            # 5: cloud_cloud からの遷移
            [0,0,0,0, m.loc['cloud_cloud','sun'], m.loc['cloud_cloud','cloud'], m.loc['cloud_cloud','rain'], m.loc['cloud_cloud','snow'], 0,0,0,0, 0,0,0,0],
            # 6: rain_cloud からの遷移
            [0,0,0,0, m.loc['rain_cloud','sun'], m.loc['rain_cloud','cloud'], m.loc['rain_cloud','rain'], m.loc['rain_cloud','snow'], 0,0,0,0, 0,0,0,0],
            # 7: snow_cloud からの遷移
            [0,0,0,0, m.loc['snow_cloud','sun'], m.loc['snow_cloud','cloud'], m.loc['snow_cloud','rain'], m.loc['snow_cloud','snow'], 0,0,0,0, 0,0,0,0],

            # 8: sun_rain からの遷移
            [0,0,0,0, 0,0,0,0, m.loc['sun_rain','sun'], m.loc['sun_rain','cloud'], m.loc['sun_rain','rain'], m.loc['sun_rain','snow'], 0,0,0,0],
            # 9: cloud_rain からの遷移
            [0,0,0,0, 0,0,0,0, m.loc['cloud_rain','sun'], m.loc['cloud_rain','cloud'], m.loc['cloud_rain','rain'], m.loc['cloud_rain','snow'], 0,0,0,0],
            # 10: rain_rain からの遷移
            [0,0,0,0, 0,0,0,0, m.loc['rain_rain','sun'], m.loc['rain_rain','cloud'], m.loc['rain_rain','rain'], m.loc['rain_rain','snow'], 0,0,0,0],
            # 11: snow_rain からの遷移
            [0,0,0,0, 0,0,0,0, m.loc['snow_rain','sun'], m.loc['snow_rain','cloud'], m.loc['snow_rain','rain'], m.loc['snow_rain','snow'], 0,0,0,0],

            # 12: sun_snow からの遷移
            [0,0,0,0, 0,0,0,0, 0,0,0,0, m.loc['sun_snow','sun'], m.loc['sun_snow','cloud'], m.loc['sun_snow','rain'], m.loc['sun_snow','snow']],
            # 13: cloud_snow からの遷移
            [0,0,0,0, 0,0,0,0, 0,0,0,0, m.loc['cloud_snow','sun'], m.loc['cloud_snow','cloud'], m.loc['cloud_snow','rain'], m.loc['cloud_snow','snow']],
            # 14: rain_snow からの遷移
            [0,0,0,0, 0,0,0,0, 0,0,0,0, m.loc['rain_snow','sun'], m.loc['rain_snow','cloud'], m.loc['rain_snow','rain'], m.loc['rain_snow','snow']],
            # 15: snow_snow からの遷移
            [0,0,0,0, 0,0,0,0, 0,0,0,0, m.loc['snow_snow','sun'], m.loc['snow_snow','cloud'], m.loc['snow_snow','rain'], m.loc['snow_snow','snow']]
        ])#1日後
        p_2 = p_1 @ p_1#2日後
        p_3 = p_2 @ p_1#3日後
        p_4 = p_3 @ p_1#4日後
        p_5 = p_4 @ p_1#5日後
        p_1_row_sums = p_1.sum(axis=1)
        p_2_row_sums = p_2.sum(axis = 1)
        p_3_row_sums = p_3.sum(axis = 1)
        p_4_row_sums = p_4.sum(axis = 1)
        p_5_row_sums = p_5.sum(axis = 1)
        if np.all(np.isclose(p_1_row_sums, 1)):
            p_1_result = "OK"
        else:
            p_1_result = "NG"
        if np.all(np.isclose(p_2_row_sums, 1)):
            p_2_result = "OK"
        else:
            p_2_result = "NG"
        if np.all(np.isclose(p_3_row_sums, 1)):
            p_3_result = "OK"
        else:
            p_3_result = "NG"
        if np.all(np.isclose(p_4_row_sums, 1)):
            p_4_result = "OK"
        else:
            p_4_result = "NG"
        if np.all(np.isclose(p_5_row_sums, 1)):
            p_5_result = "OK"
        else:
            p_5_result = "NG"
        p_1max = p_1[1.0 > p_1].max()
        p_2max = p_2[1.0 > p_2].max()
        p_3max = p_3[1.0 > p_3].max()
        p_4max = p_4[1.0 > p_4].max()
        p_5max = p_5[1.0 > p_5].max()
        p_1min = p_1[p_1 > 0].min()
        p_2min = p_2[p_2 > 0].min()
        p_3min = p_3[p_3 > 0].min()
        p_4min = p_4[p_4 > 0].min()
        p_5min = p_5[p_5 > 0].min()
        p_1avg = p_1[p_1 > 0].mean()
        p_2avg = p_2[p_2 > 0].mean()
        p_3avg = p_3[p_3 > 0].mean()
        p_4avg = p_4[p_4 > 0].mean()
        p_5avg = p_5[p_5 > 0].mean()
        p_1sen = np.median(p_1[p_1 > 0])
        p_2sen = np.median(p_2[p_2 > 0])
        p_3sen = np.median(p_3[p_3 > 0])  
        p_4sen = np.median(p_4[p_4 > 0])
        p_5sen = np.median(p_5[p_5 > 0])
        p_1var = np.var(p_1[p_1 > 0])
        p_2var = np.var(p_2[p_2 > 0])
        p_3var = np.var(p_3[p_3 > 0])
        p_4var = np.var(p_4[p_4 > 0])
        p_5var = np.var(p_5[p_5 > 0])
        p_1std = np.std(p_1[p_1 > 0])
        p_2std = np.std(p_2[p_2 > 0])
        p_3std = np.std(p_3[p_3 > 0])
        p_4std = np.std(p_4[p_4 > 0])
        p_5std = np.std(p_5[p_5 > 0])
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return
    
    today = date.today()
    tomorrow = today + timedelta(days = 1)
    tomorrow_1 = today + timedelta(days = 2)
    tomorrow_2 = today + timedelta(days = 3)
    tomorrow_3 = today + timedelta(days = 4)
    tomorrow_4 = today + timedelta(days = 5)
    today_weather_value = df['Weather'].iloc[1] # 今日とは限らない　した同じ
    past_weather_value = df['Weather'].iloc[2]

def weather_tomorrow():
    weather_calcuration()
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    if past_weather_value == 'sun' and today_weather_value == 'sun':
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
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[0,0]) / 100}で晴れとなり、{math.floor(100 * p_2[0,1]) / 100}で曇りとなり、{math.floor(100 * p_2[0,2]) / 100}で雨となり、{math.floor(100 * p_2[0,3]) / 100}で雪となる'
    elif past_weather_value == 'cloud' and today_weather_value == 'sun':
        baseline = max(math.floor(100 * p_1[1,0]) / 100 ,math.floor(100 * p_1[1,1]) / 100 ,math.floor(100 * p_1[1,2]) / 100 ,math.floor(100 * p_1[1,3]) / 100 )
        if math.floor(100 * p_1[1,0]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[1,1]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[1,2]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[1,3]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[1,0]) / 100}で晴れとなり、{math.floor(100 * p_2[1,1]) / 100}で曇りとなり、{math.floor(100 * p_2[1,2]) / 100}で雨となり、{math.floor(100 * p_2[1,3]) / 100}で雪となる'
    elif past_weather_value == 'rain' and today_weather_value == 'sun':
        baseline = max(math.floor(100 * p_1[2,0]) / 100 ,math.floor(100 * p_1[2,1]) / 100 ,math.floor(100 * p_1[2,2]) / 100 ,math.floor(100 * p_1[2,3]) / 100 )
        if math.floor(100 * p_1[2,0]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[2,1]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[2,2]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[2,3]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[2,0]) / 100}で晴れとなり、{math.floor(100 * p_2[2,1]) / 100}曇りとでとなり、{math.floor(100 * p_2[2,2]) / 100}で雨となり、{math.floor(100 * p_2[2,3]) / 100}で雪となる'
    elif past_weather_value == 'snow' and today_weather_value == 'sun':
        baseline = max(math.floor(100 * p_1[3,0]) / 100 ,math.floor(100 * p_1[3,1]) / 100 ,math.floor(100 * p_1[3,2]) / 100 ,math.floor(100 * p_1[3,3]) / 100 )
        if math.floor(100 * p_1[3,0]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[3,1]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[3,2]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[3,3]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[3,0]) / 100}で晴れとなり、{math.floor(100 * p_2[3,1]) / 100}で曇りとなり、{math.floor(100 * p_2[3,2]) / 100}で雨となり、{math.floor(100 * p_2[3,3]) / 100}で雪となる'
    elif past_weather_value == 'sun' and today_weather_value == 'cloud':
        baseline = max(math.floor(100 * p_1[4,4]) / 100 ,math.floor(100 * p_1[4,5]) / 100 ,math.floor(100 * p_1[4,6]) / 100 ,math.floor(100 * p_1[4,7]) / 100 )
        if math.floor(100 * p_1[4,4]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[4,5]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[4,6]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[4,7]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[4,4]) / 100}で晴れとなり、{math.floor(100 * p_2[4,5]) / 100}で曇りとなり、{math.floor(100 * p_2[4,6]) / 100}で雨となり、{math.floor(100 * p_2[4,7]) / 100}で雪となる'
    elif past_weather_value == 'cloud' and today_weather_value == 'cloud':
        baseline = max(math.floor(100 * p_1[5,4]) / 100 ,math.floor(100 * p_1[5,5]) / 100 ,math.floor(100 * p_1[5,6]) / 100 ,math.floor(100 * p_1[5,7]) / 100 )
        if math.floor(100 * p_1[5,4]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[5,5]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[5,6]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[5,7]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[5,4]) / 100}で晴れとなり、{math.floor(100 * p_2[5,5]) / 100}で曇りとなり、{math.floor(100 * p_2[5,6]) / 100}で雨となり、{math.floor(100 * p_2[5,7]) / 100}で雪となる'
    elif past_weather_value == 'rain' and today_weather_value == 'cloud':
        baseline = max(math.floor(100 * p_1[6,4]) / 100 ,math.floor(100 * p_1[6,5]) / 100 ,math.floor(100 * p_1[6,6]) / 100 ,math.floor(100 * p_1[6,7]) / 100 )
        if math.floor(100 * p_1[6,4]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[6,5]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[6,6]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[6,7]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[6,4]) / 100}で晴れとなり、{math.floor(100 * p_2[6,5]) / 100}で曇りとなり、{math.floor(100 * p_2[6,6]) / 100}で雨となり、{math.floor(100 * p_2[6,7]) / 100}で雪となる'
    elif past_weather_value == 'snow' and today_weather_value == 'cloud':
        baseline = max(math.floor(100 * p_1[7,4]) / 100 ,math.floor(100 * p_1[7,5]) / 100 ,math.floor(100 * p_1[7,6]) / 100 ,math.floor(100 * p_1[7,7]) / 100 )
        if math.floor(100 * p_1[7,4]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[7,5]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[7,6]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[7,7]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[7,4]) / 100}で晴れとなり、{math.floor(100 * p_2[7,5]) / 100}で曇りとなり、{math.floor(100 * p_2[7,6]) / 100}で雨となり、{math.floor(100 * p_2[7,7]) / 100}で雪となる'
    elif past_weather_value == 'sun' and today_weather_value == 'rain':
        baseline = max(math.floor(100 * p_1[8,8]) / 100 ,math.floor(100 * p_1[8,9]) / 100 ,math.floor(100 * p_1[8,10]) / 100 ,math.floor(100 * p_1[8,11]) / 100 )
        if math.floor(100 * p_1[8,8]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[8,9]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[8,10]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[8,11]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[8,8]) / 100}で晴れとなり、{math.floor(100 * p_2[8,9]) / 100}で曇りとなり、{math.floor(100 * p_2[8,10]) / 100}で雨となり、{math.floor(100 * p_2[8,11]) / 100}で雪となる'
    elif past_weather_value == 'cloud' and today_weather_value == 'rain':
        baseline = max(math.floor(100 * p_1[9,8]) / 100 ,math.floor(100 * p_1[9,9]) / 100 ,math.floor(100 * p_1[9,10]) / 100 ,math.floor(100 * p_1[9,11]) / 100 )
        if math.floor(100 * p_1[9,8]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[9,9]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[9,10]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[9,11]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[9,8]) / 100}で晴れとなり、{math.floor(100 * p_2[9,9]) / 100}で曇りとなり、{math.floor(100 * p_2[9,10]) / 100}で雨となり、{math.floor(100 * p_2[9,11]) / 100}で雪となる'
    elif past_weather_value == 'rain' and today_weather_value == 'rain':
        baseline = max(math.floor(100 * p_1[10,8]) / 100 ,math.floor(100 * p_1[10,9]) / 100 ,math.floor(100 * p_1[10,10]) / 100 ,math.floor(100 * p_1[10,11]) / 100 )
        if math.floor(100 * p_1[10,8]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[10,9]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[10,10]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[10,11]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[10,8]) / 100}で晴れとなり、{math.floor(100 * p_2[10,9]) / 100}で曇りとなり、{math.floor(100 * p_2[10,10]) / 100}で雨となり、{math.floor(100 * p_2[10,11]) / 100}で雪となる'
    elif past_weather_value == 'snow' and today_weather_value == 'rain':
        baseline = max(math.floor(100 * p_1[11,8]) / 100 ,math.floor(100 * p_1[11,9]) / 100 ,math.floor(100 * p_1[11,10]) / 100 ,math.floor(100 * p_1[11,11]) / 100 )
        if math.floor(100 * p_1[11,8]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[11,9]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[11,10]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[11,11]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[11,8]) / 100}で晴れとなり、{math.floor(100 * p_2[11,9]) / 100}で曇りとなり、{math.floor(100 * p_2[11,10]) / 100}で雨となり、{math.floor(100 * p_2[11,11]) / 100}で雪となる'
    elif past_weather_value == 'sun' and today_weather_value == 'snow':
        baseline = max(math.floor(100 * p_1[12,12]) / 100 ,math.floor(100 * p_1[12,13]) / 100 ,math.floor(100 * p_1[12,14]) / 100 ,math.floor(100 * p_1[12,15]) / 100 )
        if math.floor(100 * p_1[12,12]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[12,13]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[12,14]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[12,15]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[12,12]) / 100}で晴れとなり、{math.floor(100 * p_2[12,13]) / 100}で曇りとなり、{math.floor(100 * p_2[12,14]) / 100}で雨となり、{math.floor(100 * p_2[12,15]) / 100}で雪となる'
    elif past_weather_value == 'cloud' and today_weather_value == 'snow':
        baseline = max(math.floor(100 * p_1[13,12]) / 100 ,math.floor(100 * p_1[13,13]) / 100 ,math.floor(100 * p_1[13,14]) / 100 ,math.floor(100 * p_1[13,15]) / 100 )
        if math.floor(100 * p_1[13,12]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[13,13]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[13,14]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[13,15]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[13,12]) / 100}で晴れとなり、{math.floor(100 * p_2[13,13]) / 100}で曇りとなり、{math.floor(100 * p_2[13,14]) / 100}で雨となり、{math.floor(100 * p_2[13,15]) / 100}で雪となる'
    elif past_weather_value == 'rain' and today_weather_value == 'snow':
        baseline = max(math.floor(100 * p_1[14,12]) / 100 ,math.floor(100 * p_1[14,13]) / 100 ,math.floor(100 * p_1[14,14]) / 100 ,math.floor(100 * p_1[14,15]) / 100 )
        if math.floor(100 * p_1[14,12]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[14,13]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[14,14]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[14,15]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[14,12]) / 100}で晴れとなり、{math.floor(100 * p_2[14,13]) / 100}で曇りとなり、{math.floor(100 * p_2[14,14]) / 100}で雨となり、{math.floor(100 * p_2[14,15]) / 100}で雪となる'
    elif past_weather_value == 'snow' and today_weather_value == 'snow':
        baseline = max(math.floor(100 * p_1[15,12]) / 100 ,math.floor(100 * p_1[15,13]) / 100 ,math.floor(100 * p_1[15,14]) / 100 ,math.floor(100 * p_1[15,15]) / 100 )
        if math.floor(100 * p_1[15,12]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は晴れです'
        elif math.floor(100 * p_1[15,13]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は曇りです'
        elif math.floor(100 * p_1[15,14]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雨です'
        elif math.floor(100 * p_1[15,15]) / 100 == baseline:
            tomorrow_weather = f'{tomorrow}の天気は雪です'
        else:
            txtBox.insert(tk.END,'\n想定していないエラーです。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        tomorrow_1_weather = f'{tomorrow_1}は、{math.floor(100 * p_2[15,12]) / 100}で晴れとなり、{math.floor(100 * p_2[15,13]) / 100}で曇りとなり、{math.floor(100 * p_2[15,14]) / 100}で雨となり、{math.floor(100 * p_2[15,15]) / 100}で雪となる'
    txtBox.insert(tk.END,f'\n{tomorrow_weather}\n\n{tomorrow_1_weather}\n')
    txtBox.see(tk.END)
    txtBox.configure(state = "disabled")
    return  
    
def weather_matrix_display():
    weather_calcuration()
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    txtBox.insert(tk.END,'\n\n開発者モード\n\n'
            '\n早見表\n\n'
            '--- 1日前が「晴れ(s)」のグループ ---\n\n'
            '行0 [s_s] : s > s > s ,  s > s > c ,  s > s > r ,  s > s > sn\n\n'
            '行1 [c_s] : c > s > s ,  c > s > c ,  c > s > r ,  c > s > sn\n\n'
            '行2 [r_s] : r > s > s ,  r > s > c ,  r > s > r ,  r > s > sn\n\n'
            '行3 [sn_s]: sn > s > s , sn > s > c , sn > s > r , sn > s > sn\n\n'
            '--- 1日前が「曇り(c)」のグループ ---\n\n'
            '行4 [s_c] : s > c > s ,  s > c > c ,  s > c > r ,  s > c > sn\n\n'
            '行5 [c_c] : c > c > s ,  c > c > c ,  c > c > r ,  c > c > sn\n\n'
            '行6 [r_c] : r > c > s ,  r > c > c ,  r > c > r ,  r > c > sn\n\n'
            '行7 [sn_c]: sn > c > s , sn > c > c , sn > c > r , sn > c > sn\n\n'
            '--- 1日前が「雨(r)」のグループ ---\n\n'
            '行8 [s_r] : s > r > s ,  s > r > c ,  s > r > r ,  s > r > sn\n\n'
            '行9 [c_r] : c > r > s ,  c > r > c ,  c > r > r ,  c > r > sn\n\n'
            '行10[r_r] : r > r > s ,  r > r > c ,  r > r > r ,  r > r > sn\n\n'
            '行11[sn_r]: sn > r > s , sn > r > c , sn > r > r , sn > r > sn\n\n'
            '--- 1日前が「雪(sn)」のグループ ---\n\n'
            '行12[s_sn] : s > sn > s , s > sn > c , s > sn > r , s > sn > sn\n\n'
            '行13[c_sn] : c > sn > s , c > sn > c , c > sn > r , c > sn > sn\n\n'
            '行14[r_sn] : r > sn > s , r > sn > c , r > sn > r , r > sn > sn\n\n' 
          f"p_1info\n確率モデルp_1の状態：{p_1_result}\n最小値：{p_1min},\n最大値：{p_1max},\n平均値：{p_1avg}\n中央値：{p_1sen}\n分散：{p_1var}\n標準偏差：{p_1std}\n\n"
          f"p_2info\n確率モデルp_2の状態：{p_2_result}\n最小値：{p_2min},\n最大値：{p_2max},\n平均値：{p_2avg}\n中央値：{p_2sen}\n分散：{p_2var}\n標準偏差：{p_2std}\n\n"
          f"p_3info\n確率モデルp_3の状態：{p_3_result}\n最小値：{p_3min},\n最大値：{p_3max},\n平均値：{p_3avg}\n中央値：{p_3sen}\n分散：{p_3var}\n標準偏差：{p_3std}\n\n"
          f"p_4info\n確率モデルp_4の状態：{p_4_result}\n最小値：{p_4min},\n最大値：{p_4max},\n平均値：{p_4avg}\n中央値：{p_4sen}\n分散：{p_4var}\n標準偏差：{p_4std}\n\n"
          f"p_5info\n確率モデルp_5の状態：{p_5_result}\n最小値：{p_5min},\n最大値：{p_5max},\n平均値：{p_5avg}\n中央値：{p_5sen}\n分散：{p_5var}\n標準偏差：{p_5std}\n\n"
          f'{tomorrow}\n\n'
          f'{p_1}\n\n'
          f'{tomorrow_1}\n\n'
          f'{p_2}\n\n'
          f'{tomorrow_2}\n\n'
          f'{p_3}\n\n'
          f'{tomorrow_3}\n\n'
          f'{p_4}\n\n'
          f'{tomorrow_4}\n\n'
          f'{p_5}\n')

def reset():
    ck.set_appearance_mode("system")
    root_end = ck.CTk()
    root_end.title('リセットしますか？')
    root_end.geometry("600x350")
    root_end.state("normal")
    label = ck.CTkLabel(root_end, text = 'リセットしますか？', text_color= ("black", "white"), font = (weather_config.FONT_FAMILY, 20))
    label.pack()
    txtBox = ck.CTkTextbox(root_end,height = 250, width = 500,fg_color=("white", "black"), text_color=(weather_config.FONT_COLOR), font = (weather_config.FONT_FAMILY, 20))
    txtBox.pack()
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    btn_yes = ck.CTkButton(root_end, text = 'はい', height = 50, width = 150,fg_color=(weather_config.FG_COLOR), text_color=(weather_config.FONT_COLOR),font = (weather_config.FONT_FAMILY, 18))
    btn_no = ck.CTkButton(root_end, text = "いいえ", height = 50, width = 150,fg_color=(weather_config.FG_COLOR), text_color=(weather_config.FONT_COLOR),font = (weather_config.FONT_FAMILY, 18))
    btn_yes.place(x = 100, y= 300)
    btn_no.place(x = 300, y = 300)
    file_path = path_bool
    if file_path == True:
        txtBox.insert(tk.END,f'CSV file：\n{found_path_data_save}\n\n保存データが存在しますが、本当にリセットしますか？（はい/いいえ）\n')
        txtBox.see(tk.END)
        txtBox.configure(state = "disabled")
        can_not_reset = '\nリセットに失敗しました。\nファイルは存在します。\n'
    elif file_path == False:
        txtBox.insert(tk.END,input('\n本当にリセットしますか？（はい/いいえ）\n'))
        txtBox.see(tk.END)
        txtBox.configure(state = "disabled")
        can_not_reset = '\nリセットに失敗しました。\nファイルが存在しません。\n'
        
    def reset_do(event):
        try:
            os.remove(path)
            txtBox.insert(tk.END,'\nリセットしました。\n')
            txtBox.see(tk.END)
            txtBox.configure(state = "disabled")
        except:
            txtBox.insert(tk.END,can_not_reset) 
    def reset_cancel(event):
        txtBox.insert(tk.END, '\nキャンセルしました。\n')
        txtBox.see(tk.END)
        txtBox.configure(state = "disabled")
        time.sleep(1)
        root_end.destroy()
    
    btn_yes.bind('<Button-1>', reset_do)
    btn_no.bind('<Button-1>', reset_cancel)    
    txtBox.configure(state = "disabled")

def end():
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    txtBox.insert(tk.END,'終了します。')
    txtBox.see(tk.END)
    time.sleep(1)
    txtBox.configure(state = "disabled")
    root.destroy()

def info_display():
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    txtBox.insert(tk.END,f'\nマルコフ連鎖天気予報 ver{weather_config.VER_INFO}\n'
                  '\n作成日：2025年11月12日\n'
                  '\n作成者：RI\n')
    txtBox.see(tk.END)
    path = pathlib.Path(found_path_weathernews)
    if path.exists():
        stats = path.stat()
        txtBox.insert(tk.END,"\n【基本情報(Python file)】\n"
                      f"\nファイル名:{path.name}\n"
                      f"\n絶対パス:{path.absolute()}\n"
                      f"\nサイズ:{stats.st_size}バイト({stats.st_size / 1024 : .2f}KB)\n"
                      "\n【タイムスタンプ】\n"
                      f"\n作成時刻:{dt.datetime.fromtimestamp(stats.st_ctime)}\n"
                      f"\n更新時刻:{dt.datetime.fromtimestamp(stats.st_mtime)}\n"
                      f"\nアクセス時刻:{dt.datetime.fromtimestamp(stats.st_atime)}\n")
        txtBox.see(tk.END)
    else:
        txtBox.insert(tk.END,f"エラー: '{found_path_weathernews}' は現在のディレクトリに見つかりませんでした。")
        txtBox.see(tk.END)
    path = pathlib.Path(found_path_data_save)
    if path.exists():
        stats = path.stat()
        txtBox.insert(tk.END,"\n【基本情報(CSV file)】\n"
                      f"\nファイル名:{path.name}\n"
                      f"\n絶対パス:{path.absolute()}\n"
                      f"\nサイズ:{stats.st_size}バイト({stats.st_size / 1024 : .2f}KB)\n"
                      "\n【タイムスタンプ】\n"
                      f"\n作成時刻:{dt.datetime.fromtimestamp(stats.st_ctime)}\n"
                      f"\n更新時刻:{dt.datetime.fromtimestamp(stats.st_mtime)}\n"
                      f"\nアクセス時刻:{dt.datetime.fromtimestamp(stats.st_atime)}\n")
        txtBox.see(tk.END)
    else:
        txtBox.insert(tk.END,f"エラー: '{found_path_data_save}' は現在のディレクトリに見つかりませんでした。")
        txtBox.see(tk.END)
    path = pathlib.Path(found_path_tflite)
    if path.exists():
        stats = path.stat()
        txtBox.insert(tk.END,"\n【基本情報(TensorFlowLite file)】\n"
                      f"\nファイル名:{path.name}\n"
                      f"\n絶対パス:{path.absolute()}\n"
                      f"\nサイズ:{stats.st_size}バイト({stats.st_size / 1024 : .2f}KB)\n"
                      "\n【タイムスタンプ】\n"
                      f"\n作成時刻:{dt.datetime.fromtimestamp(stats.st_ctime)}\n"
                      f"\n更新時刻:{dt.datetime.fromtimestamp(stats.st_mtime)}\n"
                      f"\nアクセス時刻:{dt.datetime.fromtimestamp(stats.st_atime)}\n")
        txtBox.see(tk.END)
    else:
        txtBox.insert(tk.END,f"エラー: '{found_path_tflite}' は現在のディレクトリに見つかりませんでした。")
        txtBox.see(tk.END)
    txtBox.configure(state = "disabled")

def how_to_display():
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    txtBox.insert(tk.END,'\n天気予報appへようこそ!!!\n'
                  '\nマルコフ連鎖を使って古典的な天気予報を行うことが出来ます。\n'
                  '\n下の操作ボタンをクリックして操作を始めてください。\n'
                  '\n使い方\n'
                  '\nメニューバーのファイルボタンから操作を始めてください。\n'
                  '\n記録：現在の天気を記録します。\n'
                  '\n確認：CSVファイルに保存されているデータを図や表を用いて確認することが出来ます。\n'
                  '\n予報：保存されているデータをもとに二次マルコフ連鎖を用いて明日の天気を予報します。\n'
                  '\n削除：記録された最新の天気情報を削除します。\n'
                  '\nリセット：現在保存されているデータをすべて削除します。\n'
                  '\nファイル検索：Python、CSVファイルの場所を特定します。\n'
                  '\n終了：アプリケーションを終了します。\n'
                  '\n開発者モード：開発者向けに行列計算の内部を確認することが出来ます。\n')
    txtBox.see(tk.END)
    txtBox.configure(state = "disabled")

def del_weather():
    df = file_read()
    txtBox.configure(state = "normal")
    txtBox.delete("1.0","end")
    try:
        del_today = df.index[-1]
        drop = df.drop(del_today)
        df = drop
        date_list = df['Date'].tolist()
        weather_list = df['Weather'].tolist()
        data = {'Date': date_list, 'Weather': weather_list}
        file_write(data)
        txtBox.insert(tk.END,"\n最新の天気を削除しました。\n")
        txtBox.see(tk.END)
    except:
        txtBox.insert(tk.END,"\n失敗しました。\n")
        txtBox.see(tk.END)
    txtBox.configure(state = "disabled")
        
def windouw():
    global root,root_progress,progressbar,txtBox,button_sun,button_rain,button_cloud,button_snow
    
    cpu_usage = psutil.cpu_percent(interval = 1)
    print(f"CPU使用率: {cpu_usage:5.1f}%", end="", flush=True)
    
    ck.set_appearance_mode("system")
    weather_config.FONT_FAMILY = weather_config.FONT_FAMILY
    root_progress = ck.CTk()
    root_progress.title("天気予報×AI")
    root_progress.geometry("300x70") 
    root_progress.state("normal")
    label = ck.CTkLabel(root_progress,text = "読み込み中...", text_color = ("black", "white"), font = ("Miryo", 16))
    label.pack()
    
    progressbar = ck.CTkProgressBar(root_progress,orientation="horizontal", fg_color=("white","black"), progress_color=(weather_config.FONT_COLOR), width = 240, height = 10, mode="determinate")
    progressbar.pack(padx = 30,pady = 10)
    progressbar.set(0)
    root_progress.update()
    research()
    root_progress.destroy()
    
    ck.set_appearance_mode("system")
    root = ck.CTk() 
    root.title("天気予報×AI") 
    root.geometry(weather_config.DISPLAY_SIZE) 
    root.after(10,lambda :root.state("zoomed"))
    root.grid_rowconfigure(0, weight=0) 
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)

    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff = 0)
    file_menu.add_command(label = 'ファイル検索', command = research_display)
    file_menu.add_separator()
    file_menu.add_command(label = 'リセット', command = reset)
    file_menu.add_separator()
    file_menu.add_command(label = '終了', command = end)
    if weather_config.DEBUG_MODE:
        file_menu.add_separator()
        file_menu.add_command(label = '開発者モード', command = weather_matrix_display)
    ope_menu = tk.Menu(menubar, tearoff= 0)
    ope_menu.add_command(label = '記録', command = weather_log)
    ope_menu.add_separator()
    ope_menu.add_command(label = "記録（画像認識：TensorFlowLite）", command = weather_log_image)
    ope_menu.add_separator()
    ope_menu.add_command(label = '確認', command = weather_log_check)
    ope_menu.add_separator()
    ope_menu.add_command(label = '予報', command = weather_tomorrow)
    ope_menu.add_separator()
    ope_menu.add_command(label = "削除", command = del_weather)
    setting_menu = tk.Menu(menubar, tearoff = 0)
    setting_menu.add_command(label = 'ライトモード', command = lambda : ck.set_appearance_mode("light"))
    setting_menu.add_command(label = 'ダークモード', command = lambda : ck.set_appearance_mode('dark'))
    setting_menu.add_command(label = 'システムに従う', command = lambda : ck.set_appearance_mode('system'))
    help_menu = tk.Menu(menubar, tearoff = 0)
    help_menu.add_command(label = '情報', command = info_display)
    help_menu.add_separator()
    help_menu.add_command(label = '使い方', command = how_to_display)
    menubar.add_cascade(label = 'ファイル(F)', menu = file_menu)
    menubar.add_cascade(label = "操作(O)", menu = ope_menu)
    menubar.add_cascade(label = '設定(S)', menu = setting_menu)
    menubar.add_cascade(label = 'ヘルプ(H)', menu = help_menu)
    root.config(menu = menubar)
    
    title_frame = ck.CTkFrame(root,width = 100, corner_radius = 0)
    title_frame.grid(row = 0, column = 0,sticky = 'new')
    title_frame.grid_columnconfigure(0, weight=0)
    title_frame.grid_rowconfigure(0, weight=0)
    label = ck.CTkLabel(title_frame, text="天気予報×AI", text_color=(weather_config.FONT_COLOR), font = (weather_config.FONT_FAMILY , weather_config.FONT_SIZE_TITLE, "bold")) 
    label.grid(row = 0, column = 0,padx=5, pady=5, sticky ="ew") 

    main_frame = ck.CTkFrame(root)
    main_frame.grid(row = 0, column = 1, rowspan = 2, sticky = "nsew")
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight= 1)
    txtBox = ck.CTkTextbox(main_frame,height=1600, width=1600, fg_color=("white", "black"), text_color=(weather_config.FONT_COLOR), font = (weather_config.FONT_FAMILY, weather_config.FONT_SIZE_MAIN))
    txtBox.configure(state="disabled")
    txtBox.grid(row=0, column=0, columnspan = 2, padx=5, pady=5, sticky="nsew")

    sidebar_frame = ck.CTkFrame(root,width = 100, corner_radius = 0 )
    sidebar_frame.grid_columnconfigure(0, weight=1)
    sidebar_frame.grid(row = 1, column = 0, rowspan = 2, sticky ="sew")

    button_sun = ck.CTkButton(sidebar_frame,text = '晴れ',width = 150, height =50, fg_color=(weather_config.FG_COLOR), text_color=(weather_config.FONT_COLOR), font = (weather_config.FONT_FAMILY,weather_config.FONT_SIZE_BTN ))
    button_cloud = ck.CTkButton(sidebar_frame,text = '曇り', width = 150, height = 50, fg_color=(weather_config.FG_COLOR), text_color=(weather_config.FONT_COLOR), font = (weather_config.FONT_FAMILY, weather_config.FONT_SIZE_BTN))
    button_rain = ck.CTkButton(sidebar_frame,text = '雨', width = 150, height = 50, fg_color=(weather_config.FG_COLOR), text_color=(weather_config.FONT_COLOR), font = (weather_config.FONT_FAMILY, weather_config.FONT_SIZE_BTN))
    button_snow = ck.CTkButton(sidebar_frame,text = '雪', width = 150, height = 50, fg_color=(weather_config.FG_COLOR), text_color=(weather_config.FONT_COLOR), font = (weather_config.FONT_FAMILY, weather_config.FONT_SIZE_BTN))

    button_sun.grid(row = 0, column = 0, padx = 20, pady = 20)
    button_cloud.grid(row = 1, column = 0, padx = 20, pady = 20)
    button_rain.grid(row = 2, column = 0, padx = 20, pady = 20)
    button_snow.grid(row = 3, column = 0, padx = 20, pady = 20)
    
    root.mainloop()   

windouw()

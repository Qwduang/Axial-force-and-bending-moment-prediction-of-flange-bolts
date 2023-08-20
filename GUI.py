
import pandas as pd
import PySimpleGUI as sg
import numpy as np
from PIL import Image
from pickle import load
import pickle
import warnings
from sklearn.exceptions import DataConversionWarning



with open('rf_model_BOLT.pkl', 'rb') as model_file:
    rf_model_bolt = pickle.load(model_file)
with open('rf_model_SM2.pkl', 'rb') as model_file:
    rf_model_SM2 = pickle.load(model_file)

# ADD TITLE COLOUR ,title_color='white'
# 设置主题为白色背景和红色文本框
#sg.theme_previewer()
#print(sg.theme_list())

sg.theme('LightGrey4')
sg.SetOptions(background_color='white', text_element_background_color='white')


# All the stuff inside your window.
layout = [
    [sg.Text('Developed by Hang Du, Yuxiao Luo, Kaoshan Dai, Fan Ke, Tang Xiao', font=('Helvetica', 10))],
    [sg.Text('SiChuan University (SCU), Chengdu, China')],
    [sg.Text('Email: duhang202206@163.com')],
    [sg.Frame(layout=[
        [sg.Column([
            [sg.Text('D_tube', size=(10, 1),justification='center'), sg.InputText(key='-f1-',size=(20, 1))],
            [sg.Text('t_tube', size=(10, 1),justification='center'), sg.InputText(key='-f2-',size=(20, 1))],
            [sg.Text('d_bolt', size=(10, 1), justification='center'), sg.InputText(key='-f3-',size=(20, 1))],
            [sg.Text('F_c', size=(10, 1),justification='center'), sg.InputText(key='-f4-',size=(20, 1))],
            [sg.Text('F_a', size=(10, 1),justification='center'), sg.InputText(key='-f5-',size=(20, 1))],
            [sg.Text('F_b', size=(10, 1), justification='center'), sg.InputText(key='-f6-',size=(20, 1))],
            [sg.Text('load', size=(10, 1),justification='center'), sg.InputText(key='-f7-',size=(20, 1))],
            [sg.Text('Pretension', size=(10, 1),justification='center'), sg.InputText(key='-f8-',size=(20, 1))],
            [sg.Text('n_bolt', size=(10, 1) ,justification='center',), sg.InputText(key='-f9-',size=(20, 1))]
        ], size=(200, 240), vertical_scroll_only=True, background_color='white',
            ), sg.Image(filename='image.png', size=(200, 120))],
    ], title='Input parameters', relief=sg.RELIEF_SUNKEN, border_width=1)],
    [sg.Frame(layout=[
        [sg.Text('BOLT Force', size=(10, 1)),sg.InputText(key='-OP1-', size=(45, 1))]], title='Output')],
    [sg.Frame(layout=[
        [sg.Text('BOLT Moment', size=(10, 1)),sg.InputText(key='-OP2-', size=(45, 1))]], title='Output')],
    [sg.Button('Predict'), sg.Button('Cancel')]
]

# Create the Window
window = sg.Window('Predict of bolt axial force and bending moment', layout)

#加载ONNX模型

# 禁用 DataConversionWarning 和 UserWarning 警告
warnings.filterwarnings(action='ignore', category=DataConversionWarning)
warnings.filterwarnings(action='ignore', category=UserWarning)





while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    # window['-OP-'].update('Please fill all the input parameters')
    if event == 'Predict':
        # window['-OP-'].update(values[0])
        # break
        if values['-f1-'] == '' or values['-f2-'] == '' or values['-f3-'] == '' or values['-f4-'] == '' or values[
            '-f5-'] == '' or values['-f6-'] == '' or values['-f7-'] == '' or values['-f8-'] == ''or values['-f9-'] == '':

            window['-OP1-'].update('Please fill all the input parameters')
            window['-OP2-'].update('Please fill all the input parameters')

        else:

            x_test = np.array([[float(values['-f1-']), float(values['-f2-']), float(values['-f3-']),
                                float(values['-f4-']), float(values['-f5-']), values['-f6-'], values['-f7-'],
                                values['-f8-'],values['-f9-']]])

            y_pred_BOLT = rf_model_bolt.predict(x_test)
            y_pred_SM2 = rf_model_SM2.predict(x_test)

            window['-OP1-'].update(np.round((y_pred_BOLT[0]), 4))
            window['-OP2-'].update(np.round((y_pred_SM2[0]), 4))
window.close()



# 进行预测操作
# ...

# 恢复警告设置
warnings.resetwarnings()
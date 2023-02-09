import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# 获取水库信息
def get_reservoir():
    ret = {} # 组装数据, 类型为字典

    url = 'https://water.taiwanstat.com'
    resp = requests.get(url)
    resp.encoding = 'utf-8' # 使用与网页相对应的编码格式, 避免乱码
    soup = BeautifulSoup(resp.text, 'html.parser') # 通过html dom解析器采集数据
    items = soup.select('.reservoir')

    col_1 = []
    col_2 = []
    for k, v in enumerate(items):
        name            = v.select_one('.name').get_text() # 水库名称
        number          = v.select_one('h5').get_text().replace('萬立方公尺', '') # 有效蓄水量
        col_1.append(name)
        col_2.append(float(number)) # 字符串转为浮点数, 图表数据用

    headers  = ['水库名称', '有效蓄水量(萬立方公尺)']
    ret[headers[0]] = col_1
    ret[headers[1]] = col_2
    return ret

# 展示长条图
def display_chart(data):
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # 解决中文显示
    plt.rcParams['axes.unicode_minus'] = False

    x = []
    for k, v in enumerate(data['水库名称']):
        x.append(k+1)
    h = data['有效蓄水量(萬立方公尺)']
    color = ['b'] # 全部用蓝色柱状表示
    label = data['水库名称']
    plt.barh(x, h, color=color, tick_label=label, height=0.5)  # 改成 barh
    plt.title('台灣水庫即時水情')
    plt.show()

def main():
    try:
        export_data = get_reservoir() # 获取当前水库蓄水量

        df = pd.DataFrame(export_data)
        filename = 'reservoir_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.csv' # 导出文件名
        df.to_csv(filename, index=False, header=True, encoding='utf-8-sig') # utf-8-sig 解决csv乱码
        # 展示长条图
        display_chart(export_data)

        print('导出csv成功')
    except:
        print('导出csv失败')

if __name__ == '__main__': # 主入口
    main()
# import openpyxl
# import os
#
# # 文件路径与工作簿
# path = r'C:\Users\SZLCSC\Downloads\向波-导出数据.xlsx'
# wb = openpyxl.load_workbook(path)
# ws = wb.active
#
# # 收集数据
# text_list = []
# for row in range(2, ws.max_row + 1):
#     sku = ws[f'C{row}'].value
#     name = ws[f'D{row}'].value
#     brands = ws[f'E{row}'].value
#     model = ws[f'F{row}'].value
#     cataloged = ws[f'G{row}'].value
#     parameter = ws[f'O{row}'].value
#     text = f'商品编码:{sku}@@@商品名称:{name}@@@品牌:{brands}@@@型号:{model}@@@目录:{cataloged}参数:{parameter}'
#     text_list.append(text)
#
# # 设置每个文件最多的条数
# max_num = 300
#
# # 确保目录存在
# output_dir = r'D:\测试文件'
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)
#
# # 写入文件
# file_index = 1
# for i in range(0, len(text_list), max_num):
#     with open(os.path.join(output_dir, f'{file_index}.txt'), 'w', encoding='utf-8') as file:
#         file.write('\n'.join(text_list[i:i + max_num]))
#     file_index += 1

import requests

url = "https://api.link-ai.chat/v1/chat/completions"
payload = {
    "app_code": "YHFKmsxe",
    "messages": [
        {
            "role": "user",
            "content": "有好用的记号笔推荐吗"
        }
    ]
}
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer Link_Q7A2gqMvQadVIlC55diQKNaPPcAdbnAb4brsRchxIe"
}
response = requests.request("POST", url, json=payload, headers=headers)
print(response.json()['choices'][0]['message']['content'])
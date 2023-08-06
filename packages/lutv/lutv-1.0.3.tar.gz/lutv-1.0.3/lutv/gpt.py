import os, requests
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + os.getenv('OPENAI_API_KEY', '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'),
}


def tructiep():
    while True:
        n = input('Nội dung: ')
        json_data = {'model': 'gpt-3.5-turbo','messages': [{'role': 'user','content': n,},],}
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data).json()
        print('____\n\n',response["choices"][0]['message']['content'],'\n\n____')
        if n =='':
            break
def chat(noidung):
    json_data = {'model': 'gpt-3.5-turbo','messages': [{'role': 'user','content': noidung,},],}
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data).json()
    print('____\n\n',response["choices"][0]['message']['content'],'\n\n____')
def save(text):
    json_data = {'model': 'gpt-3.5-turbo','messages': [{'role': 'user','content': text,},],}
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data).json()
    a=response["choices"][0]['message']['content']
    try:parts = a.split("```")[1].split('python')[1]
    except:parts = a.split("```")[1]
    with open("filename.py", "w", encoding='utf-8') as f:
        f.write(parts)
    print('Done')
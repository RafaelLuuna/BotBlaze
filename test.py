import json
from icecream import ic
import Scripts.BlazeFunctions.Lances as Lances

from keras.models import load_model

LancesBlaze = Lances.Get(20000, ReturnType='dict', Values=['roll','color'])

model = load_model('.\IA\Models\model_dense_input20_output2.keras')

final_list = []

LeituraMaxima = 20

for i, Lance in enumerate(LancesBlaze):
    print(f'\n# {i}')
    if i > LeituraMaxima:
        input_layer = []
        for seq in LancesBlaze[i-LeituraMaxima:i]:
            input_layer.append(Lances.Converter.Cor(seq['color'],input_type='string',output_type='int'))
        LanceNum = Lances.Converter.Cor(Lance['color'],input_type='string',output_type='int')
        predict = Lances.Converter.Cor(model.predict([input_layer]),input_type='IA',output_type='int')
        final_list.append({'CorSorteada':LanceNum, 'PrevisaoIA':predict, 'Sequence':input_layer})



json_object = json.dumps(final_list, indent=4)

with open('./Reports/Report_21.10.2023_10.55.json', 'w') as arquivo:

    arquivo.write(json_object)

with open('./Reports/Report_21.10.2023_10.55.json', 'r') as arquivo:

    new_json_object = json.loads(arquivo.read())



    
ic(len(new_json_object))
ic(new_json_object)

quit()


10
19
20
21
33
44
45
47
59
68
70
86
87
90
94

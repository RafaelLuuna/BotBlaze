import matplotlib.pyplot as plt
import BlazeFunctions.Lances as Lances

def PlotarGraficos(history, modelName):
    losses = history.history['loss']
    val_losses = history.history['val_loss']
    accuracies = history.history['accuracy']
    val_accuracies = history.history['val_accuracy']

    # Plotando as perdas
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(history.epoch, losses, label='Loss', color='blue', marker='o')
    plt.plot(history.epoch, val_losses, label='Val_Loss', color='green', marker='o')
    plt.title('Loss Over Time '+ modelName)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Plotando as métricas de precisão
    plt.subplot(1, 2, 2)
    plt.plot(history.epoch, accuracies, label='Accuracy', color='blue', marker='o')
    plt.plot(history.epoch, val_accuracies, label='Val_Accuracie', color='green', marker='o')
    plt.title('Accuracy Over Time '+ modelName)
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()

def SepararTreinamento(input, input_size, input_type='cor', val_percent=0.2, return_lst=['train_x','train_y']):
    split_val = int(len(input) * val_percent)
    if split_val < input_size:
        print("\n![AVISO]! A porcentagem de amostra para validação contém apenas 1 registro, por favor, defina o valor de 'val_percent' maior.\n")
        split_val = input_size +1
    input_val = input[:split_val]
    input = input[split_val:]

    train_x = [input[i:i + input_size] for i in range(0,len(input)-input_size+1)]
    val_x = [input_val[i:i + input_size] for i in range(0,len(input_val)-input_size+1)]


    train_y = []
    for i in train_x[1:]:
        train_y.append(Lances.ConverterCor(i[input_size-1],input_type='int',output_type='IA'))
        
    val_y = []
    for i in val_x[1:]:
        val_y.append(Lances.ConverterCor(i[input_size-1],input_type='int',output_type='IA'))



    train_x = train_x[:-1]
    val_x = val_x[:-1]

    output = []
    for item in return_lst:
        match item:
            case 'train_x':
                output.append(train_x)
            case 'val_x':
                output.append(val_x)
            case 'train_y':
                output.append(train_y)
            case 'val_y':
                output.append(val_y)


    return tuple(output)

def EncapsularSequencias(input):
    output = input
    for iLst, value in enumerate(input):
        output[iLst] = [[value[i]] for i in value]
    return output

def AgruparSequancias(input_x, input_y, group_size):
    if group_size <= 0:
        group_size = 1
    output_x = []
    output_y = []
    group = []
    index = 0
    i = 0
    while index < len(input_x)-group_size:
        group.append(input_x[index + i])
        i += 1
        if i == group_size:
            output_x.append(group)
            output_y.append(input_y[index+ i - 1])

            group = []
            i = 0
            index += 1
    return output_x, output_y


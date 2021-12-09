import os


def add_operators():
    with open('data\список операторов.txt', "r") as file:
        lines = file.read().split("\n")
        file.close()
    return lines


# функция загрузки списка объектов из файла, где ключ название файла-объекта, а значенияя это параметры проверки внутри
def add_objects():
    with open('data\список объектов.txt', 'r') as file:
        lines = file.read().split("\n")
        file.close()
    return lines


def read_objects():
    files = os.listdir()
    objects_txt = []
    for file in files:
        if file.endswith('.txt'):  # читаем только файлв с расширением txt  корне
            objects_txt.append(file)

    dict_of_params = dict()

    for file in objects_txt:
        with open(file, 'r') as f:
            word_list = f.read().split("\n")  # избавляемся от знака переноса
            word_list[:] = [item for item in word_list if item != '']  # удаляем пустые строки из списка
            dict_of_params[str(f.name)] = word_list  # добавляем в словарь, имя файла ключ - строки внутри  значения
    return dict_of_params

    '''
    wordLst = os.listdir('objects')

    dic = {}
    for word in wordLst:
        dic.update({word: []})
    path = r'objects'
    filelst = os.listdir(path)
    for file in filelst:
        if '.txt' not in file: continue
    f = open(path + '\\' + file, 'r')
    txt = f.readlines()
    for key in dic.keys():
        #if key in txt:
            dic[key].append(txt)
    return  dic


    


   # d = defaultdict(set)
   # for path, dirs, files in os.walk('objects'):
        #for f in fnmatch.filter(files, '*.txt'):
           # d[os.path.basename(path)].add(f)

   # return(dict(d))


    #filename = os.listdir(path) #возвращает список файлов в директории


      #    #my_dict = {}
    #return files

    #folder = 'objects'  # присваиваем  директорию на ту где лежат файлы объектов
    #for root, dirs, files in os.walk(folder):  # нас интересуют только файлы
        #for file in files:
            #file_name = os.path.join(path, file)
           # os.chdir("/objects")
            #with open(file) as f:
               # items = [i.strip() for i in f.read().split("\n")]
               # my_dict[file.replace(".txt", "")] = items
    #output_dict = {}
    #folder = 'objects'  # присваиваем  директорию на ту где лежат файлы объектов
    #for root, dirs, files in os.walk(folder):  # нас интересуют только файлы
        #for filename in files:
            # при сравнеии удаляем расширение и оставляем только имя файла
            #if os.path.splitext(os.path.basename(filename))[0]:
               # filename = 'objects' + '\\' + filename
                #output_dict[filename.split(',')[0]] = numpy.loadtxt(filename)
            #return output_dict
'''

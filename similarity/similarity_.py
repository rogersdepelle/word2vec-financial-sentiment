import json
import numpy
import word2vec

def similarity_words(model,word_a,word_b):
    try:
        contain_word_a = model.__contains__(word_a)
        contain_word_b = model.__contains__(word_b)
        #print(word_a)
        if(contain_word_a and contain_word_b):
            cosine_similarity = numpy.dot(model[word_a], model[word_b])/(numpy.linalg.norm(model[word_a])* numpy.linalg.norm(model[word_b]))
            return cosine_similarity
        else:
            return -1
    except Exception as e:
        #print("a")
        return -1

#return the average value of similarity of a word regard to group o words
def mean_similarity_word_words(model,word,words):
    total = 0
    contador = 0
    for word_base in words:
        similari = similarity_words(model,word,word_base)
        if(similari >-1):
            total +=similari
            contador +=1
    if(contador>0):
        return total/contador
    else:
        return -1

#return the maximum similarity of a word regard to group o words
def max_similarity_word_words(model,word,words):
    max_similarity = -1
    contador = 0
    for word_base in words:
        similari = similarity_words(model,word,word_base)
        if(contador==0):
            max_similarity=similari
        else:
            if(similari>max_similarity):
                max_similarity=similari
        contador+=1
    return max_similarity


def similarity_words_words_mean(model,list_words_a,list_words_b):
    count = 0
    total = 0
    for word_a in list_words_a:
        mean_simil = mean_similarity_word_words(model,word_a,list_words_b)
        if(mean_simil>-1):
            total+=mean_simil
            count+=1
    if(count>0):
        return total/count
    else:
        return 0

def similarity_words_words_max(model,list_words_a,list_words_b):
    count = 0
    total = 0
    for word_a in list_words_a:
        mean_simil = max_similarity_word_words(model,word_a,list_words_b)
        if(mean_simil>-1):
            total+=mean_simil
            count+=1
    if(count>0):
        return total/count
    else:
        return 0

def Load_model(path_bin):
    model = word2vec.load(path_bin)
    return model

def similarity_testsentences_ktearms(model,path_datatest_json,path_k_pos_neg):
    #load news teste
    json_file = open(path_datatest_json)
    json_str = json_file.read()
    news = json.loads(json_str)

    #load the sets of k terms
    json_file = open(path_k_pos_neg)
    json_str = json_file.read()
    k_terms = json.loads(json_str)

    #retrieve the positive and negative words from json file
    k_posi_words=[]
    k_nega_words=[]
    for label in k_terms:
        #print(label)
        if(label == "positive"):
            words_pmi_posi = k_terms[label]
            #print(words_pmi_posi)
            #retrieve words
            position = 0
            for item in words_pmi_posi:
                if((position%2)==0):# it is a word
                    k_posi_words.append(item)
                position+=1
        else: # negative
            words_pmi_nega = k_terms[label]
            #print(words_pmi_nega)
            #retrieve words
            position = 0
            for item in words_pmi_nega:
                if((position%2)==0):# it is a word
                    k_nega_words.append(item)
                position+=1
    #print(k_nega_words)
    #print(k_posi_words)

    #the format of the output_file
    arr_reviews_and_similaridade=[]

    #calulate the values for each sentece
    for key in news:
        reviews_and_similaridade = { "id":"", "values": {"label": "", "mean_max": {"positive": float,"negative": float},"mean_mean": {"positive": float,"negative": float}}}
        arr_words_new = news[key]["text"]
        label_new = news[key]["label"]
        #print(key)
        #calculate the similarity between the given

        #print(label_new)
        #print(key)
        #similarity between arr_words_new and k_nega_words
        mean_mean_simil_neg = similarity_words_words_mean(model,arr_words_new,k_nega_words)
        #print(mean_mean_simil_neg)
        mean_max_simil_neg = similarity_words_words_max(model,arr_words_new,k_nega_words)
        #print(mean_max_simil_neg)

        #similarity between arr_words_new and k_nega_words
        mean_mean_simil_pos = similarity_words_words_mean(model,arr_words_new,k_posi_words)
        #print(mean_mean_simil_pos)
        mean_max_simil_pos = similarity_words_words_max(model,arr_words_new,k_posi_words)
        #print(mean_max_simil_pos)

        reviews_and_similaridade["id"]=key
        reviews_and_similaridade["values"]["label"]=label_new
        reviews_and_similaridade["values"]["mean_max"]["positive"] = mean_max_simil_pos
        reviews_and_similaridade["values"]["mean_max"]["negative"] = mean_max_simil_neg
        reviews_and_similaridade["values"]["mean_mean"]["positive"] = mean_mean_simil_pos
        reviews_and_similaridade["values"]["mean_mean"]["negative"] = mean_mean_simil_neg
        arr_reviews_and_similaridade.append(reviews_and_similaridade)
    #write the result file
    reviews_and_similaridade_file = open("reviews_and_similaridade.json", "w")
    json.dump(arr_reviews_and_similaridade, reviews_and_similaridade_file)
    reviews_and_similaridade_file.close()


model = Load_model('/home/danny/Downloads/Word2vec_trunk/vectors.bin')
path_datatest_json='data_teste.json'
path_k_pos_neg='kterms.json'

similarity_testsentences_ktearms(model,path_datatest_json,path_k_pos_neg)



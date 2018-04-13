from unit.unit import *
from cmdb.models import *
import math

_STOP_WORDS = frozenset([
    'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
    'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although',
    'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another',
    'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as',
    'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been',
    'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
    'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can',
    'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
    'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
    'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even',
    'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',
    'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
    'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
    'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here',
    'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
    'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc',
    'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last',
    'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me',
    'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
    'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
    'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
    'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
    'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
    'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
    'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
    'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some',
    'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
    'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their',
    'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
    'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
    'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
    'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
    'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
    'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
    'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
    'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
    'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
    'yourselves', 'the', ''])

df = {}


def write_index(index, filePath):
    if not os.path.exists(filePath):
        #print ("File or directory " + filePath + " not exist, please change the name!")
        return
    fileObject = open(filePath, 'w')
    #json_str = json.dumps(index)
    fileObject.write(str(index))
    #json.dump(json_str, fileObject)
    #fileObject.write(json_str)
    fileObject.close()
    return


def read_index(filePath):
    if not os.path.exists(filePath):
        #print ("File or directory " + filePath + " not exist, please change the name!")
        return
    fileObject = open(filePath, 'r')
    dic = fileObject.read()
    #dic = ''
    #for line in fileObject:
        #dic = '%s%s' % (dic, line)
    #    dic = dic + line
    index = eval(dic)
    #index = json.loads(dic)
    fileObject.close()
    return index


def read_file(filePath):
    fileObject = open(filePath, 'r')
    text = fileObject.read().lower()
    fileObject.close()
    return text


def find_snippet(filePath, word, wordTimes):
    text = read_file(filePath)
    position = 0
    s = 0
    while s != wordTimes:
        position = text.find(word, position + 1)
        s += 1

    if position < 50:
        left = 0
        right = 100
    elif position > len(text) - 50:
        left = len(text) - 100
        right = len(text)
    else:
        left = position - 50
        right = position + 50
    '''
    while True:
        left = left - 1
        if (position - left > 50) or left == 0:
            break
    while True:
        right = right + 1
        if (right - position > 50) or right == len(text):
            break
    '''
    snippet = text[left:right]
    return snippet


def calculate_tf(Map):
    tf = {}
    for i in range(0, len(Map)):
        tf[Map[i][0]] = round(math.log(1 + float(Map[i][1])), 2)
    return tf


def calculate_df(N):
    for word in df:
        df[word] = round(math.log(N / float(df[word]), 10), 2)


def word_split(filePath):
    word_list = []
    time = {}
    position = {}

    words = tokenize(filePath)
    Map = computerWordFrequencies(words)
    tf = calculate_tf(Map)

    for word, frequency in Map:
        if word in _STOP_WORDS:
            continue
        if word.isdigit():
            continue
        if word in df:
            df[word] += 1
        else:
            df.setdefault(word, 1)

    filePathCut = filePath[filePath.find('/')+1:]

    for i, word in enumerate(words):
        if word in time:
            time[word] += 1
            #if time[word] % 2 == 0:
            #continue
        else:
            time.setdefault(word, 1)
        #    position.setdefault(c, 0)
        if word.isdigit():
            continue
        if len(word) > 20:
            if '/' not in word and '_' not in word:
                continue
        if word[-1] == 'e':
            if word[:-1].isdigit():
                continue
        #positionNow = text.find(c, position[c] + 1)
        #if positionNow - position[c] < 20:
        #    position[c] = positionNow
        #    continue
        #position[c] = positionNow
        #word_list.append((filePathCut, (position[c], c)))
        word_list.append((filePathCut, (i, word)))
    return word_list, tf


def word_clean(words):
    cleaned_words = []
    for filePathCut, (position, word) in words:
        if word in _STOP_WORDS:
            continue
        cleaned_words.append((filePathCut, (position, word)))
    return cleaned_words


def inverted_index(filePath):
    invertedSub = {}
    words, tf = word_split(filePath)
    words = word_clean(words)
    for index, (offset, word) in words:
        locations = invertedSub.setdefault(word, [tf[word]])
        locations.append(offset)
        #locations.append((index, offset))
        '''
        if word in invertedSub:
            continue
        if word in df:
            df[word] += 1
        else:
            df.setdefault(word, 1)
        '''
    return invertedSub


def inverted_index_combine(inverted, filePath):
    invertedSub = inverted_index(filePath)
    filePathCut = filePath[filePath.find('/') + 1:]
    for word, locations in invertedSub.iteritems():
        indices = inverted.setdefault(word, {})
        indices[filePathCut] = locations
    return inverted


def each_file(filePath):
    inverted = {}
    N = 0
    if not os.path.exists(filePath):
        #print ("File or directory " + filePath + " not exist, please change the name!")
        return
    if os.path.isdir(filePath):
        for dirPath, dirNames, fileNames in os.walk(filePath):
            for fileName in fileNames:
                if "bookkeeping" in fileName:
                    continue
                #if cmp(fileName, "20") > 0:
                #    continue
                child = os.path.join('%s/%s' % (dirPath, fileName))
                #print child
                N += 1
                inverted_index_combine(inverted, child)

    else:
        child = filePath

    calculate_df(N)

    for word in inverted:
        for fileName in inverted[word]:
            inverted[word][fileName][0] = round(inverted[word][fileName][0] * df[word], 2)

    createFile("index.txt")
    write_index(inverted, "index.txt")
    #index = read_index("index.txt")
    #print index
    #print inverted

    #print df
    #print N

'''
def pretreat_query(query):
    words = []
    re_word = re.compile(r"[\w']+")
    queryc = query.replace('\'', '')
    for word in re_word.finditer(query):
        words.append(word.group(0).lower())
    filePathCut = 'query'
    wordList = []
    for i, word in enumerate(words):
        if word.isdigit():
            continue
        if len(word) > 20:
            if '/' not in word and '_' not in word:
                continue
        if word[-1] == 'e':
            if word[:-1].isdigit():
                continue
        wordList.append((filePathCut, (i, word)))
    wordList = word_clean(wordList)
    return wordList


def search(inverted, query):
    results = {}
    words = [word for _, (offset, word) in pretreat_query(query) if word in inverted]
    for word in words:
        for fileName in inverted[word]:
            if fileName in results:
                results[fileName] = results[fileName] * inverted[word][fileName][0]
            else:
                results.setdefault(fileName, inverted[word][fileName][0])
    return sorted(results.items(), key=lambda x: x[1], reverse=True)
'''
#each_file("WEBPAGES_CLEAN")

def pretreat_query(query):
    words = []
    re_word = re.compile(r"[\w']+")
    queryc = query.replace('\'', '')
    for word in re_word.finditer(queryc):
        words.append(word.group(0).lower())
    return words

'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cos method begin
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
for inverted structure:

'''


def cal_tfidf(inverted, words):
    results = {}
    for word in words:
        for fileName in inverted[word]:
            if fileName != "IDF":
                if fileName in results:
                    results[fileName] = results[fileName] * inverted[word][fileName][0] * inverted[word]["IDF"]
                else:
                    results.setdefault(fileName, inverted[word][fileName][0] * inverted[word]["IDF"])
    return results


def search(inverted, query):
    results = {}
    #words = [word for _, (offset, word) in pretreat_query(query) if word in inverted]
    #words = [word for word in pretreat_query(query) if word in inverted]
    queryWord = pretreat_query(query)
    words = {}
    queryList = []
    for word in queryWord:
        if word in inverted:
            if word in words:
                words[word] += 1
            else:
                queryList.append(word)
                words.setdefault(word, 1)
    for word in words:
        words[word] = round(math.log(1 + float(words[word]), 10), 2)

    fileSet = []
    for word in words:
        for fileName in inverted[word]:
            if fileName != "IDF" and fileName not in fileSet:
                fileSet.append(fileName)

    proximity = cal_proximity(queryList, inverted, 1)
    '''
    results = cal_tfidf(inverted, words)
    print(proximity)
    print(results)
    for fileName in results:
        if fileName in proximity:
            results[fileName] = results[fileName] * (1 + 2 * proximity[fileName])
    '''
    for fileName in fileSet:
        upper = 0
        lower = 0
        # for each file, calculate root of square sum of TfIdf value
        rootSquare1 = calFileScore(inverted, fileName)
        for word in words:
            # for each word, calculate mix mul between word and file. Sum them based on word
            #upper += calMixScore(inverted, word, fileName)
            upper += calMixScore(inverted, word, fileName, words)
            # for each word, calculate root of square sum of TfIdf value. Sum them based on word
            #lower += calWordScore(inverted, word, fileName)
            lower += calWordScore(inverted, word, fileName, words)
        # formula
        res = upper / (math.sqrt(lower) * rootSquare1)
        if fileName in proximity:
            res = res * (proximity[fileName] * 2 + 1)
        else:
            res = res
        #res = upper
        # given query, for each file we calculate one score
        results[fileName] = res

    # return file info based on score
    return sorted(results.items(), key=lambda x: x[1], reverse=True), words


def calFileScore(inverted, fileName):
    square = 0
    '''
    for word in inverted.keys():
        if fileName in inverted[word]:
            temp = inverted[word][fileName][0] * inverted[word]["IDF"]
            #temp = temp * temp
            square += temp * temp
    '''
    filePath = '%s%s' % ('unit/WEBPAGES_CLEAN/', fileName)
    token = tokenize(filePath)
    Map = computerWordFrequencies(token)
    for word, fre in Map:
        if word in inverted:
            if fileName in inverted[word]:
                temp = inverted[word][fileName][0] * inverted[word]["IDF"]
                #temp = temp * temp
                square += temp * temp

    return math.sqrt(square)


def calMixScore(inverted, word, fileName, words):
    res = 0
    if fileName in inverted[word]:
        res = inverted[word][fileName][0] * inverted[word]["IDF"]
        #res = res * inverted[word]["IDF"] * getTfOfQuery(word)
        res = res * inverted[word]["IDF"] * words[word]
    return res


def calWordScore(inverted, word, fileName, words):
    res = 0
    if fileName in inverted[word]:
        #res = inverted[word]["IDF"] * getTfOfQuery(word)
        res = inverted[word]["IDF"] * words[word]
        res = res * res
    return res

#def getTfOfQuery(word):
    # calculate Tf of query

def cal_proximity(queryList, inverted, distance):
    res = {}
    for i in range(0, len(queryList) - 1):
        map1 = inverted[queryList[i]]
        map2 = inverted[queryList[i + 1]]
        for fileName in map1:
            if fileName in map2:
                if fileName != "IDF":
                    list1 = map1[fileName]
                    list2 = map2[fileName]
                    if len(list2) == 1:
                        res[fileName] = 0
                    else:
                        count = 0
                        j1 = 1
                        j2 = 1
                        while j1 < len(list1) and j2 < len(list2):
                            if list2[j2] < list1[j1]:
                                j2 += 1
                            else:
                                if list2[j2] - list1[j1] > distance:
                                    j1 += 1
                                else:
                                    count += 1
                                    j1 += 1
                                    j2 += 1
                        if fileName not in res:
                            res[fileName] = 0
                        res[fileName] += float(count) / min(len(list1), len(list2))

    return res




'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cos method end
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''


def output(query, index):
    #index = read_index('unit/index.txt')
    #s = time.time()
    #query = 'machine learning'
    result_final = []
    #words = [word for _, (offset, word) in pretreat_query(query) if word in index]
    result, words = search(index, query)
    print(len(result))
    fileName_url = read_index('unit/WEBPAGES_CLEAN/bookkeeping.json')
    count = 0
    for fileName, score in result:
        if count == 5:
            break
        filePath = '%s%s' % ('unit/WEBPAGES_CLEAN/', fileName)
        token = tokenize(filePath)
        max = 0
        wordTimes = -1
        '''
        for word in words:
            #max = 0
            #wordTimes = -1
            if fileName in index[word]:
                for i in range(1, len(index[word][fileName])):
                    times = 0
                    if int(index[word][fileName][i]) - 10 < 0:
                        left = 0
                        right = 20
                    elif int(index[word][fileName][i]) + 10 > len(token):
                        left = len(token) - 20
                        right = len(token)
                    else:
                        left = int(index[word][fileName][i]) - 10
                        right = int(index[word][fileName][i]) + 10
                    for j in range(left, right):
                        if token[j] in words:
                            times += 1
                    if times > max:
                        #snippet = token[left:right]
                        max = times
                        wordTimes = i
        snippet = find_snippet(filePath, word, wordTimes)
        #snippet = token[left:right]
        #print (fileName, score, fileName_url[fileName])
        #print (snippet)
        '''
        wr = searchResult()
        wr.fileName = fileName
        wr.webLink = fileName_url[fileName]
        #wr.snippet = snippet
        result_final.append(wr)
        #result_final.setdefault(fileName, [])
        #result_final[fileName].append(fileName_url[fileName])
        #result_final[fileName].append(snippet)
        count += 1
    #e = time.time()
    #print e-s
    return result_final

from cgitb import text
import MeCab
import urllib.request
import collections

def parsewithelimination(sentense):

  slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
  slothlib_file = urllib.request.urlopen(slothlib_path)
  stopwords=[]
  result_list = []
  for line in slothlib_file:
    ss=line.decode("utf-8").strip()
    if not ss==u'':
      stopwords.append(ss)

  elim=['数','非自立','接尾']
  part=['名詞']

  m=MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
  m.parse('')
  node=m.parseToNode(sentense)
    
  result=''
  while node:
    if node.feature.split(',')[6] == '*': # 原形を取り出す
      term=node.surface
    else :
      term=node.feature.split(',')[6]
        
    if term in stopwords:
      node=node.next
      continue
    
    if node.feature.split(',')[1] in elim:
      node=node.next
      continue

    if node.feature.split(',')[0] in part:
      if result == '':
        result = term
      else:
        result=result.strip() + ' '+ term
      result_list.append(list([node.surface,node.feature.split(',')[1]]))
        
    node=node.next

  return result


def main(text):
    result = parsewithelimination(text)
    l = result.split()
    c = collections.Counter(l)
    values, counts = zip(*c.most_common()[0:5])
    return list(values)
  
def run(class_name, class_overview):
  text_1 = main(class_name)
  text_2 = main(class_overview)
  keyword_list = text_1 +text_2
  keyword_num = list(dict.fromkeys(keyword_list))
  return keyword_num
  

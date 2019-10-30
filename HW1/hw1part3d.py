
import gensim
from gensim.models.word2vec import Word2Vec
# Load the binary model
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary = True);


from nltk.corpus import brown

#model = gensim.models.Word2Vec(brown.sents())
word1="rebellion"
word2="slave"

similarities1= model.most_similar(positive=[word1], topn = 10)

similarities2= model.most_similar(positive=[word2], topn = 10)

similaritieswords1=[]
for p in similarities1:
    similaritieswords1.append(p[0])

similaritieswords2=[]
for p in similarities2:
    similaritieswords2.append(p[0])

cosinesimilaritie1=""
for p in similaritieswords1:
    a=model.similarity(word1,p)
    cosinesimilaritie1=cosinesimilaritie1+"\n"+ word1 + " - "+ p+ ": "+ str(a)

cosinesimilaritie2=""
for p in similaritieswords2:
    a=model.similarity(word2,p)
    cosinesimilaritie2=cosinesimilaritie2+"\n"+ word2 + " - "+ p+ ": "+ str(a)

print("Top ten Similar words: \n")
print(word1 + " = " + str(similaritieswords1))
print(word2 + " = " + str(similaritieswords2))
print("Cosine Similarities: \n")
print(cosinesimilaritie1)
print(cosinesimilaritie2)

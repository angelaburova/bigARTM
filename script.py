from matplotlib import pyplot as plt
import artm

batch_vectorizer = artm.BatchVectorizer(data_path="out.txt", data_format="vowpal_wabbit", target_folder="out_batches", batch_size=2000)
batch_vectorizer = artm.BatchVectorizer(data_path="out_batches", data_format='batches')
my_dictionary=artm.Dictionary()
my_dictionary.gather(data_path=batch_vectorizer.data_path);

T = 12
model_artm = artm.ARTM(num_topics=T, topic_names=["sbj"+str(i) for i in range(T)], class_ids={"autors":0.3, "title":0.5, "text":0.1 })
model_artm.scores.add(artm.PerplexityScore(name='PerplexityScore', dictionary=my_dictionary))
model_artm.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore',class_id ='text'))
#model_artm.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore',class_id ='autors'))
#model_artm.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore',class_id ='title'))
model_artm.scores.add(artm.SparsityThetaScore(name='SparsityThetaScore'))
model_artm.scores.add(artm.TopTokensScore(name="top_words", num_tokens=15, class_id='text'))
model_artm.initialize(dictionary=my_dictionary)#seed=-1 - error
model_artm.num_document_passes=5
model_artm.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=15)
plt.plot(model_artm.score_tracker["PerplexityScore"].value)
for topic_name in model_artm.topic_names:
    print topic_name + ': ',
    for word in model_artm.score_tracker["top_words"].last_tokens[topic_name]:
        print word,
    print
#theta_test=model_artm.transform(batch_vectorizer=batch_vectorizer)
phi = model_artm.get_phi()
#print phi
model_artm.cache_theta=True
theta_test = model_artm.transform(batch_vectorizer=batch_vectorizer)
theta = model_artm.get_theta()
#print theta

print model_artm.score_tracker["SparsityPhiScore"].last_value
print model_artm.score_tracker["SparsityThetaScore"].last_value
model_artm.regularizers.add(artm.SmoothSparsePhiRegularizer(name='SparsePhi', tau=-100, dictionary=my_dictionary))
model_artm.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=15)
model_artm.regularizers['SparsePhi'].tau = -3*1e4
model_artm.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=15)
#for topic_name in model_artm.topic_names:
 #   print topic_name + ': ',
  #  for word in model_artm.score_tracker["top_words"].last_tokens[topic_name]:
   #     print word,
    #print
for topic_name in model_artm.topic_names:
    print topic_name + ': ',
    for word in model_artm.score_tracker["top_words"].last_tokens[topic_name]:
        print word,
    print
print model_artm.score_tracker["SparsityPhiScore"].last_value
print model_artm.score_tracker["SparsityThetaScore"].last_value
model_artm.save("my_model")
model_artm.load("my_model")

theta_test = model_artm.transform(batch_vectorizer)
theta = model_artm.get_theta()
#print theta


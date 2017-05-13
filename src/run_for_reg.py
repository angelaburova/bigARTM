import artm

T = 12
batch_vectorizer = artm.BatchVectorizer(data_path="out_batches", data_format='batches')
model_artm = artm.ARTM(num_topics=T, topic_names=["sbj"+str(i) for i in range(T)], class_ids={"autors": 3, "title": 5, "text": 1 })
model_artm.load("my_model")
model_artm.cache_theta = True
model_artm.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore',class_id ='text'))
model_artm.scores.add(artm.SparsityThetaScore(name='SparsityThetaScore'))
model_artm.scores.add(artm.TopTokensScore(name="top_words", num_tokens=15, class_id='text'))
my_dictionary = artm.Dictionary()
my_dictionary.gather(data_path=batch_vectorizer.data_path);

model_artm.regularizers.add(artm.SmoothSparsePhiRegularizer(name='SparsePhi', tau=-100, dictionary=my_dictionary))
model_artm.regularizers['SparsePhi'].tau = -4*1e4
model_artm.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=15)

for topic_name in model_artm.topic_names:
    print topic_name + ': ',
    for word in model_artm.score_tracker["top_words"].last_tokens[topic_name]:
        print word,
    print
print model_artm.score_tracker["SparsityPhiScore"].last_value
print model_artm.score_tracker["SparsityThetaScore"].last_value

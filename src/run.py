import artm
import os

T = 10
dict_file_name = os.getcwd() + "/../parsing/utils/new_dict.txt"
stop_file_name = os.getcwd() +"/../parsing/utils/stop5k.txt"

model_artm = artm.ARTM(num_topics=T, topic_names=["sbj"+str(i) for i in range(T)], class_ids={"autors":3, "title":5, "text":1 })
model_artm.prepare_data(path_out="out.txt", path_dict=dict_file_name, path_stop=stop_file_name) # prepare_data from the library. It can be used only one time.

batch_vectorizer = artm.BatchVectorizer(data_path="C:\\Users\\Angela\\Desktop\\ML\\bigARTM-master\\bigARTM-master\\results\\old_files\\out_with_lemm_from_server.txt", data_format="vowpal_wabbit", target_folder="out_batches", batch_size=2000)
batch_vectorizer = artm.BatchVectorizer(data_path="out_batches", data_format='batches')
my_dictionary=artm.Dictionary()
my_dictionary.gather(data_path=batch_vectorizer.data_path);

model_artm.cache_theta=True
model_artm.scores.add(artm.PerplexityScore(name='PerplexityScore', dictionary=my_dictionary))
model_artm.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore',class_id ='text'))
model_artm.scores.add(artm.SparsityThetaScore(name='SparsityThetaScore'))
model_artm.scores.add(artm.TopTokensScore(name="top_words", num_tokens=15, class_id='text'))
model_artm.initialize(dictionary=my_dictionary)
model_artm.num_document_passes=5
model_artm.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=15)
#model_artm.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=15, dictionary=my_dictionary)
model_artm.save("my_super_model")

for topic_name in model_artm.topic_names:
    print topic_name + ': ',
    for word in model_artm.score_tracker["top_words"].last_tokens[topic_name]:
        print word,
    print

print model_artm.score_tracker["SparsityPhiScore"].last_value
print

model_artm.post_regularization() # out post regulariztion. It can be commented

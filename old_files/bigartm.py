from matplotlib import pyplot as plt
import artm

batch_vectorizer=artm.BatchVectorizer(data_path="var.txt",data_format="vompal_wabbit",target_folder="var_batches",batch_size=100)

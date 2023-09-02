import numpy as np

class NaiveBayes(object):
	def __init__(self,num_class,feature_dim,num_value):
		"""Initialize a naive bayes model. 

		This function will initialize prior and likelihood, where 
		prior is P(class) with a dimension of (# of class,)
			that estimates the empirical frequencies of different classes in the training set.
		likelihood is P(F_i = f | class) with a dimension of 
			(# of features/pixels per image, # of possible values per pixel, # of class),
			that computes the probability of every pixel location i being value f for every class label.  

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example 
		    num_value(int): number of possible values for each pixel 
		"""

		self.num_value = num_value
		self.num_class = num_class
		self.feature_dim = feature_dim

		self.prior = np.zeros((num_class))
		self.likelihood = np.zeros((feature_dim,num_value,num_class))

	def train(self,train_set,train_label):
		""" Train naive bayes model (self.prior and self.likelihood) with training dataset. 
			self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
			self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of 
				(# of features/pixels per image, # of possible values per pixel, # of class).
			You should apply Laplace smoothing to compute the likelihood. 

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		
		# YOUR CODE HERE
		# # of occurance of num 0-9
		class_occurance = np.zeros((self.num_class))
		# # of occurance that at pixel i, have RGB value f, belongs to num 0-9
		evidence_occurance = np.zeros((self.feature_dim,self.num_value,self.num_class))
		for label_num in range(len(train_label)):
			label_val = train_label[label_num]
			class_occurance[label_val] += 1
			process = float(label_num/len(train_label)*100)
			print('Training......%f'%process,'%')
			for pix_num in range(len(train_set[label_num])):
				pix_val = int(train_set[label_num][pix_num])
				
				evidence_occurance[pix_num,pix_val,label_val] +=1 

		# laplace smooth
		k = 1
		for num in range(self.num_class):
			self.likelihood[:,:,num] = (evidence_occurance[:,:,num] + k)/(class_occurance[num] + k*self.num_value)

		# log and calculate prior
		self.likelihood = np.log(self.likelihood)
		self.prior = np.log(class_occurance / len(train_label))
		print("Training finished")
		

		pass

	def test(self,test_set,test_label):
		""" Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
			by performing maximum a posteriori (MAP) classification.  
			The accuracy is computed as the average of correctness 
			by comparing between predicted label and true label. 

		Args:
		    test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
		    test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value  
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""    

		# YOUR CODE HERE
		accuracy = 0
		pred_label = np.zeros((len(test_set)))

		# get the MAP result
		for i in range(len((test_label))):
			process = float(i/len(test_label)*100)
			print('Testing......%f'%process,'%')
			MAP_table = np.zeros(self.num_class)
			for j in range(self.num_class):
				MAP_table[j] = self.prior[j]
				for k in range(len(test_set[i])):
					MAP_table[j] += self.likelihood[k,int(test_set[i][k]),j]

			pred_label[i] = np.argmax(MAP_table)

		# calculate tthe accuracy
		acc_count = 0
		for i in range(len((test_label))):
			if pred_label[i] == test_label[i]:
				acc_count += 1

		accuracy = acc_count/len(test_label)
		print('Test finished')
		print('Accuracy is:',accuracy)

		
		

		return accuracy, pred_label


	def save_model(self, prior, likelihood):
		""" Save the trained model parameters 
		"""    

		np.save(prior, self.prior)
		np.save(likelihood, self.likelihood)

	def load_model(self, prior, likelihood):
		""" Load the trained model parameters 
		""" 

		self.prior = np.load(prior)
		self.likelihood = np.load(likelihood)

	def intensity_feature_likelihoods(self, likelihood):
			"""
			Get the feature likelihoods for high intensity pixels for each of the classes,
				by sum the probabilities of the top 128 intensities at each pixel location,
				sum k<-128:255 P(F_i = k | c).
				This helps generate visualization of trained likelihood images. 
			
			Args:
				likelihood(numpy.ndarray): likelihood (in log) with a dimension of
					(# of features/pixels per image, # of possible values per pixel, # of class)
			Returns:
				feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
					(# of features/pixels per image, # of class)
			"""
			# YOUR CODE HERE
			
			
			feature_likelihoods = np.zeros((likelihood.shape[0],likelihood.shape[2]))
			for i in range(len(likelihood)):
				for j in range(128,256,1):
					for k in range(len(likelihood[i,j])):
						feature_likelihoods[i,k] += np.exp(likelihood[i,j,k])

			return feature_likelihoods

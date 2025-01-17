class neuralNetwork:
	def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
		#input nodes
		self.inodes = inputnodes

		#output nodes
		self.onodes = outputnodes

		#hidden nodes
		self.hnodes = hiddennodes

		#learning rate
		self.lr = learningrate

		#weights (matrices) input -> hidden and hidden -> output
		self.wih = (numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes)))
		self.who = (numpy.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes)))

		# activation function
		self.activation_function = lambda x: scipy.special.expit(x)

		pass

	def train(self, inputs_list, targets_list):

		inputs = numpy.array(inputs_list, dnmin=2).T
		targets = numpy.array(targets_list, ndmin=2).T

		hidden_inputs = numpy.dot(self.wih, inputs)
		hidden_outputs = self.activation_function(hidden_inputs)

		final_inputs = numpy.dot(self.who, hidden_outputs)

		final_outputs = self.activation_function(final_inputs)

		# output layer error is the (target-output)
		output_errors = targets - final_outputs

		# hidden layer error is the output_errors, split by weights, recombined at hidden nodes
		hidden_errors = numpy.dot(self.who.T, output_errors)

		# update the weights for the links between the hidden and output layers
		self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)), numpy.transpose(hidden_outputs))

		# update the weights for the links between the input and hidden layers
		self.wih += self.self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), numpy.transpose(inputs))
		pass

	def query(self, inputs_list):
		# convert list into matrix
		inputs = numpy.array(inputs_list, ndmin=2).T

		# dot product of integers and input->hidden weights to give hidden inputs
		hidden_inputs = numpy.dot(self.wih, inputs)

		# calculate the hidden layer output
		hidden_outputs = self.activation_function(hidden_inputs)

		# calculate final layer inputs
		final_inputs = numpy.dot(self.who, hidden_outputs)

		# calculate final output of the neural network
		final_outputs = self.activation_function(final_inputs)

		return final_outputs
		pass
	
# load the mnist training data CSV file into a list
training_data_file = open("mnist_dataset/mnist_train.csv", 'r')
training_data_list = training_data_file.readlines()
training_data_file.close()

# train the neural network

# epochs is the number of times the training data set is used for training
epochs = 5

for e in range(epochs):
    # go through all records in the training data set
    for record in training_data_list:
        # split the record by the ',' commas
        all_values = record.split(',')
        # scale and shift the inputs
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        # create the target output values (all 0.01, except the desired label which is 0.99)
        targets = numpy.zeros(output_nodes) + 0.01
        # all_values[0] is the target label for this record
        targets[int(all_values[0])] = 0.99
        n.train(inputs, targets)
        pass
    pass

# load the mnist test data CSV file into a list
test_data_file = open("mnist_dataset/mnist_test.csv", 'r')
test_data_list = test_data_file.readlines()
test_data_file.close()

# test the neural network

# scorecard for how well the network performs, initially empty
scorecard = []

# go through all the records in the test data set
for record in test_data_list:
    # split the record by the ',' commas
    all_values = record.split(',')
    # correct answer is first value
    correct_label = int(all_values[0])
    # scale and shift the inputs
    inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
    # query the network
    outputs = n.query(inputs)
    # the index of the highest value corresponds to the label
    label = numpy.argmax(outputs)
    # append correct or incorrect to list
    if (label == correct_label):
        # network's answer matches correct answer, add 1 to scorecard
        scorecard.append(1)
    else:
        # network's answer doesn't match correct answer, add 0 to scorecard
        scorecard.append(0)
        pass
    
    pass


# calculate the performance score, the fraction of correct answers
scorecard_array = numpy.asarray(scorecard)
print ("performance = ", scorecard_array.sum() / scorecard_array.size)
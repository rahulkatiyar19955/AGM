# Guidlines to use Learning Code 

The Learning library was written as part of project for GSoC'17.

Following steps are involved in the learning process:
* Parsing of Data
* Training of Data
* Testing of Data

**Parsing of Data**:
Files involved:
* *AGMParser.py*: This file is used to parse planning files to get learning variables.
```
p = Parser()
p.parse_domain(domainFile)
# To parse domain. Parameters: domain file (.aggl)
p.parse_initM(initFile)
# To parse initial world model. Parameters: initModel file (.xml)
p.parse_target(targetFile)
# To parse Target files. Parameters: target file (.aggt)
p.parse_plan(planFile)
# To parse plan file for training purposes. Parameters: plan file (.plan)
```

**Training of Data**
Files involved:
* *classifier.py*: This files is used for both training and predicting data.
```
c = Classifier()
c.train(attr_list, tgt_actions)
# Trains data. Parameters: list of attributes, list of target actions
c.store()
# Stores probability values etc. in store.data
c.prefetch()
# Loads stored data by store(). Standard file name store.data.
c.make_square()
# Makes all data types API compatible (dimension)
```

* *train.py*: It's a wrapper function which uses *Parser()* and *Classifier()*. To run:
```
>> python train.py
```
It'll store all trained data in `store.data`. For manipulating directories to train change the following variable
```
# For training directories between start_value to end_value, do following:
start_dir = start_value
end_dir = end_value
# For training selective libraries:
dirs = dir_list
# where dir_list is list of directories
```

**Note:** While developing the learning library, we used numeric values for directories (length 5, for any alternative length, set `enum(other_length, i))`. Every directory will have .xml extension file added to it (initial World Model File). It'll search for .aggt file automatically but for plannning files, append to .aggt .aggt.plan for corresponding plan file.


**Testing of Data**

* *classifier.py* As described earlier, this is also used to predict data.
```
c = Classifier()
c.predict(attr_list, tgt_actions)
# Predicts data. Parameters: list of attributes, returns probability distribution over target variables
```
* *test.py*: This is a redundant file, use API Files instead.
* *generate.py*: This is a redundant file, use API File instead.
* *naiveBayesClassifier.py*: This is an API file, use this to predict data.
```
# Three ways to call constructor
nbc = NaiveBayesClassifier(attr_freq, target_freq)
nbc1 = NaiveBayesClassifier(attr_freq, target_freq, laplace_constant)
nbc2 = NaiveBayesClassifier([], [], laplace_constant, fileName)
'''
attr_freq: A 2D dictionary which if indexed using a target and an attribute, should return number of times an attribute was observed given a target during training.
target_freq: A 1D dictionary which if indexed using a target returns number of time the target was observed while training.
laplace_constant: Default value is one. This represents Laplace Constant.
fileName: File Data should be pickled. Unpickling should return a tuple (attr_freq, target_freq). This option is for passing data via a file (for avoiding repetition).
'''
```
***
Lashit Jain

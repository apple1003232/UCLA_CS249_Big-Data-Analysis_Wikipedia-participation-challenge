CS 249 Project
Wikipedia Participation Challenge

Team: ATAD


==========================================================================
SOFTWARE TOOLS

All tools used in the program are included in Python 2.7.10, as following:

(1) Python 2.7.10

(2) scikit-learn

===========================================================================
DATASETS

All datasets used in the program can be downloaded from the following link:

https://www.kaggle.com/c/wikichallenge/data

(1) training.tsv (from wikichallenge_data_all)
The official dataset for validation and prediction.

(2) validation.tsv and validation_solutions.tsv (from "wikichallenge_data_optional_validation")
The main dataset for training and testing, including model selection and parameter adjustment.

===========================================================================
SOURCE CODE FILES

(1) validation_preparation.py
Given the raw dataset file validation.tsv, it produces a new validation dataset for where user_id, article_id, namespace, timestamp, reverted are filtered. All users in the new validation dataset are active, which means they edited at least once between 2007-08-01 and 2007-12-31. The new validation dataset is created for future work instead of the raw validation.tsv.

(2) Feature Extraction.py
The program extracts 26 useful features(X) and 1 solution(y) for each user in the new validation dataset, and stores them in separate files. Given the new validation dataset, it produces 3 output files for training and testing. One output file includes 26 features(X) for editing behavior between 2001-01-01 and 2007-08-01, and one output file contains the solution(y), which is the edits value between 2007-08-01 to 2008-01-01. These two files are for training. The third output file contains 26 features(X) from the whole time span, which is between 2001-01-01 and 2008-01-01. The third file is for testing. These 3 files and validation_solutions.tsv can be separated in two training datasets and validation datasets.

(3) Feature Extraction_training.py
Similar to Feature Extraction.py, the program extracts 26 useful features(X) and 1 solution(y) for each user in the new validation dataset, and stores them in 4 separate files. One includes 26 features(X) for editing behavior between 2001-01-01 and 2009-11-01, and one output file contains the solution(y), which is the edits value between 2009-11-01 to 2010-04-01. These two files are for training. The third output file contains 26 features(X) between 2001-01-01 to 2010-04-01, and the forth one includes the solution(y) between 2010-04-01 to 2010-09-01. The two files are for validation and prediction. 

(4) models_prediction.py
The program includes several models from scikit-learn and provides the function for training and estimation. Given 2 training datasets and 1 extra dataset for testing, it produces one estimation solutions file. For details, please refer to our report and source codes.

(5) RMSLE.py
Given the estimation solutions file and one accurate solutions file(either validation_solutions.tsv or one dataset we counted ourselves), it computes the root mean square least error(RMSLE), which is used to evaluate the estimation.


==================================================================================
REPRODUCING THE RESULTS

(1) Training and validation
(Using validation.tsv:)
$ ./validation_preparation.py
$ ./Feature Extraction.py
$ ./models_prediction.py
$ ./RMSLE.py

(Using training.tsv:)
$ ./Feature Extraction_training.py
$ ./models_prediction.py
$ ./RMSLE.py

(2) Prediction
$ ./Feature Extraction_training.py
$ ./models_prediction.py

===================================================================================
For more details, please refer to CS249 Project report: "Wikipedia Participation Challenge" by team ATAD.

Thank you.

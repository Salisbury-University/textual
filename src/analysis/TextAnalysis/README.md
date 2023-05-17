# SentimentAnalysisVADER.py: 
Description: Sentiment Analysis using VADER (LEXICON APPROACH)

### What this program does:
  * Reads YouTube comments from a json file
  * Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) to evaluate the sentiment of YouTube Comments
  * Uses bounds to classify the sentiment of each comment
  
### What this will demonstrate:
  * What sentiment analysis is.
  * How to do sentiment analysis using a lexicon based approach
  * Pros and Cons of a lexicon based sentiment analysis approach

# SentimentAnalysisMLTOOL(NoteBookVersion).py:
Description: Sentiment Analysis using VADER and Multinomial Logistic Regression (MACHINE LEARNING APPROACH)

### What this program does:
* Read comments from the json file downloaded from our database.
* The preprocess function is called to apply the preprocessing steps on the input dataset. This includes detecting the language of comments, evaluating the sentiment using VADER  removing stopwords, converting letters to lowercase, and lemmatization.
* The distribution of sentiment evaluated by VADER is plotted using a bar chart.
* The dataset is split into a training set and a testing set.
* The comments in the training set are vectorized using CountVectorizer.
* A logistic regression model is trained on the training set.
* The accuracy score of the model is computed on both the training and test datasets.
* Predictions are made on the test dataset, and a confusion matrix is plotted to visualize the results.
* Classification report and F1 score are printed to evaluate the model's performance.
* at the end, the code enters a loop where the user can enter their own YouTube comments to manually test their model, and the model predicts their sentiment (positive, neutral, negative).

### What this will teach:
  * How to do sentiment analysis on an unlabeled dataset.
  * How to use VADER to create labels for an unlabeled textual dataset.
  * A general pipeline of sentiment analysis using machine learning, from data preprocessing to model training and evaluation steps. (Multinomial Logistic Regression).
  * Pros and cons of using a machine learning approach in this manner.


# SentimentAnalysisMLTOOL(Parallelized).py:
Description: Sentiment Analysis using VADER and Multinomial Logistic Regression (MACHINE LEARNING APPROACH)

### What this program does:
* This is the same program as the notebook version except the preprocessing steps and the training steps have been parallelized using python's multiprocessing module. May be faster for debugging.

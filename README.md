# LingPeer

LingPeer is a web app that suggests potential reviewers for abstracts in theoretical linguistics based on data from Lingbuzz. You can access it by visiting the following URL:

[LingPeer](https://lingpeer.streamlit.app/)

## Data Source

LingPeer works on data from [Lingbuzz.net](https://ling.auf.net/). It was collected using the [lingbuzz_scraper](https://github.com/cmunozperez/lingbuzz_scraper) tool.

## Usage

LingPeer was designed to be used as a web application. You just need to provide the title of a manuscript, its keywords and abstract to get a list of potential reviewers. It is possible to get recommendations based on partial data (e.g., title and keywords only), but this provides less accurate results.

It is also possible to run LingPeer as a script. First, you need to clone this repository to your local machine.

```
git clone https://github.com/cmunozperez/LingPeer.git
```

You run the script by executing the `main.py` file in the project directory.

```
python main.py
```

Alternatively, you can import the `main.py` module and use the function `get_peers`. It takes three string arguments as shown below.

```
title = 'This is the title of the manuscript'
keywords = 'keyword, another keyword, a third keyword, a final keyword'
abstract = 'This is an abstract describing some aspect of some language.'

get_peers(title, keywords, abstract)
```
The output of the `get_peers` function is a list of tuples, each of them including (i) the name of a potential reviewer, (ii) a list of keywords matching that author with the provided abstract, (iii) a sample manuscript of the author related to the abstract provided, (iv) the lingbuzz id of the manuscript, and (v) the cosine similarity between the abstract provided and the retrieved manuscript.


## Retraining the Classifier
You can retrain the classifier by providing a new dataset from Lingbuzz. To do this, follow these steps:

1. Obtain a new dataset from Lingbuzz by running the [lingbuzz_scraper](https://github.com/cmunozperez/lingbuzz_scraper) tool.
2. Place the newly generated csv file in the project directory.
3. Run the script with the -newdata flag:

```
python main.py -newdata
```

This will allow you to retrain the classifier using the new dataset.





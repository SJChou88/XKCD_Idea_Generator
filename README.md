# XKCD_Idea_Generator

Everyone encounters writer's block at some point. Looking at XKCD, we train a recurrent neural network on transcripts scraped from www.explainxkcd.com. We then generate new transcripts starting from seed phrases. Code is included for a website that interfaces with the model via Flask.

## Prerequisites

Other than standard python packages, the primary additional package required is keras.

## Data

Data consists of transcripts scraped from www.explainxkcd.com. Characters that were used less than 10 times were removed from the text corpus, which results in about 1800 transcripts consisting of 1.3 million characters.

## Model

The model is a long short term memory network, which is a form of a recurrent neural network. 

### Generator

A seed is given to the generator and predictions are made on the next letter. This is repeated until the given length is reached.

## Acknowledgements

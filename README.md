# Word2vec Financial Sentiment

Issues:

pre-processing
pmi
similarity (word2vec)
evaluation

Format Files:

**trannin/test**
{
  "id":{
    "label":"positive",
    "text":["word1", "worn2"..."wordN"]
  }
}

**result**

{
  "id":{
    “label”:”positive”,
    "mean_max":{“positive”: SIMILATRITY, “negative”: SIMILATRITY},
    "mean_general":{“positive”: SIMILATRITY, “negative”: SIMILATRITY}}
}

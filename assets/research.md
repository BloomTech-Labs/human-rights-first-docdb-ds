# Research Findings
We put together this page in order to pass along the flow of research to future cohorts and present findings on why specific technologies were selected over others.



## Box API




## Tesseract
For this project, we are using [PyTesseract](https://pypi.org/project/pytesseract/), a wrapper designed for work with Google's [Tesseract](https://opensource.google/projects/tesseract) OCR Engine. Research into Tesseract functionality has included use cases with [cv2](https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/) for better image blur detection. We eventually dismissed this notion as it was deemed unneccessary for our project needs.



## FastAPI



## MongoDB
[MongoDB](https://www.mongodb.com/) was chosen as the database housing for this project. [Here](https://github.com/Lambda-School-Labs/human-rights-first-docdb-ds/blob/feature/mongo_population_research/assets/mongo_population_research.md) you can find the research our team has completed about this library.



## NER
[SpaCy](https://spacy.io/) offers pretrained models for Named Entity Recognition. But the key terms most pertinent to our stakeholder are not necessarily recognized by generic models.
- [Prodigy](https://prodi.gy/) is a tool for building custom NER datasets.
- Annotation is always labor-intensive, but prodigy could work well for us, or for the researchers themselves, if our app somehow exposes this functionality to the end user. See [this video for a walkthrough](https://www.youtube.com/watch?v=59BKHO_xBPA).



## Pegasus
Automated document summaries come in many forms.
- For a broad overview, see these [lecture slides](http://web.stanford.edu/class/cs276b/handouts/lecture14.pdf).
- Abstractive summaries are feasible with Google's [PEGASUS](https://arxiv.org/pdf/1912.08777.pdf), available in the [repo](https://github.com/google-research/pegasus) and described on [Google's AI blog](https://ai.googleblog.com/2020/06/pegasus-state-of-art-model-for.html).

## Future Research
- Tags:
  Extracting tags could be achieved by vectorization (TFIDF, CountVectorizer or SpaCy) of documents.

## MongoDB Population Research Discussion
Jacob Smith, Hunter Jordan, Josh Araujo, Peter Rockwood

We are tasked with creating a script that:
-  Grabs a pdf from Box
-  Extract pdf text via Tesseract OCR
-  Packages it into a dictionary along with any additional key/value pairs we may need in the future.
- Pushes it to a MongoDB Table.

### Grabing a pdf
- We now have a method in the box_wrapper class that makes this simple:
- `byte_str = BoxWrapper().download_file(file_id)`

### OCR text extraction
- We now have a method from the DocProcessor class in ocr.py that makes this simple:
- `text = DocProcessor().get_text(byte_str, dpi=200)`

### Creating a mongoDB bound dict:
At minimum we need:
- A link to the pdf in Box. This can be obtained via `BoxWrapper().get_file_info(file_id)['url']`
- The text output from Tessaract: `text` in this case.

Our current best guess at what will need to be included looks like this:
```
info = BoxWrapper().get_file_info(file_id)
file_dict = {
	'url' : info['url']
	'text': text,  
	'file_path': info['path'],  
	'tags': tags, #from spaCy NER perhaps?
	'metadata': metadata  
}
```

### Pushing dict to MongoDB table
- Again, this is simple using the provided Data.insert() method from  data.py
- `Data().insert(file_dict)`

We have the ability to do bulk inserts of dicts by passing a list of dicts into the method above. That may be preferred in an offline process.

Notes:
- Josh came to the discussion with fully formed code in hand that implements everything above. We are working on adapting his code to recent changes in the DS repo and should have a working code to push soon!
- We need some clarity on whether the MongoDB populating will be run on or offline, this will impact how we approach crawling through the Box repository.
- We will want to have a team wide discussion down the road about what should go in each Mongo record.
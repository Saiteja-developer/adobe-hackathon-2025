Methodology
Challenge 1b is to provide a system that will extract all relevant sections and subsections from a collection of PDFs in a specific domain area, according to a provided user persona with a job-to-be-done. Our solution is offline, CPU-only, domain-independent, and able to process any number of document collections in succession.

1. Input Handling
Each collection folder (e.g., Collection_1, Collection_2, …) contains:
A PDFs/ folder containing 3-10 documents with similar content, including some or all of an issue.
A challenge1b_input.json file detailing the persona and job-to-be-done.
Our program loads these inputs and sets up the files for analysis, using an automated batch loop through each collection.

2. PDF Text Block Extraction
With the help of pdfplumber, we parse out each PDF into separate text blocks along with the associated metadata, such as page number, bounding box, and font specifications. We filter out the raw data for noise, excluding empty or too short fragments in order to retain only meaningful material.

3. Semantic Relevance Ranking
In order to evaluate how well each block aligns with the personas goal:
We created semantic representations of both the user query and each text block using TF-IDF vectorization (scikit-learn).
Cosine similarity is measured between the persona+job vector and each block.
We can do an additional domain-category aware heuristic boost (optional), so we can better order blocks in a category that is more relevant to the domain (i.e. food, cities, travel tips).
Top 5 blocks are chosen based on their semantic score.

4. Summarization of Subsections
All of the top-ranked blocks are passed to a light-weight summarization module with nltk. It tokenizes the content into sentences and runs a simple scoring method, keeping the most informative (1-3 per block) sentences in a condensed summary for “subsection analysis.”

5. JSON Output Generation
We lay out the output in the desired structure:
metadata: which contains the input documents, persona, job, and timestamp.
extracted_sections: Title, page number and rank of importance, for the top 5 blocks.
subsection_analysis: Edited summaries of those sections.
Our final output is saved as challenge1b_output.json in each collection folder.

6. Execution Strategy
All code will run offline in a Docker container (AMD64 CPU architecture), to allow for sequential processing of any number of collections. Total runtime is about 60 seconds, under 1 GB of model size, and no internet is required.
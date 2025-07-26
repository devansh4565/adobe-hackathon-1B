import fitz  # PyMuPDF
import os
import json
from sentence_transformers import SentenceTransformer, util

# --- Step 1: Load the pre-trained model ---
# The first time this runs, it will download the model.
# For Docker, the model must be included in the image to work offline.
print("Loading sentence transformer model...")
# The model will be located at this path *inside* the Docker image
model_path = '/app/local_model'
model = SentenceTransformer(model_path)
print("Model loaded.")


def extract_text_chunks(pdf_path):
    """
    Extracts structured text chunks (title, content, page) from a PDF.
    This function is from our previous step.
    """
    doc = fitz.open(pdf_path)
    doc_name = os.path.basename(pdf_path)
    chunks = []
    
    headings = []
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    if line["spans"]:
                        first_span = line["spans"][0]
                        if len(line["spans"]) == 1 and first_span["size"] > 13:
                            headings.append({
                                "title": first_span["text"].strip(),
                                "page": page_num,
                                "y_pos": line["bbox"][1]
                            })

    if not headings:
        full_text = "".join(page.get_text() for page in doc)
        chunks.append({
            "doc_name": doc_name, "page_num": 0,
            "section_title": "Full Document Text", "content": full_text
        })
        return chunks

    for i, heading in enumerate(headings):
        start_page, start_y = heading["page"], heading["y_pos"]
        end_page = headings[i+1]["page"] if i + 1 < len(headings) else len(doc) - 1
        end_y = headings[i+1]["y_pos"] if i + 1 < len(headings) else 9999

        section_content = ""
        for page_num in range(start_page, end_page + 1):
            page = doc[page_num]
            text_blocks = page.get_text("blocks")
            for block in text_blocks:
                block_y = block[1]
                is_after_start = (page_num > start_page) or (page_num == start_page and block_y > start_y)
                is_before_end = (page_num < end_page) or (page_num == end_page and block_y < end_y)
                if is_after_start and is_before_end:
                    section_content += block[4]
        
        chunks.append({
            "doc_name": doc_name, "page_num": heading["page"],
            "section_title": heading["title"], "content": f"{heading['title']}\n{section_content.strip()}"
        })
    return chunks


def rank_chunks_by_relevance(query, chunks):
    """
    Ranks text chunks based on their semantic similarity to a query
    using the optimized semantic_search function.
    """
    chunk_contents = [chunk['content'] for chunk in chunks]
    
    print("Generating embeddings...")
    # Generate embeddings for all chunks at once
    chunk_embeddings = model.encode(chunk_contents, convert_to_tensor=True)
    
    print("Performing semantic search...")
    # Use the optimized semantic_search to find the top k most similar chunks
    # We ask for all chunks (len(chunks)) and it will return them ranked.
    hits = util.semantic_search(model.encode(query), chunk_embeddings, top_k=len(chunks))
    
    # The output is a list of lists, we only need the first list for our single query
    hits = hits[0] 
    
    # --- Re-order our original chunks based on the search results ---
    ranked_chunks = []
    for hit in hits:
        # Get the original chunk using the index from the search result
        original_chunk = chunks[hit['corpus_id']]
        original_chunk['score'] = hit['score']
        ranked_chunks.append(original_chunk)
        
    return ranked_chunks

# --- Example Usage ---
if __name__ == '__main__':
    # --- This part is the same as before ---
    pdf_directory = 'input_docs'
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
        print(f"Created '{pdf_directory}'. Please add your PDFs there to test.")

    all_document_chunks = []
    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            print(f"Processing {pdf_path}...")
            chunks = extract_text_chunks(pdf_path)
            all_document_chunks.extend(chunks)

    # --- This is the new part for ranking ---
    if all_document_chunks:
        # Define the persona and job-to-be-done (from the PDF example)
        persona = "PhD Researcher in Computational Biology"
        job_to_be_done = "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks for Graph Neural Networks"
        query = f"Persona: {persona}. Job: {job_to_be_done}"

        # Get the ranked list of chunks
        ranked_results = rank_chunks_by_relevance(query, all_document_chunks)
        
        # --- Display the top 5 most relevant sections ---
        print("\n--- Top 5 Most Relevant Sections ---")
        for i, result in enumerate(ranked_results[:5]):
            print(f"Rank {i+1}: Score: {result['score']:.4f}")
            print(f"  Document: {result['doc_name']}, Page: {result['page_num']}")
            print(f"  Section: {result['section_title']}")
            print("-" * 20)
    else:
        print("No documents processed. Please add PDFs to the 'input_docs' folder.")
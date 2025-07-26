#!/usr/bin/env python3
"""
Content Segmentation Module for Adobe Hackathon Round 1B
Extracts full text content for each heading identified in the Round 1A outline.
"""

import fitz  # PyMuPDF
import json
import os
from typing import List, Dict, Any, Tuple
import re

class ContentSegmenter:
    """Extracts content for each section based on heading boundaries."""
    
    def __init__(self):
        self.negative_keywords = [
            'figure', 'table', 'university', 'department', 'institute',
            'inc.', 'llc', 'copyright', 'issn', 'editor', 'author',
            'reviewed by', 'letter from', 'in this issue', 'continued', 'www.'
        ]
    
    def is_valid_heading(self, line_text: str) -> bool:
        """Check if a line is a valid heading."""
        text_lower = line_text.lower()
        if not text_lower.strip() or len(text_lower) > 200:
            return False
        if any(keyword in text_lower for keyword in self.negative_keywords):
            return False
        if re.search(r'\S+@\S+', text_lower):
            return False
        return True
    
    def find_heading_bbox(self, page: fitz.Page, heading_text: str) -> Tuple[float, float]:
        """Find the bounding box coordinates of a heading on a page."""
        try:
            # Search for the heading text on the page
            rect_list = page.search_for(heading_text)
            if rect_list:
                # Return the first (highest) occurrence
                rect = rect_list[0]
                return rect.y0, rect.y1  # top and bottom coordinates
            return None, None
        except Exception:
            return None, None
    
    def extract_text_in_range(self, page: fitz.Page, start_y: float, end_y: float) -> str:
        """Extract text within a vertical range on a page."""
        try:
            # Get text dictionary with sorted blocks
            text_dict = page.get_text("dict", sort=True, flags=fitz.TEXTFLAGS_TEXT)
            extracted_text = []
            
            for block in text_dict["blocks"]:
                if block["type"] == 0:  # Text block
                    block_bbox = block["bbox"]
                    block_y0, block_y1 = block_bbox[1], block_bbox[3]
                    
                    # Check if block is within our vertical range
                    if start_y <= block_y1 and block_y0 <= end_y:
                        for line in block["lines"]:
                            line_text = " ".join(span['text'] for span in line['spans']).strip()
                            if line_text:
                                extracted_text.append(line_text)
            
            return " ".join(extracted_text)
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def extract_section_content(self, pdf_path: str, outline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract content for each section based on the outline."""
        extracted_sections = []
        
        try:
            with fitz.open(pdf_path) as doc:
                for i, section in enumerate(outline):
                    if not self.is_valid_heading(section['text']):
                        continue
                    
                    section_content = []
                    current_page = section['page']
                    
                    # Find the next section to determine content boundaries
                    next_section = None
                    if i + 1 < len(outline):
                        next_section = outline[i + 1]
                    
                    # Extract content from current page
                    page = doc[current_page]
                    heading_y0, heading_y1 = self.find_heading_bbox(page, section['text'])
                    
                    if heading_y0 is not None:
                        # Determine end boundary for current page
                        if next_section and next_section['page'] == current_page:
                            # Next section is on same page
                            next_y0, _ = self.find_heading_bbox(page, next_section['text'])
                            end_y = next_y0 if next_y0 else page.rect.height
                        else:
                            # Next section is on different page or this is the last section
                            end_y = page.rect.height
                        
                        # Extract text from current page
                        page_content = self.extract_text_in_range(page, heading_y1, end_y)
                        if page_content.strip():
                            section_content.append(page_content)
                    
                    # Extract content from subsequent pages until next section
                    if next_section:
                        for page_num in range(current_page + 1, next_section['page']):
                            if page_num < len(doc):
                                page = doc[page_num]
                                page_content = self.extract_text_in_range(page, 0, page.rect.height)
                                if page_content.strip():
                                    section_content.append(page_content)
                        
                        # Extract content from the page with next section (up to next section)
                        if next_section['page'] < len(doc):
                            page = doc[next_section['page']]
                            next_y0, _ = self.find_heading_bbox(page, next_section['text'])
                            if next_y0:
                                page_content = self.extract_text_in_range(page, 0, next_y0)
                                if page_content.strip():
                                    section_content.append(page_content)
                    else:
                        # This is the last section, extract from remaining pages
                        for page_num in range(current_page + 1, len(doc)):
                            page = doc[page_num]
                            page_content = self.extract_text_in_range(page, 0, page.rect.height)
                            if page_content.strip():
                                section_content.append(page_content)
                    
                    # Combine all content for this section
                    full_content = " ".join(section_content).strip()
                    
                    if full_content:  # Only add sections with content
                        extracted_sections.append({
                            'doc_name': os.path.basename(pdf_path),
                            'heading_text': section['text'],
                            'page_num': section['page'],
                            'content_text': full_content,
                            'level': section['level']
                        })
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
        
        return extracted_sections
    
    def process_document(self, pdf_path: str, outline_path: str) -> List[Dict[str, Any]]:
        """Process a single document and its outline to extract section content."""
        try:
            # Load the outline from Round 1A
            with open(outline_path, 'r', encoding='utf-8') as f:
                outline_data = json.load(f)
            
            outline = outline_data.get('outline', [])
            
            # Check if it's a text file (for testing) or PDF
            if pdf_path.endswith('.txt') or pdf_path.endswith('.pdf') and not os.path.exists(pdf_path):
                # For testing with text files
                return self.extract_section_content_from_text(pdf_path, outline)
            else:
                # For actual PDF files
                if not outline:
                    # If no outline, extract content directly from PDF
                    return self.extract_content_directly_from_pdf(pdf_path)
                else:
                    # Use the outline to extract content
                    return self.extract_section_content(pdf_path, outline)
            
        except Exception as e:
            print(f"Error processing document {pdf_path}: {e}")
            return []
    
    def extract_content_directly_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract content directly from PDF when no outline is available."""
        try:
            import fitz  # PyMuPDF
            
            with fitz.open(pdf_path) as doc:
                sections = []
                
                # Process each page separately to get page numbers
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    page_text = page.get_text()
                    
                    if not page_text.strip():
                        continue
                    
                    # Split page text into lines
                    lines = page_text.split('\n')
                    current_section = None
                    current_content = []
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Check if this line looks like a heading
                        is_heading = (
                            len(line) < 100 and 
                            (line.isupper() or 
                             line.endswith(':') or 
                             line.endswith('.') or
                             any(keyword in line.lower() for keyword in [
                                 'guide', 'activities', 'tips', 'cuisine', 'history', 'culture', 
                                 'restaurants', 'hotels', 'cities', 'coastal', 'adventures',
                                 'packing', 'nightlife', 'entertainment', 'overview', 'introduction'
                             ]))
                        )
                        
                        if is_heading and len(line) > 10:
                            # Save previous section if exists
                            if current_section and current_content:
                                sections.append({
                                    'doc_name': os.path.basename(pdf_path),
                                    'heading_text': current_section,
                                    'page_num': page_num + 1,  # 1-indexed page numbers
                                    'content_text': '\n'.join(current_content),
                                    'level': 'H1'
                                })
                            
                            # Start new section
                            current_section = line
                            current_content = []
                        else:
                            # Add to current content
                            if current_section:
                                current_content.append(line)
                            elif len(line) > 50:  # Substantial content without heading
                                current_content.append(line)
                    
                    # Add the last section from this page
                    if current_section and current_content:
                        sections.append({
                            'doc_name': os.path.basename(pdf_path),
                            'heading_text': current_section,
                            'page_num': page_num + 1,  # 1-indexed page numbers
                            'content_text': '\n'.join(current_content),
                            'level': 'H1'
                        })
                
                # If no sections found, fall back to paragraph-based approach with page numbers
                if not sections:
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        page_text = page.get_text()
                        
                        if not page_text.strip():
                            continue
                        
                        paragraphs = [p.strip() for p in page_text.split('\n\n') if p.strip()]
                        for i, paragraph in enumerate(paragraphs[:5]):  # Limit per page
                            if len(paragraph) > 100:
                                # Try to extract a title from the first sentence
                                first_sentence = paragraph.split('.')[0]
                                title = first_sentence if len(first_sentence) < 100 else f"Section {i+1}"
                                
                                sections.append({
                                    'doc_name': os.path.basename(pdf_path),
                                    'heading_text': title,
                                    'page_num': page_num + 1,  # 1-indexed page numbers
                                    'content_text': paragraph,
                                    'level': 'H1'
                                })
                
                return sections
                
        except Exception as e:
            print(f"Error extracting content directly from PDF {pdf_path}: {e}")
            return []
    
    def extract_section_content_from_text(self, text_path: str, outline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract content from text file for testing purposes."""
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            extracted_sections = []
            
            for i, section in enumerate(outline):
                if not self.is_valid_heading(section['text']):
                    continue
                
                # Find the section content by looking for the heading and next heading
                heading_text = section['text']
                start_idx = content.find(heading_text)
                
                if start_idx == -1:
                    continue
                
                # Find the end of this section (next heading or end of file)
                end_idx = len(content)
                if i + 1 < len(outline):
                    next_heading = outline[i + 1]['text']
                    next_idx = content.find(next_heading, start_idx + len(heading_text))
                    if next_idx != -1:
                        end_idx = next_idx
                
                # Extract the content between headings
                section_content = content[start_idx + len(heading_text):end_idx].strip()
                
                if section_content:
                    extracted_sections.append({
                        'doc_name': os.path.basename(text_path),
                        'heading_text': section['text'],
                        'page_num': section['page'],
                        'content_text': section_content,
                        'level': section['level']
                    })
            
            return extracted_sections
            
        except Exception as e:
            print(f"Error extracting content from text file {text_path}: {e}")
            return []

def main():
    """Test the content segmenter with a sample document."""
    segmenter = ContentSegmenter()
    
    # Example usage
    pdf_path = "input/sample.pdf"
    outline_path = "output/sample.json"
    
    if os.path.exists(pdf_path) and os.path.exists(outline_path):
        sections = segmenter.process_document(pdf_path, outline_path)
        print(f"Extracted {len(sections)} sections with content")
        for section in sections[:3]:  # Show first 3 sections
            print(f"Section: {section['heading_text']}")
            print(f"Content length: {len(section['content_text'])} characters")
            print(f"Preview: {section['content_text'][:100]}...")
            print("-" * 50)

if __name__ == "__main__":
    main() 
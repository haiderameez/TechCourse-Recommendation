# Tech Course Recommendation
This is a custom chatbot using Langchain to extract, embed, and store course data, with a Flask RESTful API for interaction.

## Usage Guide

### 1. Download the Repository

### 2. Install all the dependencies using the following line of code:
```python
pip install -r requirements.txt
```

### 3. Data Scraping
- Run `extractor.py`, this will create a json file that will contain the course title, description and link.
- Similarly, also run `nested_extractor.py` this will update the json file to also contain the details of the course.
- The nested extractor scrapes within the already scraped courses.

### 4. Running the API  
- Run `app.py` to initialize the creation of the pickle file and also to run the api.
- To get answers from model, run queries similar to this

### 5. Example Usage
1. Query,
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:5000/search" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"query": "AWS cloud computing"}' | ConvertTo-Json -Depth 100
   ```
   This query will return
   ```json
   {  
    "full_content":  "LEARN CLOUD COMPUTING BASICS-AWS In this course we are going to cover the basics and the mostost important services on AWS, At the end In this course we are going to cover the basics and the most important services on AWS, At the end of this course, you will have a solid understanding of AWS and you can start using it for your projects.\n\nMAIN FEATURES OF THE PROGRAM:\n• One on One Live Interactive Sessions with verified Instructor\n• Customized Curriculum according to your kid’s progress\n• Simple and interesting assignments for easy learning\n• Class Tracking Report on daily basis.\n• Strong focus on Learning with Fun\n• Complete access of the study materials and Power Point Slides.",
    "link":  "https://brainlox.com/courses/872d1cb6-8469-4797-b267-8c41837b10e2",
    "title":  "LEARN CLOUD COMPUTING BASICS-AWS"
   }
   ```
2. Query,
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:5000/search" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"query": "Machine Learning"}' | ConvertTo-Json -Depth 100
   ```
   This query will return
   ```json
   {      
    "full_content":  "Machine Learning: 7-Day Project-Based Summer Camp Join our \"Machine Learning Mania\" camp for a 7-day tech adventure! Kids will tackle machine learning Join our \"Machine Learning Mania\" camp for a 7-day tech adventure! Kids will tackle machine learning, using Python to predict house prices, segment customers, and explore neural networks. An exciting introduction to this groundbreaking field awaits - enroll your young coder today",
    "link":  "https://brainlox.com/courses/1db857a4-f374-49fb-af9c-0f6d2e5ada45",
    "title":  "Machine Learning: 7-Day Project-Based Summer Camp"
   }
  ```

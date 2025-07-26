
import re
import PyPDF2
import io
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from concurrent.futures import ThreadPoolExecutor
import tempfile
import os
import json

class ResumeAnalysisAgent:
    def __init__(self, api_key, cutoff_score=75):
        self.api_key = api_key
        self.cutoff_score = cutoff_score
        self.resume_text = None
        self.rag_vectorstore = None
        self.analysis_result = None
        self.jd_text = None
        self.extracted_skills = None
        self.resume_weaknesses = []
        self.resume_strengths = []
        self.improvement_suggestions = {}

    def extract_text_from_pdf(self, pdf_file):
        """Extract text from a PDF file"""
        try:
            if hasattr(pdf_file, 'getvalue'): 
                pdf_data = pdf_file.getvalue()
                pdf_file_like = io.BytesIO(pdf_data)
                reader = PyPDF2.PdfReader(pdf_file_like)
            else: 
                reader = PyPDF2.PdfReader(pdf_file)
                
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_txt(self, txt_file):
        """Extract text from a text file"""
        try:
            if hasattr(txt_file, 'getvalue'):  
                return txt_file.getvalue().decode('utf-8')
            else: 
                with open(txt_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Error extracting text from text file: {e}")
            return ""

    def extract_text_from_file(self, file):
        """Extract text from a file (PDF or TXT)"""
        if hasattr(file, 'name'):
            file_extension = file.name.split('.')[-1].lower()
        else:
            file_extension = file.split('.')[-1].lower()
            
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(file)
        elif file_extension == 'txt':
            return self.extract_text_from_txt(file)
        else:
            print(f"Unsupported file extension: {file_extension}")
            return ""

    def create_rag_vector_store(self, text):
        """Create a vector store for RAG"""
   
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        
   
        embeddings = OpenAIEmbeddings(api_key=self.api_key)
        vectorstore = FAISS.from_texts(chunks, embeddings)
        return vectorstore

    def create_vector_store(self, text):
        """Create a simpler vector store for skill analysis"""
        embeddings = OpenAIEmbeddings(api_key=self.api_key)
        vectorstore = FAISS.from_texts([text], embeddings)
        return vectorstore

    def analyze_skill(self, qa_chain, skill):
        """Analyze a skill in the resume"""
        query = f"On a scale of 0-10, how clearly does the candidate mention proficiency in {skill}? Provide a numeric rating first, followed by reasoning."
        response = qa_chain.run(query)
        match = re.search(r"(\d{1,2})", response)
        score = int(match.group(1)) if match else 0
        

        reasoning = response.split('.', 1)[1].strip() if '.' in response and len(response.split('.')) > 1 else ""
        
    
        return skill, min(score, 10), reasoning

    def analyze_resume_weaknesses(self):
        """Analyze specific weaknesses in the resume based on missing skills"""
        if not self.resume_text or not self.extracted_skills or not self.analysis_result:
            return []
        
        weaknesses = []
        
        for skill in self.analysis_result.get("missing_skills", []):
            try:
                llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=self.api_key)
                prompt = f"""
                Resume: {self.resume_text[:1000]}
                Skill: {skill}
                In 1-2 lines, JSON only:
                {{
                    "weakness": "...",
                    "improvement_suggestions": ["..."],
                    "example_addition": "..."
                }}
                """
                response = llm.invoke(prompt, timeout=30)
                weakness_content = response.content.strip() if hasattr(response, 'content') else str(response)
                try:
                    weakness_data = json.loads(weakness_content)
                    weakness_detail = {
                        "skill": skill,
                        "score": self.analysis_result.get("skill_scores", {}).get(skill, 0),
                        "detail": weakness_data.get("weakness", "No specific details provided."),
                        "suggestions": weakness_data.get("improvement_suggestions", []),
                        "example": weakness_data.get("example_addition", "")
                    }
                    weaknesses.append(weakness_detail)
                    self.improvement_suggestions[skill] = {
                        "suggestions": weakness_data.get("improvement_suggestions", []),
                        "example": weakness_data.get("example_addition", "")
                    }
                except Exception as json_err:
                    weaknesses.append({
                        "skill": skill,
                        "score": self.analysis_result.get("skill_scores", {}).get(skill, 0),
                        "detail": f"LLM output error: {weakness_content[:200]}"
                    })
            except Exception as e:
                weaknesses.append({
                    "skill": skill,
                    "score": self.analysis_result.get("skill_scores", {}).get(skill, 0),
                    "detail": f"API error: {str(e)[:200]}"
                })
        self.resume_weaknesses = weaknesses
        return weaknesses

    def extract_skills_from_jd(self, jd_text):
        """Extract skills from a job description"""
        try:
            llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=self.api_key)
            prompt = f"""
            JD: {jd_text[:1000]}
            List all skills as a Python list. Output only the list, nothing else.
            """
            response = llm.invoke(prompt, timeout=30)
            skills_text = response.content if hasattr(response, 'content') else str(response)
            match = re.search(r'\[(.*?)\]', skills_text, re.DOTALL)
            if match:
                skills_text = match.group(0)
            try:
                skills_list = eval(skills_text)
                if isinstance(skills_list, list):
                    return skills_list
            except Exception as eval_err:
                pass
            skills = []
            for line in skills_text.split('\n'):
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    skill = line[2:].strip()
                    if skill:
                        skills.append(skill)
                elif line.startswith('"') and line.endswith('"'):
                    skill = line.strip('"')
                    if skill:
                        skills.append(skill)
            return skills
        except Exception as e:
            print(f"Error extracting skills from job description: {e}")
            return []

    def semantic_skill_analysis(self, resume_text, skills):
        """Analyze skills semantically"""
        vectorstore = self.create_vector_store(resume_text)
        retriever = vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-3.5-turbo", api_key=self.api_key),
            retriever=retriever,
            return_source_documents=False
        )

        skill_scores = {}
        skill_reasoning = {}
        missing_skills = []
        total_score = 0

        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda skill: self.analyze_skill(qa_chain, skill), skills))

        for skill, score, reasoning in results:
            skill_scores[skill] = score
            skill_reasoning[skill] = reasoning
            total_score += score
            if score <= 5:
                missing_skills.append(skill)

        overall_score = int((total_score / (10 * len(skills))) * 100)
        selected = overall_score >= self.cutoff_score

        reasoning = "Candidate evaluated based on explicit resume content using semantic similarity and clear numeric scoring."
        strengths = [skill for skill, score in skill_scores.items() if score >= 7]
        improvement_areas = missing_skills if not selected else []
        

        self.resume_strengths = strengths

        return {
            "overall_score": overall_score,
            "skill_scores": skill_scores,
            "skill_reasoning": skill_reasoning,
            "selected": selected,
            "reasoning": reasoning,
            "missing_skills": missing_skills,
            "strengths": strengths,
            "improvement_areas": improvement_areas
        }

    def analyze_resume(self, resume_file, role_requirements=None, custom_jd=None):
        """Analyze a resume against role requirements or a custom JD"""
        self.resume_text = self.extract_text_from_file(resume_file)
        
       
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as tmp:
            tmp.write(self.resume_text)
            self.resume_file_path = tmp.name
     
        self.rag_vectorstore = self.create_rag_vector_store(self.resume_text)
        
   
        if custom_jd:
            self.jd_text = self.extract_text_from_file(custom_jd)
            self.extracted_skills = self.extract_skills_from_jd(self.jd_text)
            
        
            self.analysis_result = self.semantic_skill_analysis(self.resume_text, self.extracted_skills)
    
        elif role_requirements:
            self.extracted_skills = role_requirements
            
 
            self.analysis_result = self.semantic_skill_analysis(self.resume_text, role_requirements)
            
    
        if self.analysis_result and "missing_skills" in self.analysis_result and self.analysis_result["missing_skills"]:
            self.analyze_resume_weaknesses()
     
            self.analysis_result["detailed_weaknesses"] = self.resume_weaknesses
        
        return self.analysis_result

    def ask_question(self, question):
        """Ask a question about the resume"""
        if not self.rag_vectorstore or not self.resume_text:
            return "Please analyze a resume first."
        
        retriever = self.rag_vectorstore.as_retriever(
            search_kwargs={"k": 3}  
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-3.5-turbo", api_key=self.api_key),
            chain_type="stuff",  
            retriever=retriever,
            return_source_documents=False,
        )
        
        response = qa_chain.run(question)
        return response

    def generate_interview_questions(self, question_types, difficulty, num_questions):
        """Generate interview questions based on the resume"""
        if not self.resume_text or not self.extracted_skills:
            return []
        
        try:
            llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=self.api_key)
            context = f"Resume: {self.resume_text[:1000]} | Skills: {', '.join(self.extracted_skills)} | Strengths: {', '.join(self.analysis_result.get('strengths', []))} | Gaps: {', '.join(self.analysis_result.get('missing_skills', []))}"
            prompt = f"""
            Give {num_questions} {difficulty.lower()} interview questions for this candidate. Only these types: {', '.join(question_types)}. Short, direct, no explanation. Format: (Type, Question)
            {context}
            """
            
            response = llm.invoke(prompt)
            questions_text = response.content
            
      
            questions = []
            pattern = r'[("]([^"]+)[",)\s]+[(",\s]+([^"]+)[")\s]+'
            matches = re.findall(pattern, questions_text, re.DOTALL)
            
            for match in matches:
                if len(match) >= 2:
                    question_type = match[0].strip()
                    question = match[1].strip()
                    
     
                    for requested_type in question_types:
                        if requested_type.lower() in question_type.lower():
                            questions.append((requested_type, question))
                            break
            

            if not questions:
                lines = questions_text.split('\n')
                current_type = None
                current_question = ""
                
                for line in lines:
                    line = line.strip()
                    if any(t.lower() in line.lower() for t in question_types) and not current_question:
                        current_type = next((t for t in question_types if t.lower() in line.lower()), None)
                        if ":" in line:
                            current_question = line.split(":", 1)[1].strip()
                    elif current_type and line:
                        current_question += " " + line
                    elif current_type and current_question:
                        questions.append((current_type, current_question))
                        current_type = None
                        current_question = ""

            questions = questions[:num_questions]
            
            return questions
        
        except Exception as e:
            print(f"Error generating interview questions: {e}")
            return []

    def improve_resume(self, improvement_areas, target_role=""):
        """Generate suggestions to improve the resume"""
        if not self.resume_text:
            return {}
        
        try:
           
            improvements = {}
            
  
            for area in improvement_areas:
           
                if area == "Skills Highlighting" and self.resume_weaknesses:
                    skill_improvements = {
                        "description": "Your resume needs to better highlight key skills that are important for the role.",
                        "specific": []
                    }
                 
                    before_after_examples = {}
                    
                    for weakness in self.resume_weaknesses:
                        skill_name = weakness.get("skill", "")
                        if "suggestions" in weakness and weakness["suggestions"]:
                            for suggestion in weakness["suggestions"]:
                                skill_improvements["specific"].append(f"**{skill_name}**: {suggestion}")
                        
                        if "example" in weakness and weakness["example"]:
                       
                            resume_chunks = self.resume_text.split('\n\n')
                            relevant_chunk = ""
                            
                            
                            for chunk in resume_chunks:
                                if skill_name.lower() in chunk.lower() or "experience" in chunk.lower():
                                    relevant_chunk = chunk
                                    break
                            
                            if relevant_chunk:
                                before_after_examples = {
                                    "before": relevant_chunk.strip(),
                                    "after": relevant_chunk.strip() + "\n• " + weakness["example"]
                                }
                    
                    if before_after_examples:
                        skill_improvements["before_after"] = before_after_examples
                    
                    improvements["Skills Highlighting"] = skill_improvements
 
            remaining_areas = [area for area in improvement_areas if area not in improvements]
            
            if remaining_areas:
                llm = ChatOpenAI(model="gpt-4.1-nano", api_key=self.api_key)
                
                # Create a context with resume analysis and weaknesses
                weaknesses_text = ""
                if self.resume_weaknesses:
                    weaknesses_text = "Resume Weaknesses:\n"
                    for i, weakness in enumerate(self.resume_weaknesses):
                        weaknesses_text += f"{i+1}. {weakness['skill']}: {weakness['detail']}\n"
                        if "suggestions" in weakness:
                            for j, sugg in enumerate(weakness["suggestions"]):
                                weaknesses_text += f"   - {sugg}\n"
                
                context = f"""
                Resume Content:
                {self.resume_text}
                
                Skills to focus on: {', '.join(self.extracted_skills)}
                
                Strengths: {', '.join(self.analysis_result.get('strengths', []))}
                
                Areas for improvement: {', '.join(self.analysis_result.get('missing_skills', []))}
                
                {weaknesses_text}
                
                Target role: {target_role if target_role else "Not specified"}
                """
                
                prompt = f"""
                Provide detailed suggestions to improve this resume in the following areas: {', '.join(remaining_areas)}.
                
                {context}
                
                For each improvement area, provide:
                1. A general description of what needs improvement
                2. 3-5 specific actionable suggestions
                3. Where relevant, provide a before/after example
                
                Format the response as a JSON object with improvement areas as keys, each containing:
                - "description": general description
                - "specific": list of specific suggestions
                - "before_after": (where applicable) a dict with "before" and "after" examples
                
                Only include the requested improvement areas that aren't already covered.
                Focus particularly on addressing the resume weaknesses identified.
                """
                
                response = llm.invoke(prompt)
                
                # Try to parse JSON from the response
                ai_improvements = {}
                
                # Extract from markdown code blocks if present
                json_match = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', response.content)
                if json_match:
                    try:
                        ai_improvements = json.loads(json_match.group(1))
                        # Merge with existing improvements
                        improvements.update(ai_improvements)
                    except json.JSONDecodeError:
                        pass
                
                # If JSON parsing failed, create structured output manually
                if not ai_improvements:
                    sections = response.content.split("##")
                    
                    for section in sections:
                        if not section.strip():
                            continue
                            
                        lines = section.strip().split("\n")
                        area = None
                        
                        for line in lines:
                            if not area and line.strip():
                                area = line.strip()
                                improvements[area] = {
                                    "description": "",
                                    "specific": []
                                }
                            elif area and "specific" in improvements[area]:
                                if line.strip().startswith("- "):
                                    improvements[area]["specific"].append(line.strip()[2:])
                                elif not improvements[area]["description"]:
                                    improvements[area]["description"] += line.strip()
            
            # Ensure all requested areas are included
            for area in improvement_areas:
                if area not in improvements:
                    improvements[area] = {
                        "description": f"Improvements needed in {area}",
                        "specific": ["Review and enhance this section"]
                    }
            
            return improvements
        
        except Exception as e:
            print(f"Error generating resume improvements: {e}")
            return {area: {"description": "Error generating suggestions", "specific": []} for area in improvement_areas}

    def get_improved_resume(self, target_role="", highlight_skills=""):
        """Generate an improved version of the resume optimized for the job description"""
        if not self.resume_text:
            return "Please upload and analyze a resume first."
        
        try:
            # Parse highlight skills if provided
            skills_to_highlight = []
            if highlight_skills:

                if len(highlight_skills) > 100: 
                    self.jd_text = highlight_skills
                    try:
                        parsed_skills = self.extract_skills_from_jd(highlight_skills)
                        if parsed_skills:
                            skills_to_highlight = parsed_skills
                        else:
                 
                            skills_to_highlight = [s.strip() for s in highlight_skills.split(",") if s.strip()]
                    except:
      
                        skills_to_highlight = [s.strip() for s in highlight_skills.split(",") if s.strip()]
                else:
                    skills_to_highlight = [s.strip() for s in highlight_skills.split(",") if s.strip()]
        
            if not skills_to_highlight and self.analysis_result:

                skills_to_highlight = self.analysis_result.get('missing_skills', [])
  
                skills_to_highlight.extend([
                    skill for skill in self.analysis_result.get('strengths', [])
                    if skill not in skills_to_highlight
                ])

                if self.extracted_skills:
                    skills_to_highlight.extend([
                        skill for skill in self.extracted_skills 
                        if skill not in skills_to_highlight
                    ])
            

            weakness_context = ""
            improvement_examples = ""
            
            if self.resume_weaknesses:
                weakness_context = "Address these specific weaknesses:\n"
                
                for weakness in self.resume_weaknesses:
                    skill_name = weakness.get('skill', '')
                    weakness_context += f"- {skill_name}: {weakness.get('detail', '')}\n"
                    
           
                    if 'suggestions' in weakness and weakness['suggestions']:
                        weakness_context += "  Suggested improvements:\n"
                        for suggestion in weakness['suggestions']:
                            weakness_context += f"  * {suggestion}\n"
    
                    if 'example' in weakness and weakness['example']:
                        improvement_examples += f"For {skill_name}: {weakness['example']}\n\n"
            
    
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, api_key=self.api_key)
            
     
            jd_context = ""
            if self.jd_text:
                jd_context = f"Job Description:\n{self.jd_text}\n\n"
            elif target_role:
                jd_context = f"Target Role: {target_role}\n\n"
            
            prompt = f"""
            Resume: {self.resume_text[:1000]}
            {jd_context}
            Highlight: {', '.join(skills_to_highlight)}
            {weakness_context}
            {improvement_examples}
            Rewrite resume for this job. Short, modern, clear sections. Add only key improvements. Output only the improved resume text, no extra explanation.
            """
            
            response = llm.invoke(prompt)
            improved_resume = response.content.strip()
       
            with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as tmp:
                tmp.write(improved_resume)
                self.improved_resume_path = tmp.name
            
            return improved_resume
        
        except Exception as e:
            print(f"Error generating improved resume: {e}")
            return "Error generating improved resume. Please try again."

    def cleanup(self):
        """Clean up temporary files"""
        try:
            if hasattr(self, 'resume_file_path') and os.path.exists(self.resume_file_path):
                os.unlink(self.resume_file_path)
            
            if hasattr(self, 'improved_resume_path') and os.path.exists(self.improved_resume_path):
                os.unlink(self.improved_resume_path)
        except Exception as e:
            print(f"Error cleaning up temporary files: {e}")
  # molit-gemma-rag-chatbot                                                                                                                                
                  
  > 거대언어모델 기반 국토교통 분야 데이터 질의응답 챗봇 시스템                                                                                            
   
  [![Paper](https://img.shields.io/badge/Paper-RISS-blue)](https://www.riss.kr/link?id=T17378943)                                                                
  [![Model](https://img.shields.io/badge/HuggingFace-molit--gemma-yellow)](https://huggingface.co/chohi/gemma-molit-finetuned/blob/main/README.md)
  [![License](https://img.shields.io/badge/License-Gemma-green)](LICENSE)                                                                                  
                                                                                                                                                           
  대한민국 국토교통부 정책 문서를 학습한 sLLM(`molit-gemma`)과                                                                                             
  OpenSearch 기반 RAG 파이프라인을 결합한 **온프레미스 정부 도메인 챗봇** 구현 코드입니다.                                                                 
                                                                                                                                                           
  ## ✨ Features  
  - 🇰🇷 한국어 정부 도메인 특화 (Gemma-3-1B fine-tuned)                                                                                                     
  - 🔍 OpenSearch 기반 RAG로 환각 완화                                                                                                                     
  - 🔒 온프레미스 배포 (외부 API 의존성 없음)                                                                                                              
  - 📊 BLEU 0.6258 / LLM-as-a-Judge 4.34                                                                                                                   
                                                                                                                                                           
  ## 🏗️  Architecture                                                                                                                                       
  ```             
  [사용자 질의]
     ↓                                                                                                                                                     
  [OpenSearch] ← 국토교통부 정책 문서 임베딩
     ↓ (Top-K 검색)                                                                                                                                        
  [molit-gemma] ← Gemma-3-1B fine-tuned
     ↓                                                                                                                                                     
  [RAG 응답 + 출처]
  ```                                                                                                                                                      
                  
  ## 🚀 Quick Start                                                                                                                                        
  ```bash         
  git clone https://github.com/chohi22/molit-gemma-rag-chatbot
  cd molit-gemma-rag-chatbot                                                                                                                               
  pip install -r requirements.txt
                                                                                                                                                           
  # OpenSearch 실행
  docker compose up -d

  # 문서 인덱싱
  python scripts/index_documents.py --src data/molit_docs/                                                                                                 
                                                                                                                                                           
  # 챗봇 실행                                                                                                                                              
  python app.py                                                                                                                                            
  ```             

  ## 📁 Repository Structure
  ```
  ├── src/
  │   ├── retriever/        # OpenSearch RAG                                                                                                               
  │   ├── generator/        # molit-gemma 추론
  │   └── pipeline/         # 통합 파이프라인                                                                                                              
  ├── scripts/              # 인덱싱·평가 스크립트
  ├── eval/                 # BLEU, LLM-as-a-Judge                                                                                                         
  ├── notebooks/            # 실험 노트북                                                                                                                  
  └── docs/                 # 시스템 설계 문서                                                                                                             
  ```                                                                                                                                                      
                                                                                                                                                           
  ## 📈 Evaluation                                                                                                                                         
  | Method | BLEU | LLM-Judge |
  |--------|------|-----------|                                                                                                                            
  | Gemma-3-1B (baseline) | 0.41 | 3.12 |
  | Gemma-3-1B + RAG | 0.55 | 3.89 |                                                                                                                       
  | **molit-gemma + RAG** | **0.63** | **4.34** |                                                                                                          
                                                                                                                                                           
  ## 📄 Paper                                                                                                                                              
  정현일. (2026). 거대언어모델 기반 국토교통 분야 데이터 질의응답 챗봇 시스템
  설계 및 구현. 충북대학교 일반대학원 산업인공지능학과 석사학위논문.                                                                                       
  - 📚 RISS: https://www.riss.kr/link?id=T17378943                                                                                                                                     
  - 🤗 Model: https://huggingface.co/chohi/gemma-molit-finetuned/blob/main/README.md                                                                                                                          
                                                                                                                                                           
  ## 🤝 Contributing
  이슈와 PR 환영합니다.                                                                                                                                    
                                                                                                                                                           
  ## 📜 License
  - 코드: MIT                                                                                                                                              
  - 모델: Gemma Terms of Use
                                                                                                                                                           
  추가 권장 파일
                                                                                                                                                           
  - requirements.txt, docker-compose.yml                                                                                                                   
  - docs/architecture.md — 시스템 설계서
  - eval/results.md — 상세 평가 결과                                                                                                                       
  - LICENSE, CITATION.cff                                                                                                                                  
                                                  

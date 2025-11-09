Project: ATLAS

인지 지도 및 AI 코칭 플랫폼 기획서

문서 버전: 1.0
작성일: 2025년 11월 8일

1. 프로젝트 개요

1.1. 프로젝트명

Project: ATLAS (아틀라스)

1.2. 핵심 비전

"학습의 '블랙박스'를 열어, 학생의 잠재력을 지도로 그려내는 AI 코칭 플랫폼"

기존의 교육 AI가 '정답'을 맞혔는지에 집중했다면, ATLAS는 학생이 정답에 도달하는 **'사고 과정(Thought Process)'**과 **'잠재 역량(Latent Space)'**을 분석하고 시각화합니다.

본 프로젝트는 Pacer(코칭 플랫폼), Meta-RAG(논리 엔진), Manim(시각화 엔진) 프로젝트를 '4축 잠재 공간 모델'이라는 통일된 평가 기준 아래 통합하여, 코치의 티칭 활동을 극대화하는 것을 목표로 합니다.

2. 문제 정의: 학습은 '블랙박스'다

기존의 코칭 방식은 학생의 점수나 결과물에 의존합니다.

코치: 학생이 "왜" 이 문제를 틀렸는지, "어디서" 막혔는지 정확히 알기 어렵습니다.

학생: 자신이 무엇을 모르는지 모른 채, 비효율적인 학습을 반복합니다. (인지 과부하 발생 [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/docs/v1/COGNITIVE_OVERLOAD_SYSTEM.md])

학부모: '성적표' 외에는 자녀의 진짜 실력을 알 길이 없습니다.

우리의 목표: 이 블랙박스를 열어, 학생의 머릿속에 숨겨진 복잡한 인지 상태를 **'지도(Atlas)'**로 그려내는 것입니다.

3. 핵심 솔루션: 4축 잠재 공간 모델

ATLAS는 학생을 4개의 대륙, 11개의 세부 영역으로 구성된 '인지 지도'로 모델링합니다. 이 지도는 AI와 코치가 학생을 평가하는 공통의 'Ground Truth'가 됩니다.

축 1: 인지 기저 (기본기)

axis1_geo: 기하 (공간/도형 인식)

axis1_alg: 대수 (식/기호 조작)

axis1_ana: 해석 (함수/변화 추론)

축 2: 메타인지 (전략)

axis2_opt: 최적화 (가장 효율적인 풀이 탐색)

axis2_piv: 피벗 (다른 풀이로 전환하는 유연성)

axis2_dia: 자가 진단 (자신의 오류를 인지하는 능력)

축 3: 지식 상태 (숙련도)

axis3_con: 개념적 지식 (용어의 정의를 아는가)

axis3_pro: 절차적 지식 (공식을 적용할 줄 아는가)

axis3_ret: 인출 속도 (얼마나 빨리 기억해내는가)

축 4: 실행 지구력 (완성도)

axis4_acc: 연산 정확성 (실수 없이 계산하는 능력)

axis4_gri: 난이도 내성 (어려운 문제에 포기하지 않는 끈기)

4. 통합 아키텍처

ATLAS는 3개의 핵심 엔진과 1개의 중앙 DB로 구성됩니다.

Pacer API (Orchestrator): 학생/코치의 요청을 받는 메인 API 서버. Meta-RAG와 Manim을 지휘하는 오케스트레이터이자, 4축 모델을 갱신하는 코칭 플랫폼의 본체입니다. [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/backend/main.py]

Meta-RAG Engine (논리 엔진): 문제의 '논리'를 분석하고 '텍스트 해설' 및 '관련 개념'을 추출합니다. [cite: sigongjoa/meta_rag/meta_rag-ac1d9121360fbeb12d976007ec932cd2338563e3/docs/Meta-RAG_Project_Proposal.md]

Manim Agent (시각화 엔진): Meta-RAG가 찾아낸 '관련 개념'에 매칭되는 '사전 제작된 개념 애니메이션'을 제공합니다. (V1 전략) [cite: sigongjoa/manim_agnet/manim_agnet-c3cf328dd539ee6107ba38b5b7d3a15b964f6539/korean_math_problem.py]

Platform DB (ATLAS DB): 학생의 모든 활동과 '4축 모델'의 성장 이력(Student_Vector_History)을 저장하는 핵심 자산입니다.

5. 핵심 워크플로우

5.1. 👨‍🎓 학생: AI 주도 학습

문제 제출: 학생이 과제 문제(텍스트/이미지)를 플랫폼에 제출합니다.

즉각적 분석: Meta-RAG가 즉시 '논리적 풀이 텍스트'를 분석하고, "이 문제는 '근의 공식(C-001)' 개념이 필요합니다"라고 알려줍니다.

시각화 시청: Manim 라이브러리에서 C-001에 해당하는 '근의 공식 유도 애니메이션'을 학생에게 함께 제공합니다.

자동 평가(V2): 학생의 모든 상호작용(시청, 빨리감기, 문제 풀이 결과) 로그가 AI에 의해 분석되어 4축 모델 갱신의 기초 자료로 사용됩니다.

5.2. 👩‍🏫 코치: 데이터 기반 티칭

사전 진단: [정기 평가] 학생의 시험 결과를 AI가 분석하여 '4축 모델'을 '거시적'으로 갱신합니다.

수업 준비: 코치는 수업 전 학생의 4축 모델(레이더 차트)을 확인하여, axis2_piv(피벗 능력)이 낮음을 인지하고 수업을 설계합니다.

1:1 티칭: [Offline] 수업 중 학생의 취약점(피벗 사고)을 집중 지도합니다.

수동 갱신: [수업 후] 코치가 관찰한 '정성적 메모'("피벗 훈련에 집중함")를 기록하고, 코치의 전문적 판단으로 axis2_piv 점수를 30점에서 40점으로 수동 갱신합니다. 이 모든 활동이 Student_Vector_History에 이력으로 저장됩니다.

5.3. 👨‍👩‍👧 학부모: 투명한 리포팅

리포트 초안 생성: [주 1회] AI가 이번 주 학생의 '4축 모델 변화량'과 활동 내역을 기반으로 리포트 초안을 자동 생성합니다. (e.g., "이번 주 axis2_piv 10점 상승")

코치 승인: 코치가 AI 요약본과 자신의 '정성적 메모'를 결합하여 최종 코멘트를 작성하고 리포트를 승인합니다.

카카오톡 발송: 승인된 최종 리포트(4축 변화 차트 포함)가 학부모에게 카카오톡으로 자동 발송됩니다. [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/backend/kakao_sender.py]

6. 개발 로드맵 (V1 vs V2)

복잡성과 배포 비용 문제를 해결하기 위해 '뼈대(V1)'를 먼저 구축하고 '엔진(V2)'을 고도화합니다.

구분

V1 (현재 - 뼈대 구축)

V2 (미래 - 엔진 고도화)

Manim

사전 제작 (콘텐츠 라이브러리)



(유튜브/S3에 미리 업로드)

실시간 렌더링



(학생 문제에 맞춰 즉시 생성)

Meta-RAG

텍스트 해설 + 개념 ID 매칭



(e.g., "C-001 개념 영상 보세요")

시각화 JSON 생성



(Manim이 이해하는 애니메이션 설계도)

4축 모델

코치 수동 갱신 / 규칙 기반



(핵심 이력 데이터 축적)

AI 자동 갱신



(V1 데이터를 학습한 AI가 갱신)

배포 비용

매우 낮음 (Cloud Run + Cloud SQL)

높음 (실시간 GPU 렌더링 + 고성능 LLM)

7. MLOps: AI는 코치로부터 학습한다

이 시스템의 AI는 코치(전문가)의 피드백을 통해 성장합니다.

피드백 수집: 코치가 AI의 판단(e.g., Anki 카드 생성 승인/거절)에 대해 '좋음/나쁨' 피드백을 LLM_Log에 기록합니다. [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/backend/llm_filter.py]

데이터셋 추출: export_finetuning_data.py 스크립트가 이 피드백을 '정답 데이터셋'으로 추출합니다. [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/scripts/export_finetuning_data.py]

모델 재학습: 이 데이터셋을 사용하여 Meta-RAG 엔진을 파인튜닝(Fine-tuning)합니다. [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/.github/workflows/ml_pipeline.yml]

A/B 테스트: 코치도 모르게 신규 AI(B)와 기존 AI(A)를 일부 학생에게 배포하여, 코치로부터 '좋음' 피드백을 더 많이 받는 모델을 정식 채택합니다. [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/docs/v2/AB_TESTING_STRATEGY.md]

8. [Appendix] 통합 데이터베이스 명세

(이전 대화에서 제안한 통합 데이터베이스 명세가 여기에 포함됩니다.)

Students (학생 기본 정보)

Coaches (코치 기본 정보)

Parents (학부모 기본 정보)

student_parent_association (학생-학부모 관계)

Assessments (진단 이벤트)

Student_Vector_History (학생 잠재 공간 '이력') - 4축 모델 구현체

Concepts_Library (Manim 콘텐츠 라이브러리)

Submissions (학생 제출물)

Coach_Memos (코치 정성적 메모)

LLM_Logs (AI 판단 및 코치 피드백 로그)

Anki_Cards (학생용 Anki 카드)

Weekly_Reports (주간 리포트)

9. [Appendix] 통합 시퀀스 다이어그램

(이전 대화에서 제안한 통합 시퀀스 다이어그램이 여기에 포함됩니다.)

sequenceDiagram
    participant ST as 👨‍🎓 학생 (Web)
    participant CH as 👩‍🏫 코치 (Pacer)
    participant PA as 👨‍👩‍👧 학부모 (Kakao)
    participant API as 🖥️ 플랫폼 (Pacer API)
    participant MetaRag as 🧠 Meta-RAG (논리)
    participant Manim as 🎬 Manim (시각화)
    participant DB as 🗃️ 플랫폼 DB
    participant KAKAO as 📱 카카오 API

    Note over ST, KAKAO: (A) 평가 사이클: 4축 모델 '거시적' 갱신 (코치 주도)
    
    CH->>API: 1. 진단평가(시험) 등록 및 배포
    API-->>ST: 2. (알림) "진단평가가 도착했습니다."
    ST->>API: 3. 시험 응시 및 답안 제출
    
    API->>MetaRag: 4. (오답 문항) 원인 및 개념 분석 요청
    MetaRag-->>API: 5. (오답 원인) 논리/개념 분석 결과 (JSON)
    
    API->>API: 6. (내부) [4축 모델 종합 갱신] (시험 결과 + 오답 분석 기반)
    API->>DB: 7. `INSERT Assessment` (type: 'EXAM')
    API->>DB: 8. `INSERT Student_Vector_History` (4축 점수 갱신)
    API-->>CH: 9. (알림) "학생 4축 모델 갱신됨" (코칭 자료로 활용)

    Note over ST, KAKAO: (B) 일일 학습/코칭 사이클 (학생, 코치, AI 상호작용)

    par (B-1) 코치 주도 학습 (오프라인/1:1)
        CH->>API: 10. `[수업 중]` 학생 4축 모델(레이더 차트) 조회
        CH->>ST: 11. `[Offline]` 4축 모델 기반, 학생 취약점(e.g., axis2_piv) 직접 지도
        CH->>API: 12. `[수업 후]` 정성적 메모 및 [4축 모델 수동 갱신] (코치 판단)
        API->>DB: 13. `INSERT Coach_Memo`
        API->>DB: 14. `INSERT Assessment` (type: 'COACH_MANUAL')
        API->>DB: 15. `INSERT Student_Vector_History` (4축 점수 갱신)
    
    and (B-2) 학생 주도 학습 (AI 과제)
        ST->>API: 16. (과제) 문제 제출 (AI 풀이/시각화 요청)
        
        API->>MetaRag: 17. 사고 과정 생성 요청
        MetaRag-->>API: 18. 논리적 풀이 (JSON - {text: "...", concept_id: "C-001"})
        
        API->>DB: 19. `SELECT manim_data_path FROM Concepts_Library WHERE concept_id = 'C-001'`
        DB-->>API: 20. (Manim 시각화 데이터 경로 반환)

        API->>DB: 21. `INSERT Submission` (풀이 텍스트, Manim 경로 저장)
        API-->>ST: 22. 인터랙티브 풀이(텍스트 + 애니메이션) 제공
        
        ST->>API: 23. (풀이 확인 및 상호작용 로그 전송)
        API->>API: 24. (내부) [4축 모델 미세 조정] (로그 분석 기반)
        API->>DB: 25. `INSERT Assessment` (type: 'AI_ANALYSIS')
        API->>DB: 26. `INSERT Student_Vector_History` (4축 점수 미세 갱신)
    end

    Note over ST, KAKAO: (C) 리포팅 및 MLOps 사이클
    
    (리포팅 및 학부모 발송 플로우 ...)
    (AI 모델 개선 플로우 ...)

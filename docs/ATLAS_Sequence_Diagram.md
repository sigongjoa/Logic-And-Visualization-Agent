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
    
    API->>API: 6. (내부) **[4축 모델 종합 갱신]** (시험 결과 + 오답 분석 기반)
    API->>DB: 7. `INSERT Assessment` (type: 'EXAM')
    API->>DB: 8. **`INSERT Student_Vector_History` (4축 점수 갱신)**
    API-->>CH: 9. (알림) "학생 4축 모델 갱신됨" (코칭 자료로 활용)

    Note over ST, KAKAO: (B) 일일 학습/코칭 사이클 (학생, 코치, AI 상호작용)

    par (B-1) 코치 주도 학습 (오프라인/1:1)
        CH->>API: 10. `[수업 중]` 학생 4축 모델(레이더 차트) 조회
        CH->>ST: 11. **`[Offline]`** 4축 모델 기반, 학생 취약점(e.g., axis2_piv) 직접 지도
        CH->>API: 12. `[수업 후]` 정성적 메모 및 **4축 모델 수동 갱신** (코치 판단)
        API->>DB: 13. `INSERT Coach_Memo`
        API->>DB: 14. `INSERT Assessment` (type: 'COACH_MANUAL')
        API->>DB: 15. **`INSERT Student_Vector_History` (4축 점수 갱신)**
    
    and (B-2) 학생 주도 학습 (AI 과제)
        ST->>API: 16. (과제) 문제 제출 (AI 풀이/시각화 요청)
        API->>MetaRag: 17. 사고 과정 생성 요청
        MetaRag-->>API: 18. 논리적 풀이 (JSON)
        API->>Manim: 19. 시각화 데이터 생성 요청
        Manim-->>API: 20. 시각화 데이터 (JSON)
        API->>DB: 21. `INSERT Submission` (풀이, 시각화 데이터 저장)
        API-->>ST: 22. 인터랙티브 풀이(애니메이션) 제공
        
        ST->>API: 23. (풀이 확인 및 상호작용 로그 전송)
        
        par (내부) 4+1축 모델 동시 갱신
            API->>API: 24a. (역량 분석) **[4축 모델 미세 조정]**
            API->>DB: 25a. `INSERT Assessment` (type: 'AI_ANALYSIS')
            API->>DB: 26a. **`INSERT Student_Vector_History` (4축 점수 미세 갱신)**
        and
            API->>API: 24b. (진도 분석) **[커리큘럼 축 갱신]**
            API->>DB: 25b. `UPDATE Student_Mastery` (concept_id='C-001', score=70)
        end
    end

    Note over ST, KAKAO: (C) 리포팅 사이클 (코치 -> 학부모)

    API->>API: 27. `[주 1회]` 주간 리포트 초안 자동 생성
    API->>DB: 28. (이번 주 4축 모델 변화량, 활동 내역, 코치 메모 등 모두 조회)
    API->>DB: 29. `INSERT Weekly_Report` (status: `DRAFT`)
    API-->>CH: 30. (알림) "주간 리포트 초안 검토 필요"

    CH->>API: 31. 리포트 초안 검토 (AI요약 + **4축 변화 차트**)
    CH->>API: 32. **최종 코멘트 작성 및 승인** (PUT /report/{id}/finalize)
    API->>DB: 33. `UPDATE Weekly_Report` (status: `FINALIZED`)

    API->>KAKAO: 34. 카카오톡 발송 요청 (Pacer의 kakao_sender.py)
    KAKAO-->>PA: 35. **학부모에게 최종 리포트(4축 차트 포함) 발송**
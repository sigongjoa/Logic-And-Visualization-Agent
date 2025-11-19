Project: ATLAS - 통합 데이터베이스 명세서 (V1)

이 문서는 'Project: ATLAS' V1의 핵심 데이터를 저장하는 PostgreSQL (또는 MySQL) 데이터베이스 스키마를 정의합니다.

1. 사용자 및 관계 테이블

학생, 코치, 학부모의 기본 정보와 관계를 정의합니다.

1.1. Students (학생 기본 정보)

학생 개개인을 식별하는 기본 테이블입니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| student_id | VARCHAR(50) | PK | 학생 고유 ID (e.g., std_kimminjun) |
| student_name | VARCHAR(100) | NOT NULL | 학생 이름 |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | 계정 생성일 |

1.2. Coaches (코치 기본 정보)

| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| coach_id | VARCHAR(50) | PK | 코치 고유 ID (e.g., coach_sigongjoa) |
| coach_name | VARCHAR(100) | NOT NULL | 코치 이름 |

1.3. Parents (학부모 기본 정보)

| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| parent_id | SERIAL | PK | 학부모 고유 ID (Auto-Increment) |
| parent_name | VARCHAR(100) | NOT NULL | 학부모 이름 |
| kakao_user_id | VARCHAR(255) | UNIQUE, NULL | 카카오톡 발송을 위한 고유 ID [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/backend/kakao_sender.py] |

1.4. student_coach_relation (학생-코치 관계)

한 학생이 여러 코치에게, 한 코치가 여러 학생을 관리할 수 있는 M:N 관계
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| student_id | VARCHAR(50) | PK, FK (Students) | 학생 ID |
| coach_id | VARCHAR(50) | PK, FK (Coaches) | 코치 ID |

1.5. student_parent_association (학생-학부모 관계)

| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| student_id | VARCHAR(50) | PK, FK (Students) | 학생 ID |
| parent_id | INT | PK, FK (Parents) | 학부모 ID |

2. 🧠 4+1축 학생 모델 테이블

학생의 '학습 역량(How)'을 측정하는 **4축 잠재 공간 모델**과 '학습 진도(What)'를 추적하는 **커리큘럼 축**을 정의합니다.

2.1. Assessments (진단 이벤트)

4축 모델이 "왜" 갱신되었는지 그 '이유'와 '근거'를 기록합니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| assessment_id | VARCHAR(50) | PK | 진단 이벤트 고유 ID (e.g., asmt_abc123) |
| student_id | VARCHAR(50) | FK (Students), NOT NULL | 대상 학생 |
| assessment_date | TIMESTAMPTZ | NOT NULL, DEFAULT now()| 진단(갱신)이 수행된 날짜 |
| assessment_type| VARCHAR(20) | NOT NULL | 진단 종류 (EXAM, COACH_MANUAL, AI_ANALYSIS) |
| source_ref_id | VARCHAR(50) | NULL | 이 진단의 근거 ID (e.g., submission_id 또는 exam_id) |
| notes | TEXT | NULL | 진단에 대한 추가 메모 (e.g., "코치가 2축 점수 수동 조정") |
| ai_model_version | VARCHAR(50) | NULL | [V2] 진단에 사용된 AI 모델 버전 |
| ai_reason_code | VARCHAR(50) | NULL | [V2] AI 진단 근거 코드 |

2.2. Student_Vector_History (학생 잠재 공간 '이력')

4축 모델의 모든 변경 이력을 차곡차곡 쌓아 학생의 성장 곡선을 그립니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| vector_id | VARCHAR(50) | PK | 진단 벡터 고유 ID (e.g., vec_kimminjun_v1) |
| assessment_id| VARCHAR(50) | FK (Assessments), NOT NULL | 이 벡터를 생성한 진단 이벤트 |
| student_id | VARCHAR(50) | FK (Students), NOT NULL | 대상 학생 |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now()| 이 벡터가 생성(기록)된 시간 |
| axis1_geo | TINYINT | NOT NULL, CHECK(0-100) | (축1) 인지 기저: 기하 (0-100) |
| axis1_alg | TINYINT | NOT NULL, CHECK(0-100) | (축1) 인지 기저: 대수 (0-100) |
| axis1_ana | TINYINT | NOT NULL, CHECK(0-100) | (축1) 인지 기저: 해석 (0-100) |
| axis2_opt | TINYINT | NOT NULL, CHECK(0-100) | (축2) 메타인지: 최적화 (0-100) |
| axis2_piv | TINYINT | NOT NULL, CHECK(0-100) | (축2) 메타인지: 피벗 (0-100) |
| axis2_dia | TINYINT | NOT NULL, CHECK(0-100) | (축2) 메타인지: 자가 진단 (0-100) |
| axis3_con | TINYINT | NOT NULL, CHECK(0-100) | (축3) 지식 상태: 개념적 지식 (0-100) |
| axis3_pro | TINYINT | NOT NULL, CHECK(0-100) | (축3) 지식 상태: 절차적 지식 (0-100) |
| axis3_ret | TINYINT | NOT NULL, CHECK(0-100) | (축3) 지식 상태: 인출 속도 (0-100) |
| axis4_acc | TINYINT | NOT NULL, CHECK(0-100) | (축4) 실행 지구력: 연산 정확성 (0-100) |
| axis4_gri | TINYINT | NOT NULL, CHECK(0-100) | (축4) 실행 지구력: 난이도 내성 (0-100) |

3. 🗺️ 지식 그래프 및 커리큘럼 축 테이블

커리큘럼을 '지식 지도'로 정의하고, 학생의 '지도 정복 상태'를 추적합니다.

3.1. Curriculums (커리큘럼 정보)

(e.g., '중등 수학(상)', '수학 I', '미적분')
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| curriculum_id | VARCHAR(50) | PK | 커리큘럼 ID (e.g., MATH-01) |
| curriculum_name | VARCHAR(100) | NOT NULL | 커리큘럼 이름 (e.g., "중등 수학(상)") |
| description | TEXT | | |

3.2. Concepts_Library (개념 노드)

기존 명세서의 Concepts_Library를 '커리큘럼'과 연결합니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| concept_id | VARCHAR(50) | PK | 개념 ID (e.g., C-001) |
| curriculum_id | VARCHAR(50) | FK (Curriculums) | 이 개념이 속한 커리큘럼 |
| concept_name | VARCHAR(100) | NOT NULL | 개념 이름 (e.g., "근의 공식") |
| manim_data_path | VARCHAR(255) | | (V1) Manim 콘텐츠 경로 |
| description | TEXT | NULL | 개념에 대한 간단한 설명 |

3.3. Concept_Relations (개념 관계: 지식 그래프)

(e.g., '근의 공식'을 배우려면 '이차방정식'을 알아야 한다)
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| relation_id | SERIAL | PK | |
| from_concept_id | VARCHAR(50) | FK (Concepts_Library) | (e.g., '근의 공식') |
| to_concept_id | VARCHAR(50) | FK (Concepts_Library) | (e.g., '이차방정식') |
| relation_type | VARCHAR(20) | | 관계 (e.g., REQUIRES, EXPANDS) |

3.4. Student_Mastery (학생별 개념 숙련도)

이 테이블이 '커리큘럼 축'의 실체입니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| student_id | VARCHAR(50) | PK, FK (Students) | 학생 ID |
| concept_id | VARCHAR(50) | PK, FK (Concepts_Library) | 개념 ID |
| mastery_score | TINYINT | NOT NULL, CHECK(0-100) | 숙련도 점수 (0~100) |
| status | VARCHAR(20) | | 상태 (e.g., NOT_STARTED, IN_PROGRESS, MASTERED) |
| last_updated | TIMESTAMPTZ | | 마지막 갱신일 |

4. 📚 학습/코칭 활동 테이블

V1 전략(텍스트 해설 + 콘텐츠 라이브러리)을 지원합니다.

4.1. Submissions (학생 제출물)

학생의 학습 활동(AI 과제)과 AI의 분석 결과를 저장하는 핵심 연결고리입니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| submission_id | VARCHAR(50) | PK | 제출 고유 ID (e.g., sub_xyz789) |
| student_id | VARCHAR(50) | FK (Students), NOT NULL | 제출한 학생 |
| submitted_at | TIMESTAMPTZ | NOT NULL, DEFAULT now()| 제출 시간 |
| problem_text | TEXT | | 학생이 제출한 원본 문제 |
| status | VARCHAR(20) | NOT NULL | 처리 상태 (RECEIVED, COMPLETE, ERROR) |
| logical_path_text| TEXT | NULL | [Meta-RAG 결과] 텍스트 해설 |
| concept_id | VARCHAR(50) | FK (Concepts_Library), NULL| [Meta-RAG 결과] AI가 식별한 관련 개념 ID |
| student_answer | TEXT | NULL | 학생의 최종 답안 (진단평가용) |
| audio_explanation_url | VARCHAR(255) | NULL | [V2] Fish Speech로 생성된 음성 해설 URL |
| manim_visualization_json | TEXT | NULL | [V2] Manim 시각화 데이터 (JSON) |

4.2. Coach_Memos (코치 정성적 메모)

코치님이 오프라인에서 관찰한 내용을 기록합니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| memo_id | SERIAL | PK | 메모 ID (Auto-Increment) |
| coach_id | VARCHAR(50) | FK (Coaches), NOT NULL | 작성한 코치 |
| student_id | VARCHAR(50) | FK (Students), NOT NULL | 대상 학생 |
| memo_text | TEXT | NOT NULL | (e.g., "피벗 사고 훈련에 집중함") |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now()| 작성 시간 |

5. 📈 MLOps 및 리포팅 테이블

코치의 피드백(AI 개선용)과 학부모 리포트(발송용)를 관리합니다.

5.1. LLM_Logs (AI 판단 및 코치 피드백 로그)

Pacer의 Anki 카드 생성 판단 등, AI의 세부 결정을 기록하고 코치의 피드백을 받습니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| log_id | SERIAL | PK | 로그 ID |
| source_submission_id| VARCHAR(50) | FK (Submissions), NULL | 이 판단의 근거가 된 제출물 |
| decision | VARCHAR(50) | NOT NULL | AI의 결정 (e.g., APPROVE_ANKI) |
| model_version | VARCHAR(50) | | 판단에 사용된 AI 모델 버전 (A/B 테스팅용) [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/docs/v2/AB_TESTING_STRATEGY.md] |
| coach_feedback | VARCHAR(10) | NULL | 코치의 피드백 (GOOD 또는 BAD) |
| reason_code | VARCHAR(50) | NULL | 피드백 사유 (e.g., SIMPLE_MISTAKE) |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now()| 로그 생성 시간 |

5.2. Anki_Cards (학생용 Anki 카드)

| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| card_id | SERIAL | PK | 카드 ID |
| student_id | VARCHAR(50) | FK (Students), NOT NULL | 카드 소유 학생 |
| llm_log_id | INT | FK (LLM_Logs), NOT NULL | 이 카드를 생성시킨 AI 판단 로그 |
| question | TEXT | NOT NULL | Anki 질문 (AI 생성) |
| answer | TEXT | NOT NULL | Anki 답변 (AI 생성) |
| next_review_date | DATE | NOT NULL | 다음 복습 예정일 (SM2 알고리즘) [cite: sigongjoa/pacer/pacer-a60f66786b01de22ec2291ec871c4f9328d9cf73/backend/anki_engine.py] |
| repetitions | INT | NOT NULL, DEFAULT 0 | (SM2) 반복 횟수 |
| ease_factor | FLOAT | NOT NULL, DEFAULT 2.5 | (SM2) 용이성 계수 |
| interval_days | INT | NOT NULL, DEFAULT 0 | (SM2) 다음 복습 간격(일) |

5.3. Weekly_Reports (주간 리포트)

학부모에게 발송될 리포트의 최종본을 관리합니다.
| 필드명 | 데이터 타입 | 제약 | 설명 |
| :--- | :--- | :--- | :--- |
| report_id | SERIAL | PK | 리포트 ID |
| student_id | VARCHAR(50) | FK (Students), NOT NULL | 대상 학생 |
| coach_id | VARCHAR(50) | FK (Coaches), NULL | 최종 승인한 코치 |
| period_start | DATE | NOT NULL | 리포트 기간 (시작) |
| period_end | DATE | NOT NULL | 리포트 기간 (종료) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'DRAFT' | 상태 (DRAFT, FINALIZED, SENT) |
| ai_summary | TEXT | NULL | AI가 생성한 4축 모델 변화 요약 |
| vector_start_id| VARCHAR(50) | FK (Student_Vector_History)| 기간 시작 시점의 학생 벡터 ID |
| vector_end_id | VARCHAR(50) | FK (Student_Vector_History)| 기간 종료 시점의 학생 벡터 ID |
| coach_comment | TEXT | NULL | 코치님이 작성한 최종 종합 코멘트 |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now()| 초안 생성 시간 |
| finalized_at | TIMESTAMPTZ | NULL | 코치 최종 승인 시간 |
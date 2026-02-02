LLM Prompting 기법 비교 보고서

1. 실험 결과 요약

1.1 정답률 비교표

| Prompting 기법 | 0-shot | 3-shot | 5-shot | 평균 |
|---------------|--------|--------|--------|------|
| Direct Prompting | 0.82 (82%) | 0.84 (84%) | 0.78 (78%) | 81.3% |
| CoT Prompting | 0.74 (74%) | 0.82 (82%) | 0.82 (82%) | 79.3% |
| My Prompting | 0.84 (84%) | 0.86 (86%) | 0.86 (86%) | 85.3% |

1.2 주요 관찰사항

1. 0-shot 성능: Direct Prompting과 My Prompting이 82%와 84%로 높은 성능을 보였습니다. CoT Prompting은 74%로 상대적으로 낮은 성능을 보였습니다.

2. Few-shot 효과: 
   - Direct Prompting: 3-shot에서 84%로 향상되었으나, 5-shot에서 78%로 하락 (82% → 84% → 78%)
   - CoT Prompting: Few-shot 예시가 성능을 크게 향상시킴 (74% → 82% → 82%)
   - My Prompting: Few-shot 예시가 성능을 지속적으로 향상시킴 (84% → 86% → 86%)

3. 전체 평균: My Prompting이 85.3%로 가장 높은 평균 성능을 보였습니다. Direct Prompting은 81.3%, CoT Prompting은 79.3%를 기록했습니다.

4. 최고 성능: My Prompting이 3-shot과 5-shot에서 86%로 최고 성능을 달성했습니다.

---

2. CoT Prompting이 Direct Prompting에 비해 좋을 수 있는 이유

일반적으로 Chain-of-Thought (CoT) Prompting이 Direct Prompting보다 성능이 우수할 수 있는 이유는 다음과 같습니다:

2.1 단계별 추론 과정의 명시화

- Direct Prompting: 모델이 최종 답만 생성하도록 요구하여, 복잡한 수학 문제에서 중간 계산 과정을 생략하거나 잘못된 추론을 할 수 있습니다.
- CoT Prompting: 각 단계의 추론 과정을 명시적으로 보여주므로, 모델이 문제를 더 체계적으로 분해하고 해결할 수 있습니다.

2.2 오류 검출 및 수정 가능성

- CoT 방식에서는 각 단계의 결과를 확인할 수 있어, 중간 단계에서 발생한 오류를 식별하고 수정할 기회가 있습니다.
- Direct 방식은 최종 답만 제공하므로, 오류의 원인을 파악하기 어렵습니다.

2.3 복잡한 문제 해결 능력 향상

- 다단계 계산이 필요한 문제에서, CoT는 각 단계를 순차적으로 처리하도록 유도합니다.
- 예를 들어, "A를 계산한 후 B를 계산하고, 그 결과로 C를 계산"하는 문제에서 CoT는 각 단계를 명확히 구분하여 처리합니다.

2.4 Few-shot Learning의 효과 극대화

- Few-shot 예시에서 추론 과정을 보여주면, 모델이 유사한 패턴을 학습하여 새로운 문제에도 적용할 수 있습니다.
- Direct 방식은 답만 보여주므로, 문제 해결 방법론을 학습하기 어렵습니다.

2.5 본 실험에서의 관찰

- 본 실험에서는 0-shot에서 CoT가 74%로 Direct(82%)보다 낮은 성능을 보였지만, Few-shot 환경에서는 CoT가 82%로 향상되어 Direct와 유사하거나 더 나은 성능을 보였습니다.
- 이는 CoT가 Few-shot 예시를 통해 추론 패턴을 학습하는 데 효과적임을 보여줍니다.
- Direct Prompting의 경우 5-shot에서 성능이 하락(78%)한 것은 예시의 품질이나 형식이 중요함을 시사합니다.

---

3. My Prompting이 CoT에 비해 더 좋을 수 있는 이유

본인이 구현한 프롬프트 기법(DUP Method)이 기본 CoT보다 성능이 우수한 이유는 다음과 같습니다:

3.1 구조화된 3단계 접근법 (DUP Method)

My Prompting의 구조:
- Stage 1 [Core Question]: 문제의 핵심 목표를 명확히 추출
- Stage 2 [Info]: Stage 1과 관련된 모든 필수 정보를 나열
- Stage 3 [Answer]: Stage 1과 Stage 2의 정보를 활용하여 단계별로 해결

기본 CoT와의 차이:
- 기본 CoT: 추론 과정을 자연어로 기술하지만, 단계 구분이 모호할 수 있습니다.
- My Prompting: 각 단계를 명시적으로 구조화하여, 모델이 더 체계적으로 추론하도록 유도합니다.

3.2 문제 이해 단계의 명시화

- Core Question 추출: 문제를 해결하기 전에 먼저 핵심 목표를 명확히 파악하도록 강제합니다.
- 이는 모델이 문제의 본질을 이해하고, 불필요한 정보에 혼란스러워하지 않도록 돕습니다.

3.3 정보 수집 단계의 체계화

- Info 단계: 문제 해결에 필요한 모든 정보를 먼저 정리하도록 합니다.
- 이는 모델이 문제의 조건과 변수를 명확히 인식하고, 계산 과정에서 놓치는 정보가 없도록 보장합니다.

3.4 단계별 검증 가능성

- 각 단계가 명시적으로 구분되어 있어, 각 단계의 결과를 검증하기 쉽습니다.
- Core Question이 올바르게 추출되었는지, 필요한 정보가 모두 수집되었는지 확인할 수 있습니다.

3.5 최종 답 형식의 명확성

- "Final result format: #### [value]" 형식을 명시하여, 답 추출 함수가 정확하게 답을 파싱할 수 있도록 합니다.
- 이는 평가 과정에서의 오류를 줄이는 데 도움이 됩니다.

3.6 Few-shot 예시의 일관성

- 모든 예시에서 동일한 구조(Stage 1 → Stage 2 → Stage 3)를 사용하여, 모델이 일관된 패턴을 학습하도록 합니다.
- 특히 3-shot과 5-shot에서 86%의 성능을 달성한 것은 구조화된 접근법의 효과를 보여줍니다.

3.7 본 실험에서의 관찰

- My Prompting은 모든 shot 설정에서 우수한 성능을 보였습니다:
  - 0-shot: 84% (Direct와 유사, CoT보다 10%p 높음)
  - 3-shot: 86% (모든 방법 중 최고)
  - 5-shot: 86% (모든 방법 중 최고)
- 평균 성능 85.3%로 모든 방법 중 가장 높음
- Few-shot 예시가 증가할수록 성능이 향상되고 안정화되는 경향을 보입니다.

---

4. 실험 방법론

4.1 데이터셋
- GSM8K: 초등학교 수준의 수학 단어 문제 데이터셋
- 테스트 샘플 수: 각 프롬프트 기법별 50개

4.2 모델
- 모델: llama-3.1-8b-instant (Groq API 사용)
- Temperature: 0.3
- Max Tokens: 128

4.3 평가 지표
- 정답률 (Accuracy): 예측 답과 정답의 차이가 1e-5 미만인 경우 정답으로 간주

4.4 프롬프트 기법 상세

Direct Prompting
- 최종 답만 생성하도록 요구
- Few-shot 예시에서 답만 제공
- 지시사항: "Solve these. The answer format might vary. Sometimes use numbers, sometimes words."
- 예시 형식: "Q1: question\nResult: answer (maybe)"

CoT Prompting
- 단계별 추론 과정을 포함
- Few-shot 예시에서 전체 풀이 과정 제공
- 지시사항: "Solve the problem step by step. End with #### [value]"
- 0-shot: "Question:\n{question}\nAnswer:"

My Prompting (DUP Method)
- 3단계 구조화된 접근법
- Stage 1: Core Question 추출
- Stage 2: 필요한 정보 수집
- Stage 3: 단계별 계산 및 답 도출
- "Final result format: #### [value]" 형식 명시

---

5. 결론

본 실험을 통해 다음을 확인할 수 있었습니다:

5.1 주요 발견사항

1. My Prompting의 우수성: 
   - 평균 성능 85.3%로 모든 방법 중 가장 높음
   - 3-shot과 5-shot에서 86%로 최고 성능 달성
   - 0-shot에서도 84%로 Direct와 유사한 최고 성능

2. Few-shot Learning의 효과: 
   - Direct Prompting: 3-shot에서 향상(84%)했으나 5-shot에서 하락(78%) - 예시 품질의 중요성 시사
   - CoT Prompting: Few-shot 예시가 성능을 크게 향상시킴 (74% → 82% → 82%)
   - My Prompting: Few-shot 예시가 성능을 지속적으로 향상시킴 (84% → 86% → 86%)

3. 구조화된 프롬프트의 중요성: 
   - My Prompting이 모든 shot 설정에서 우수한 성능을 보인 것은 단계를 명시적으로 구조화하고 일관된 형식을 사용하는 것이 성능 향상에 도움이 됨을 보여줍니다.
   - 특히 3단계 접근법(Core Question → Info → Answer)이 모델의 추론 과정을 체계화하는 데 효과적입니다.

4. 0-shot vs Few-shot: 
   - Direct Prompting은 0-shot과 3-shot에서 우수하지만 5-shot에서 성능이 하락
   - CoT Prompting은 0-shot에서 낮지만 Few-shot에서 크게 향상됨
   - My Prompting은 0-shot에서도 우수하고 Few-shot에서 더욱 향상됨

5.2 실용적 시사점

- 문제 복잡도에 따른 선택: 
  - 간단한 문제에서는 Direct Prompting이 효과적일 수 있지만, 복잡한 다단계 문제에서는 구조화된 방법(My Prompting)이 더 효과적입니다.

- Few-shot 예시의 품질: 
  - Direct Prompting에서 5-shot이 성능을 저하시킨 것은 예시의 품질이나 형식이 중요함을 보여줍니다.
  - 구조화된 프롬프트(My Prompting)는 Few-shot 예시를 더 효과적으로 활용합니다.

- 구조화의 균형: 
  - 과도한 구조화는 모델의 자유도를 제한할 수 있지만, 적절한 구조화(3단계 접근법)는 성능 향상에 도움이 됩니다.

- 실무 적용: 
  - My Prompting의 DUP Method는 실제 문제 해결에 적용하기 쉬운 구조화된 접근법을 제공합니다.
  - Core Question → Info → Answer의 3단계 구조는 다양한 도메인에 적용 가능합니다.

# CAR MASTER — Automotive Visual Vocabulary

현대자동차 공식 Owner's Manual을 1차 출처로 사용하는 500개 자동차 Visual Vocabulary 프로젝트입니다.

## START HERE — ChatGPT / Work 공용

둘 다 아래 파일을 같은 순서로 읽고 작업합니다.

1. `WORK_QUEUE.md` — 현재 작업·규칙·인수인계
2. `data/master.json` — 확정/후보 용어와 영구 ID
3. `data/id_registry.json` — 0001–0500 전체 영구 ID 선점표
4. `data/source_registry.json` — PDF URL + 공식 웹 매뉴얼 URL + 이미지 키 + GitHub 추출 이미지 경로 공용 레지스트리
5. `data/progress.json` — 실제 완료율

## 절대 중단 금지 규칙

한 환경에서 특정 PDF나 웹 이미지를 직접 열 수 없다는 이유만으로 작업을 중단하지 않습니다.

- PDF를 못 열면 `source_registry.json`의 official web manual URL / image key를 사용합니다.
- 웹 이미지를 직접 못 가져오면 PDF의 embedded image를 추출합니다.
- Work가 이미지를 추출하면 GitHub `images/`에 저장하고 `repo_asset` 경로를 `source_registry.json`에 기록합니다.
- 이후 Chat과 Work 모두 GitHub의 동일한 자산/링크를 사용합니다.
- 외부 링크가 죽으면 기존 출처를 삭제하지 말고 alternate source를 추가합니다.
- 자료 접근 문제는 `REVIEW` 사유가 될 수 있지만 작업 중단 사유가 될 수는 없습니다. 다른 공식 소스 또는 GitHub 자산으로 계속 진행합니다.

## ID 규칙

`0001`부터 `0500`까지 이미 모두 영구 선점되어 있습니다. 용어가 아직 비어 있어도 ID는 존재하며, 삭제·재번호·재사용하지 않습니다.

## 현재 상태

실제 완료율은 `data/progress.json`을 기준으로 합니다. 용어 조사 완료와 이미지/앱 반영 완료는 별도로 취급합니다.

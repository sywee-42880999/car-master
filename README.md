# CAR MASTER — Serverless PWA v0.1

## 현재 구현
- LEVEL 1 · SUV Exterior Learn
- 현대 공식 매뉴얼 기준 용어 / Industry Term 구분
- 학습 진행도 및 점수 localStorage 저장
- 미니 테스트
- PWA Service Worker
- 외부 이미지 URL을 사용하지 않음

## 이미지 넣는 법
현대자동차 한국 공식 페이지에서 사용 허가 범위에 맞게 이미지를 로컬 저장한 뒤:
`images/hyundai/tucson/exterior-side.jpg`
로 넣으면 자동 적용됩니다.

권장 트리밍:
- 16:9
- 차체가 가로폭 약 80~90%
- 측면/3Q에서 파트 경계가 선명한 컷
- 광고성 배경보다 360VR/스튜디오 이미지 우선

## 실행
보안 정책상 service worker/PWA는 file://보다 로컬 HTTP에서 안정적입니다.
Python이 있으면 폴더에서:
`python -m http.server 8080`
브라우저에서 `http://localhost:8080`

점수 서버는 필요하지 않습니다. 브라우저에 저장됩니다.

## 다음 확장
1. SUV Interior
2. SUV Exterior + Interior Test
3. Sedan Exterior / Interior
4. SUV + Sedan Mix Test
5. Commercial
6. Hyundai / Kia / Genesis Model Quiz


## v0.2 Mobile improvements
- iPhone / Android responsive layout
- Full-width learning image
- 54px touch-friendly primary controls
- Swipe left/right on vehicle image to move between parts
- Mobile-only progress bar
- Sticky bottom learning controls
- Single-column quiz answers on narrow screens
- Learned part, current position, and score persist locally

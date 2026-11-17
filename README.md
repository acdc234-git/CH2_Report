# CH2_Report

AX 1기 CH2 · CH3 평가 과제 모음입니다.

| 폴더 | 과제 | 내용 |
| --- | --- | --- |
| [`DATABASE_AI/`](DATABASE_AI/) | 데이터베이스 & AI 활용 | Supabase + FastAPI 로 회원·상품·주문 3개 테이블 CRUD 구현 |
| [`CloneCoding/`](CloneCoding/) | 프론트엔드 — 클론 코딩 | 스파르타 PRO CAMP 랜딩 페이지 HTML + CSS 클론 |
| [`ToDoList/`](ToDoList/) | 프론트엔드 — Todo 리스트 | 바닐라 JavaScript 로 추가·조회·수정·삭제 구현 |

## 데이터베이스 & AI 활용

테이블 구조(PK·FK)와 CRUD 동작 화면은
**[`DATABASE_AI/README.md`](DATABASE_AI/README.md)** 에 정리돼 있습니다.

- 테이블: `members` · `products` · `orders`
- API: 테이블당 5개씩 총 15개 (FastAPI · Swagger UI)
- DDL: [`DATABASE_AI/sql/schema.sql`](DATABASE_AI/sql/schema.sql)

## 클론 코딩 (HTML + CSS)

구현 화면(전체 · 헤더 · 메인 · 푸터) 캡처는
**[`CloneCoding/README.md`](CloneCoding/README.md)** 에 있습니다.

- 대상: 재직자용 실무 실습 캠프 (PRO CAMP) 랜딩 페이지
- 구성: 헤더 / 히어로 · 트랙 카드 · 수료생 후기 / 푸터
- 반응형: 820px 미디어쿼리

## Todo 리스트 (JavaScript)

기능 설명과 화면은 **[`ToDoList/README.md`](ToDoList/README.md)** 에 있습니다.

- 추가 · 조회(필터) · 수정 · 삭제 전부 동작
- 완료 토글, 남은 개수 표시, `localStorage` 저장
- 파일: `index.html` · `css/style.css` · `js/todo.js`

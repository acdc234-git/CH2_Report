# Next.js Todo — 회원 전용 할 일 관리

바닐라 JS 로 만들었던 Todo 리스트를 Next.js 기반으로 다시 만들고,
회원가입·로그인을 붙여 **회원마다 자기 할 일만** 보이도록 구현한 과제입니다.

- **배포 주소**: (Vercel URL 을 여기에 적습니다)
- **스택**: Next.js 16 (App Router) · React 19 · TypeScript · Tailwind · Supabase

## 주요 기능

| 영역 | 기능 |
| --- | --- |
| 회원 | 회원가입, 로그인, 로그아웃 |
| 할 일 | 등록, 목록 조회, 상세 조회, 상태 변경(READY / PROGRESS / DONE) |
| | 소프트 삭제(`deleted_at`), 고정(pin) |
| 보안 | 세션 미들웨어로 보호, RLS 로 본인 데이터만 접근 |

## 실행 방법

```bash
# 1) 의존성 설치
npm install

# 2) 환경변수 — .env.local.example 을 .env.local 로 복사하고 값을 채운다
cp .env.local.example .env.local

# 3) Supabase 테이블 생성
#    SQL Editor 에 supabase/schema.sql 내용을 붙여넣고 실행
#    Authentication > Providers > Email > "Confirm email" 은 꺼 둔다

# 4) 개발 서버
npm run dev
```

## 데이터 구조

### profiles

`auth.users` 와 1:1. 로그인 정보는 Supabase Auth 가 관리하고, 이름 등 서비스 정보만 둡니다.

| 컬럼 | 타입 | 제약 |
| --- | --- | --- |
| `id` | uuid | **PK**, FK → `auth.users(id)` |
| `name` | text | NOT NULL |
| `created_at` | timestamptz | default now() |
| `updated_at` / `deleted_at` | timestamptz | nullable |

### todos

| 컬럼 | 타입 | 제약 |
| --- | --- | --- |
| `id` | uuid | **PK**, default `gen_random_uuid()` |
| `user_id` | uuid | **FK → profiles(id)**, NOT NULL |
| `user_name` | text | NOT NULL |
| `status` | text | `READY` / `PROGRESS` / `DONE` |
| `title` · `content` | text | NOT NULL |
| `created_at` | timestamptz | default now() |
| `updated_at` / `deleted_at` | timestamptz | nullable |

전체 DDL 과 RLS 정책은 [`supabase/schema.sql`](supabase/schema.sql) 에 있습니다.

### 접근 제어 (RLS)

두 테이블 모두 RLS 를 켜고 `auth.uid()` 기준 정책을 걸었습니다.
로그인한 회원은 **자기 행만** 조회·생성·수정·삭제할 수 있습니다.

```sql
create policy "본인 할일 조회" on public.todos
    for select using (auth.uid() = user_id);
```

서버 코드에서도 `.eq('user_id', user.id)` 로 한 번 더 거르지만,
DB 제약으로도 막혀 있어 코드에 실수가 있어도 남의 데이터가 새지 않습니다.

## 폴더 구조

```
todo/
├── app/                      # 라우트 (App Router)
│   └── (todo)/               #   메인, sign_in, sign_up, todo/*
├── domains/
│   ├── auth/                 # 회원 — actions · components · queries
│   └── todo/                 # 할 일 — actions · components · queries · store
├── shared/                   # 공통 UI·유틸·Supabase 클라이언트
├── supabase/schema.sql       # 테이블 DDL + RLS
└── middleware.ts             # 세션 갱신
```

도메인별로 폴더를 나눠 `actions`(쓰기) / `queries`(읽기) / `components` / `types` 를 같은 자리에 모았습니다.

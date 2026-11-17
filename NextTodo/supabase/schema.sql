-- =========================================================
-- Next.js Todo — Supabase 스키마
-- Supabase 대시보드 > SQL Editor 에 붙여넣고 Run
-- =========================================================
-- 전제: Authentication > Providers > Email 에서
--       "Confirm email" 을 꺼 두어야 합니다.
--       (켜져 있으면 회원가입 직후 세션이 없어 profiles insert 가 막힙니다)

-- ---------- 회원 프로필 ----------
-- auth.users 와 1:1. 로그인 정보는 Supabase Auth 가 관리하고
-- 이름 등 서비스 정보만 여기에 둡니다.
create table if not exists public.profiles (
    id         uuid        primary key references auth.users(id) on delete cascade,
    name       text        not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz,
    deleted_at timestamptz
);

-- ---------- 할 일 ----------
create table if not exists public.todos (
    id         uuid        primary key default gen_random_uuid(),
    user_id    uuid        not null references public.profiles(id) on delete cascade,
    user_name  text        not null,
    status     text        not null default 'READY'
                           check (status in ('READY', 'PROGRESS', 'DONE')),
    title      text        not null,
    content    text        not null default '',
    created_at timestamptz not null default now(),
    updated_at timestamptz,
    deleted_at timestamptz
);

create index if not exists todos_user_id_idx on public.todos (user_id);

-- =========================================================
-- RLS — 본인 데이터만 접근
-- =========================================================
alter table public.profiles enable row level security;
alter table public.todos    enable row level security;

-- profiles: 본인 것만 조회·생성·수정
drop policy if exists "본인 프로필 조회" on public.profiles;
create policy "본인 프로필 조회" on public.profiles
    for select using (auth.uid() = id);

drop policy if exists "본인 프로필 생성" on public.profiles;
create policy "본인 프로필 생성" on public.profiles
    for insert with check (auth.uid() = id);

drop policy if exists "본인 프로필 수정" on public.profiles;
create policy "본인 프로필 수정" on public.profiles
    for update using (auth.uid() = id);

-- todos: 본인 것만 조회·생성·수정·삭제
drop policy if exists "본인 할일 조회" on public.todos;
create policy "본인 할일 조회" on public.todos
    for select using (auth.uid() = user_id);

drop policy if exists "본인 할일 생성" on public.todos;
create policy "본인 할일 생성" on public.todos
    for insert with check (auth.uid() = user_id);

drop policy if exists "본인 할일 수정" on public.todos;
create policy "본인 할일 수정" on public.todos
    for update using (auth.uid() = user_id);

drop policy if exists "본인 할일 삭제" on public.todos;
create policy "본인 할일 삭제" on public.todos
    for delete using (auth.uid() = user_id);

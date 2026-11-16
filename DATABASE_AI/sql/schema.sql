-- 쇼핑몰 CRUD 과제 테이블 (Supabase SQL Editor 에 붙여넣어 실행)
-- 관계: members 1 ──< orders >── 1 products

create table if not exists members (
  id         bigserial    primary key,
  email      text         not null unique,
  name       text         not null,
  created_at timestamptz  not null default now()
);

create table if not exists products (
  id         bigserial    primary key,
  name       text         not null,
  price      integer      not null,
  stock      integer      not null default 0,
  created_at timestamptz  not null default now()
);

create table if not exists orders (
  id         bigserial    primary key,
  member_id  bigint       not null references members(id) on delete cascade,
  product_id bigint       not null references products(id),
  quantity   integer      not null default 1,
  created_at timestamptz  not null default now()
);

-- 과제용: anon 키로 조회가 되도록 RLS 를 끈다
alter table members  disable row level security;
alter table products disable row level security;
alter table orders   disable row level security;

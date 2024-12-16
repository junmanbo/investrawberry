#!/bin/bash

# DB 테이블 생성
alembic upgrade head

# ticker 데이터 생성
python3 ./input/ticker.py

# DB 체크
python3 app/initial_data.py
python3 app/backend_pre_start.py

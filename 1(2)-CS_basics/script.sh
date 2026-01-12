#!/usr/bin/env bash
export PATH="$HOME/miniconda3/bin:$PATH"

set -e

# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO
if ! command -v conda >/dev/null 2>&1; then
    MINICONDA_DIR="$HOME/miniconda3"
    INSTALLER="/tmp/Miniconda3-latest-Linux-x86_64.sh"

    if [ ! -d "$MINICONDA_DIR" ]; then
        wget -O "$INSTALLER" "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        bash "$INSTALLER" -b -p "$MINICONDA_DIR"
    fi

    export PATH="$MINICONDA_DIR/bin:$PATH"
fi

# conda를 스크립트에서 activate 가능하게 만들기
eval "$(conda shell.bash hook)"

# Conda 채널 ToS 자동 동의
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main >/dev/null 2>&1 || true
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r >/dev/null 2>&1 || true


# Conda 환경 생성 및 활성화
## TODO
if ! conda env list | awk '{print $1}' | grep -qx "myenv"; then
    conda create -y -n myenv python=3.10
fi

conda activate myenv


## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1
fi


# 필요한 패키지 설치
## TODO
python -m pip install --upgrade pip >/dev/null 2>&1
python -m pip install mypy >/dev/null 2>&1


# 출력 디렉토리 생성
mkdir -p output


# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    ## TODO
    num="${file%.py}"
    in_path="../input/${num}_input"
    out_path="../output/${num}_output"

    [ -f "$in_path" ]
    python "$file" < "$in_path" > "$out_path"
done

cd ..


# mypy 테스트 실행 및 mypy_log.txt 저장
## TODO
mypy submission > mypy_log.txt 2>&1


# conda.yml 파일 생성
## TODO
conda env export -n myenv > conda.yml


# 가상환경 비활성화
## TODO
conda deactivate

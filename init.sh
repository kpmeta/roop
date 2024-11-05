# checking the OS type and intalling python verison accordingly
# for macOS and linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Running on macOS"
    brew install python@3.11


elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Running on Linux"
    sudo apt update
    sudo apt install python3.11

# in case of other OS types 
else
    echo "Install python 3.10 manually"
fi

python3.10 -m venv ./venvs/python_3_10
source ./venvs/python_3_10/bin/activate
pip install -r requirements.txt
# To export pdf
install: pip install Pyrebase4
install xelatex: https://tug.org/mactex/mactex-download.html
## Hello QKD


create env:
```
python -m venv ./qkd-env
```
chosse env
```
source ./qkd-env/bin/activate
```

## install dep
```
%pip install xelatex
%pip install 'qiskit[visualization]'==1.3.0
%pip install qiskit_aer
%pip install qiskit_ibm_runtime
%pip install matplotlib
%pip install pylatexenc
%pip install qiskit-transpiler-service
%pip install ipykernel 
```

```
python3 main.py
```
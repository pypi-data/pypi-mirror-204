pip uninstall -y cfscanner &>/dev/null
rm dist/ -rf
python3 -m build &>/dev/null
pip install dist/cfscanner-1.3.*whl
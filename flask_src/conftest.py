"""
conftest.py — configuração do pytest.
Garante que flask_src está no path para os imports funcionarem.
"""
import sys
import os

# Adiciona flask_src ao path do Python
sys.path.insert(0, os.path.dirname(__file__))

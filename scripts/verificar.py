"""
Corre no PC as mesmas verificações que o CI (.github/workflows/ci.yml), pela mesma ordem
Para no primeiro passo que falhar
Correr a partir da raiz: python -m scripts.verificar
"""

import subprocess
import sys

# Os mesmos comandos e limites do ci.yml. Se o CI mudar, muda-se aqui também
PASSOS = [
    ("Pylint", ["pylint", "src/", "--fail-under=8.0"]),
    (
        "Testes e cobertura",
        ["pytest", "--cov=src", "--cov-branch", "--cov-report=term-missing", "--cov-fail-under=80"],
    ),
    ("Auditoria de dependências", ["pip_audit", "-r", "requirements.txt"]),
]


def main() -> int:
    for numero, (nome, argumentos) in enumerate(PASSOS, start=1):
        print(f"\n=== {numero}/{len(PASSOS)} {nome} ===", flush=True)
        # sys.executable é o python.exe do venv que corre este script:
        # como "python -m" que evita o bloqueio do Smart App Control
        # Os argumentos vão numa lista e sem shell=True, por isso nada passa por uma shell
        resultado = subprocess.run([sys.executable, "-m", *argumentos], check=False)
        if resultado.returncode != 0:
            print(f"\nFALHOU: {nome}. Os passos seguintes não correram.")
            return resultado.returncode
    print("\nTudo verde: o CI deve passar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

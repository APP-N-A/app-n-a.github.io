#!/usr/bin/env python3
"""
Gera o arquivo cofre.js do app "Teste de Saúde Mental e Emocional".

O conteúdo do teste (itens e áreas) fica cifrado com AES-256-GCM usando uma
chave-mestra aleatória. Cada acesso (login + senha) guarda uma cópia dessa
chave-mestra, cifrada com uma chave derivada do login e da senha por
PBKDF2-SHA256. Sem um login e senha válidos, o conteúdo não pode ser lido,
mesmo que alguém abra o arquivo cofre.js no GitHub.

Uso:
    pip install cryptography
    python3 gerar_cofre.py --conteudo conteudo.json --acessos acessos.json --saida ../cofre.js

acessos.json (guarde só com você, NÃO publique):
    [
      {"login": "irmandade", "senha": "minha-senha", "rotulo": "Acesso geral do grupo"}
    ]

Observação: cada execução gera uma nova chave-mestra. Quem marcou
"Manter conectado" em algum aparelho precisará entrar de novo.
"""
import argparse
import base64
import hashlib
import json
import os
import sys
import unicodedata

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERACOES = 310_000
PREFIXO_ID = "na-cofre-v1|"


def b64(dados: bytes) -> str:
    return base64.b64encode(dados).decode("ascii")


def normalizar_login(login: str) -> str:
    # Mesmo critério do app: sem espaços nas pontas, minúsculas, forma NFC.
    return unicodedata.normalize("NFC", login.strip()).lower()


def id_do_login(login_norm: str) -> str:
    return hashlib.sha256((PREFIXO_ID + login_norm).encode("utf-8")).hexdigest()[:32]


def derivar_chave(login_norm: str, senha: str, sal: bytes, iteracoes: int) -> bytes:
    material = (login_norm + "\u0000" + unicodedata.normalize("NFC", senha)).encode("utf-8")
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=sal, iterations=iteracoes)
    return kdf.derive(material)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--conteudo", required=True, help="conteudo.json (itens e áreas, texto puro)")
    p.add_argument("--acessos", required=True, help="acessos.json (logins e senhas, texto puro)")
    p.add_argument("--saida", default="cofre.js", help="arquivo de saída (padrão: cofre.js)")
    a = p.parse_args()

    with open(a.conteudo, encoding="utf-8") as f:
        conteudo = json.load(f)
    with open(a.acessos, encoding="utf-8") as f:
        acessos = json.load(f)

    # Conferências básicas do conteúdo
    itens = conteudo.get("itens", [])
    numeros = [i["n"] for i in itens]
    if numeros != list(range(1, len(itens) + 1)):
        print("Erro: os itens devem estar numerados em sequência a partir de 1.", file=sys.stderr)
        return 1
    ids_area = {ar["id"] for ar in conteudo.get("areas", [])}
    for i in itens:
        if i.get("area") not in ids_area:
            print(f"Erro: o item {i['n']} usa uma área inexistente: {i.get('area')}", file=sys.stderr)
            return 1

    if not acessos:
        print("Erro: informe pelo menos um acesso em acessos.json.", file=sys.stderr)
        return 1

    chave_mestra = AESGCM.generate_key(bit_length=256)
    iv = os.urandom(12)
    texto = json.dumps(conteudo, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    dados = AESGCM(chave_mestra).encrypt(iv, texto, None)

    vistos = set()
    lista = []
    for ac in acessos:
        login = normalizar_login(ac["login"])
        senha = ac["senha"]
        if not login or len(senha) < 6:
            print(f"Erro: login vazio ou senha com menos de 6 caracteres ({ac.get('login')!r}).", file=sys.stderr)
            return 1
        ident = id_do_login(login)
        if ident in vistos:
            print(f"Erro: login repetido: {login}", file=sys.stderr)
            return 1
        vistos.add(ident)
        sal = os.urandom(16)
        iv_ac = os.urandom(12)
        kek = derivar_chave(login, senha, sal, ITERACOES)
        chave_cifrada = AESGCM(kek).encrypt(iv_ac, chave_mestra, None)
        lista.append({
            "rotulo": ac.get("rotulo", ""),
            "id": ident,
            "sal": b64(sal),
            "iv": b64(iv_ac),
            "chave": b64(chave_cifrada),
        })

    linhas_acessos = ",\n".join("    " + json.dumps(x, ensure_ascii=False) for x in lista)
    saida = (
        "/* Cofre do app: conteúdo do teste cifrado (AES-256-GCM).\n"
        "   Gerado por ferramentas/gerar_cofre.py. Não edite o bloco \"conteudo\".\n"
        "   Para incluir um acesso novo sem refazer o cofre, use no app:\n"
        "   Mais > Administrar acessos > Gerar acesso, e cole a linha gerada\n"
        "   dentro da lista \"acessos\" abaixo (cada linha termina com vírgula). */\n"
        "window.COFRE = {\n"
        "  \"versao\": 1,\n"
        f"  \"iteracoes\": {ITERACOES},\n"
        f"  \"conteudo\": {{\"iv\": \"{b64(iv)}\", \"dados\": \"{b64(dados)}\"}},\n"
        "  \"acessos\": [\n"
        f"{linhas_acessos},\n"
        "  ]\n"
        "};\n"
    )
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(saida)
    print(f"Cofre gerado em {a.saida} com {len(lista)} acesso(s) e {len(itens)} itens.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

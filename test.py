import re

# Função para testar a substituição
def testar_substituicao(texto):
    # Expressão regular ajustada
    pattern = r"(?<![a-zA-Z])([78])\s?g\s?plus"
    # Substituição
    resultado = re.sub(pattern, r"\1 plus", texto)
    return resultado

# Testes com diferentes entradas
entradas = [
    "7 gplus",       # Entrada com espaço entre o número e "gplus"
    "7 g plus",      # Entrada com espaço antes e depois do "g"
    "8 gplus",       # Entrada sem espaço entre "g" e "plus"
    "8 g plus",      # Entrada com espaço antes e depois do "g"
    "7gplus",        # Entrada sem espaço entre "7" e "gplus"
    "7g plus",       # Entrada sem espaço entre "7" e "g" mas com espaço entre "g" e "plus"
    "6 gplus",       # Número fora do padrão (não deve substituir)
    "test 7 gplus",  # Texto com letras antes (não deve substituir)
]

resultados = [testar_substituicao(entrada) for entrada in entradas]
print(resultados)

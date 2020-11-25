# downsampling
Downsampling assignment

O programa gera a imagem reduzida com a porcentagem e modo especificado e a salva em um arquivo com o nome output_{mode}_{reduction}.png.

Bibliotecas utilizadas:
cv2 - utilizada para tratar a imagem
numpy - utilizada para fazer cálculo de média e mediana, também para criar a imagem de output (em forma de array)
scipy (stats) - utilizado para cálculo de moda
argparse - utilizado para tratar os argumentos de entrada

mode: mean, median ou mode
reduction: float (0.5 para redução de 50%)

Para usar:
python3 main.py [img.type] [mode] [reduction]

Exemplo:
python3 main.py exemplo.png mean 0.1

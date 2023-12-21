import sympy as sp

import matplotlib.pyplot as plt

import matplotlib.animation as animation

from matplotlib.widgets import Button

import numpy as np

'''
funções:
exponencial = sp.exp(t)

rampa = t
'''

t = sp.symbols('t')

s = sp.symbols('s')

qualidade = 1000 # Quanto maior for este valor, menos os gráficos oscilarão

tamanho_Porta = 5

tamanho_Porta2 = 5

velocidadeAnimacao = 0.05



def porta(valorInicial, valorFinal):
    
    return sp.Heaviside(t - valorInicial) - sp.Heaviside(t- valorFinal)


funcao1 = porta(0,tamanho_Porta)*6*sp.exp(-t)

funcao2 = porta(0,tamanho_Porta2)

# Uso da propriedade do produto no domínio de laplace ser igual a convolução no tempo

transformada = sp.laplace_transform(funcao1,t,s) 

transformada2 = sp.laplace_transform(funcao2,t,s) 

convolucao = transformada[0] * transformada2[0]

'''
"This function returns (F, a, cond) where F is the Laplace transform of f, 
a is the half-plane of convergence, and cond are auxiliary convergence conditions."

Ou seja, para realizar o produto entre as transformadas é necessário utilizar o índice 0 da transformada do SymPy.
'''

inversa = sp.inverse_laplace_transform(convolucao,s,t)

#definindo parâmetros para plotar os gráficos

raio = np.linspace(-1,100,qualidade) #assumindo que a amplitue esteja entre -1 e 100

amplitude = max(inversa.subs(t, i) for i in raio)

# Seção gráfica

fig, (ax,ax2) = plt.subplots(2,1)

ax.set_xlim(-3, (tamanho_Porta + tamanho_Porta2) + 2)

ax.set_ylim(-3, int(amplitude+2))

ax.grid(True)

x = np.linspace(-10,20,qualidade)

y = sp.lambdify(t, inversa, 'numpy') # lambdify converte uma função literal para uma função numérica

y2 = sp.lambdify(t, funcao1, 'numpy')

y3 = sp.lambdify(t, funcao2, 'numpy')

line, = ax.plot(x, y(x), color='blue', label = 'Convolução') # Definir y com lambidify me permite escrever y(x), fazendo com que x e y tenha o mesmo tamanho

ax.legend()

ax.set_title(r'$h(t) = f_1(t) * f_2(t)$')

ax.set_xlabel(r'$t$')

ax.set_ylabel(r'$h(t)$')


ax2.set_xlim(-1, (tamanho_Porta + tamanho_Porta2) + 2)

ax2.set_ylim(-2,int(amplitude + 2))

ax2.grid(True)

ax2.plot(x, y2(x), label = r'$f_1(t)$')

line2, =  ax2.plot(-x,y3(x), color = 'red', label = r'$f_2(t)$')

ax2.legend()

ax2.set_xlabel(r'$t$')

ax2.set_ylabel(r'$f(t)$')


# animacao

pause = False  

animacao = None


# botão pra pausar a animação

def on_click(event):

    global pause

    pause = not pause

    if pause:
        animacao.event_source.stop()
    
    else:
        animacao.event_source.start()

ax_botao = plt.axes([0.8, 0.01, 0.15, 0.05])  

botao = Button(ax_botao, 'Play | Pause', color='lightgoldenrodyellow', hovercolor='0.975')


botao.on_clicked(on_click)

def animate(i):

    global pause

    if not pause:

        x = np.linspace(0, i * velocidadeAnimacao, qualidade)

        x1 = np.linspace(0, 10, qualidade)

        line.set_data(x, y(x))

        line2.set_data(-x1 + (i * velocidadeAnimacao), y3(x))

        return line, line2,


animacao = animation.FuncAnimation(

    fig,

    animate,

    interval=50,

    blit=True,  

    save_count = 60 # número máximo de frames (o próprio interpretador recomenda ligar)
)

plt.show()


'''
Referências:

https://docs.sympy.org/latest/modules/integrals/integrals.html#sympy.integrals.transforms.laplace_transform

https://docs.sympy.org/latest/modules/integrals/integrals.html#sympy.integrals.transforms.inverse_laplace_transform

https://docs.sympy.org/latest/tutorials/intro-tutorial/basic_operations.html#lambdify

https://matplotlib.org/stable/gallery/animation/simple_scatter.html#sphx-glr-gallery-animation-simple-scatter-py

https://matplotlib.org/stable/gallery/animation/strip_chart.html#sphx-glr-gallery-animation-strip-chart-py

https://matplotlib.org/stable/gallery/event_handling/coords_demo.html

https://matplotlib.org/stable/gallery/event_handling/keypress_demo.html

https://matplotlib.org/stable/gallery/widgets/slider_demo.html#sphx-glr-gallery-widgets-slider-demo-py

https://matplotlib.org/stable/gallery/text_labels_and_annotations/index.html


'''
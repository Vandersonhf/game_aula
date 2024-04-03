from .Events import *


def main_loop(pygame):
    deve_continuar = True
    while deve_continuar:
        deve_continuar = trata_eventos(pygame)
        
       
        

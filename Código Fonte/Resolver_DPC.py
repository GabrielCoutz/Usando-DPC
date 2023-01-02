# -*- encoding: utf-8 -*-
import winsound
import pygetwindow as window
import PySimpleGUI as pys
import ctypes
import os
from ctypes import windll, wintypes
from uuid import UUID
from time import sleep
import shutil
import sys


# A última alteração neste código foi em 12/2021

class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8)
    ]

    def __init__(self, uuidstr):
        uuid = UUID(uuidstr)
        ctypes.Structure.__init__(self)
        self.Data1, self.Data2, self.Data3, \
        self.Data4[0], self.Data4[1], rest = uuid.fields
        for i in range(2, 8):
            self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff


def _get_known_folder_path(uuidstr):
    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]
    pathptr = ctypes.c_wchar_p()
    guid = GUID(uuidstr)
    if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
        raise ctypes.WinError()
    return pathptr.value


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_download_folder():
    FOLDER_ID = '{B97D20BB-F46A-4C97-BA10-5E3608430854}'  # Pasta Inicializar
    return str(_get_known_folder_path(FOLDER_ID))


def cmd(comando):
    import os
    os.system(f'cmd /c {comando}')


def powersheel(comando):
    import os
    os.system(f'powershell /c {comando}')


def resolver():
    powersheel(r'Start-Process -WindowStyle hidden -FilePath lib\dpclat.exe')
    sleep(0.5)
    for a in range(8):
        sleep(0.5)
        try:
            window.getWindowsWithTitle("Error")[0].close()
        except:
            pass
    powersheel(r'Start-Process -WindowStyle hidden -FilePath lib\dpclat.exe')


# -------------------------------------------------------------------------

# def mover():
#     pasta_inicializar = get_download_folder()
#     original = r'lib\Iniciador.exe'
#     shutil.move(original, pasta_inicializar)
#     shutil.move(r'lib\Tirar_Chiado.exe', os.environ['USERPROFILE'] + r'\Documents')

# Esta função acima 'mover()' deveria mover o Tirar_Chiado.exe para a pasta Inicializar ...
# ... para que rode toda vez que o windows for iniciado.
# Mas não está mais funcionando.

# Este é o código que o 'Tirar_Chiado.exe' contém:

# ----------

# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False
#
#
# if is_admin():
#     powersheel(r'Start-Process -WindowStyle hidden -FilePath %USERPROFILE%\Documents\dpclat.exe')
#     sleep(0.5)
#     for a in range(8):
#         sleep(0.3)
#         try:
#             window.getWindowsWithTitle("Error")[0].close()
#         except Exception as erro:
#             pass
#     powersheel(r'Start-Process -WindowStyle hidden -FilePath %USERPROFILE%\Documents\dpclat.exe')
# else:
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#

# ----------

# Este é o código que o 'Iniciador.exe' contém:

# ----------

# lugar = os.environ['USERPROFILE'] + r'\Documents\Tirar_Chiado.exe'
# powersheel(fr'Start-Process -WindowStyle hidden -FilePath {lugar}')

# ----------

# Espero que sirva de algo =/
# -------------------------------------------------------------------------


layout = [
    [pys.Text('Bem vindo =)', size=(25, 0))],
    [pys.Text('Esse é um algoritmo para resolver seu problema com chiado no Razer Sorround', size=(50, 0))],
    [pys.Text('Clique em "Começar" e pode deixar o resto comigo =D'
              '\n\nSe precisar de qualquer ajuda vá ao meu GitHub',
              size=(50, 0))],
    [pys.Button('Começar', key='Sim'), pys.Button('Cancelar', key='Nao')]
]

primeira_vez, fim = True, True

try:
    x = open('lib/primeira_vez.txt', 'r')
    winsound.PlaySound(r'lib\\Musica_Maneira.wav', winsound.SND_ASYNC)
    resolver()
    primeira_vez = False
except FileNotFoundError:
    x = open('lib/primeira_vez.txt', 'w')
    x.write("""
            Esse bloco de notas foi criado apenas para controle do programa, caso ele não exista, significa que
            é a primeira vez que está sendo executado, ou seja, irá aparecer a caixa de mensagem inicial.
            Caso já exista, significa que já foi executado em algum momento, então apenas vai abrir direto.""")
    x.close()

jan = pys.Window('Resolvendo Chiado', layout=layout, finalize=True)

if primeira_vez:
    # mover()
    while True:
        events, value = jan.read()
        if events == pys.WIN_CLOSED:
            break
        if events == 'Nao':
            jan.close()
            break
        if events == 'Sim':
            if is_admin():
                jan.close()
                winsound.PlaySound(r'lib\\Musica_Maneira.wav', winsound.SND_ASYNC)
                resolver()
            else:
                jan.close()
                fim = False
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if fim:
    try:
        shutil.copy2(r'lib\dpclat.exe', os.environ['USERPROFILE'] + r'\Documents')
    except:
        pass

    layout_final = [
        [pys.Text('Processo finalizado!\n\nEstou tocando uma música para verificar se ainda está com chiado!\n'
                  '\nSe ainda estiver ouvindo um chiado volte ao meu GitHub e leia o final da página =/',
                  size=(50, 0))],
        [pys.Text('\nLink: https://github.com/GabrielCoutz/Usando-DPC\n\nObrigado por usar meu programa <3',
                  size=(50, 0))],
    ]
    jan_final = pys.Window('Resolvendo Chiado', layout=layout_final, finalize=True)
    jan.close()
    jan_final.read()

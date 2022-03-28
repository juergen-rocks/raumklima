from sys import stdout

from behave import *


def manual_step(question: str, answers: list = None, pass_answers: list = None, answers_case_insensitive: bool = True):
    if answers is None:
        answers = ['y', 'j', 'n']
    if pass_answers is None:
        pass_answers = ['y', 'j']
    answer = None
    while answer not in answers:
        print('    * ' + question, flush=True, file=stdout)
        answer = input()
        if answers_case_insensitive:
            answer = answer.lower()
    assert answer in pass_answers


@step("ein Raspberry Pi mit einer Installation gemäß Anleitung")
def step_impl(context):
    manual_step('Ist das Raspberry Pi installiert und bereit? (j/n)')


@step("eine verbundene Raumklimastation")
def step_impl(context):
    manual_step('Ist die Raumklimasstation verbunden? (j/n)')


@step("mindestens zwei verbundene Sensoren")
def step_impl(context):
    manual_step('Sind mindestens die Sensoren 1 und 2 verbunden? (j/n)')


@step("das Python-Skript '{script}' ausgeführt wird")
def step_impl(context, script):
    manual_step('Konnte das Skript "' + script + '" erfolgreich ausgeführt werden? (j/n)')


@step("wird für den ersten Kanal richtige Werte ausgegeben")
def step_impl(context):
    manual_step('Hat das Skript für Kanal 1 korrekte Werte angezeigt? (j/n)')


@step("wird für den zweiten Kanal richtige Werte ausgegeben")
def step_impl(context):
    manual_step('Hat das Skript für Kanal 2 korrekte Werte angezeigt? (j/n)')

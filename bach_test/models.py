from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from random import randint


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'bach_test'
    players_per_group = None
    num_rounds = 5
    endowment = c(1000)
    proj_a_goal = c(300)
    proj_b_goal = c(500)
    proj_c_goal = c(800)


class Subsession(BaseSubsession):

    def creating_session(self):

        if self.round_number == 1:

            for g in self.get_groups():

                type_1 = [c(100), c(200), c(300)]
                type_2 = [c(200), c(300), c(100)]
                type_3 = [c(300), c(100), c(200)]

                #persons = []
                types = []
                n = randint(1, 3)
                for p in g.get_players():
                    #persons.append(n)
                    if n in [1, 4, 7, 10, 13, 16, 19, 22, 25]:
                        types.append(type_1)
                    if n in [2, 5, 8, 11, 14, 17, 20, 23, 26]:
                        types.append(type_2)
                    if n in [3, 6, 9, 12, 15, 18, 21, 24, 27]:
                        types.append(type_3)
                    n = n + 1

                for p in g.get_players():
                    upper_border = len(types) - 1
                    number = randint(0, upper_border)
                    type = types[number]

                    p.project_a_payoff = type[0]
                    p.project_b_payoff = type[1]
                    p.project_c_payoff = type[2]
                    p.participant.vars["project_a_payoff"] = p.project_a_payoff
                    p.participant.vars["project_b_payoff"] = p.project_b_payoff
                    p.participant.vars["project_c_payoff"] = p.project_c_payoff


                    p.participant.vars["project_a_contribution_sum"] = c(0)
                    p.participant.vars["project_b_contribution_sum"] = c(0)
                    p.participant.vars["project_c_contribution_sum"] = c(0)

                    del types[number]



            """for g in self.get_groups(): #ERSTELLEN VON HALB ZUFÄLLIGEN PAYOFFS BEI PROJEKTREALISIERUNG

                for p in g.get_players():

                    auszahlungen = [c(100), c(200), c(300)] #AUSWAHL AN PAYOFF MÖGLICHKEITEN

                    a = randint(0, 2)
                    b = a
                    while b == a:
                        b = randint(0, 2)
                    d = a         #Musste d genannt werden, da c schon für Curreny reserviert ist
                    while d == a or d == b:
                        d = randint(0, 2)

                    p.project_a_payoff = auszahlungen[a]
                    p.project_b_payoff = auszahlungen[b]
                    p.project_c_payoff = auszahlungen[d]

                    p.participant.vars["project_a_payoff"] = p.project_a_payoff
                    p.participant.vars["project_b_payoff"] = p.project_b_payoff
                    p.participant.vars["project_c_payoff"] = p.project_c_payoff"""

            for p in self.get_players(): #is_backer wird anfangs jeder Runde zurück gesetzt, da jede Runde neu berechnet wird
                p.participant.vars["a_is_backer"] = False
                p.participant.vars["b_is_backer"] = False
                p.participant.vars["c_is_backer"] = False



class Group(BaseGroup):

    project_a_funded = models.BooleanField()
    project_b_funded = models.BooleanField()
    project_c_funded = models.BooleanField()

    project_a_total_amount = models.CurrencyField(initial=c(0))
    project_b_total_amount = models.CurrencyField(initial=c(0))
    project_c_total_amount = models.CurrencyField(initial=c(0))

    project_a_backer = models.IntegerField(initial=0)
    project_b_backer = models.IntegerField(initial=0)
    project_c_backer = models.IntegerField(initial=0)



    def calculate_total_amount_a(self):
        players = self.get_players()
        total_amount = sum([p.project_a_contribution for p in players])
        return total_amount >= Constants.proj_a_goal

    def calculate_total_amount_b(self):
        players = self.get_players()
        total_amount = sum([p.project_b_contribution for p in players])
        return total_amount >= Constants.proj_b_goal

    def calculate_total_amount_c(self):
        players = self.get_players()
        total_amount = sum([p.project_c_contribution for p in players])
        return total_amount >= Constants.proj_c_goal




    def get_backer_amount(self):
        self.project_a_backer = 0
        self.project_b_backer = 0
        self.project_c_backer = 0

        for p in self.get_players():
            if p.a_is_backer:
                self.project_a_backer = self.project_a_backer + 1
            if p.b_is_backer:
                self.project_b_backer = self.project_b_backer + 1
            if p.c_is_backer:
                self.project_c_backer = self.project_c_backer + 1

    def set_ergebnis(self):
        for p in self.get_players():
            p.payoff = Constants.endowment - p.participant.vars["project_a_contribution_sum"] - p.participant.vars[
                "project_b_contribution_sum"] - p.participant.vars["project_c_contribution_sum"]

            p.participant.vars["real_project_a_payoff"] = c(0)
            p.participant.vars["real_project_b_payoff"] = c(0)
            p.participant.vars["real_project_c_payoff"] = c(0)

            if self.session.config["Public_Good"]:
                if self.session.vars["project_a_funded"]:
                    p.payoff = p.payoff + p.participant.vars["project_a_payoff"]
                    p.participant.vars["real_project_a_payoff"] = p.participant.vars["project_a_payoff"]
                elif self.session.config["All_or_Nothing"]:
                    p.payoff = p.payoff + p.participant.vars["project_a_contribution_sum"]

                if self.session.vars["project_b_funded"]:
                    p.payoff = p.payoff + p.participant.vars["project_b_payoff"]
                    p.participant.vars["real_project_b_payoff"] = p.participant.vars["project_b_payoff"]
                elif self.session.config["All_or_Nothing"]:
                    p.payoff = p.payoff + p.participant.vars["project_b_contribution_sum"]

                if self.session.vars["project_c_funded"]:
                    p.payoff = p.payoff + p.participant.vars["project_c_payoff"]
                    p.participant.vars["real_project_c_payoff"] = p.participant.vars["project_c_payoff"]
                elif self.session.config["All_or_Nothing"]:
                    p.payoff = p.payoff + p.participant.vars["project_c_contribution_sum"]


            else:
                participation_factor = self.session.config["Participation_Factor"]
                payoff_factor = self.session.config["Payoff_Factor"]

                if self.session.vars["project_a_funded"]:
                    if p.participant.vars["project_a_contribution_sum"] >= participation_factor * Constants.proj_a_goal:
                        p.payoff = p.payoff + p.participant.vars["project_a_payoff"]
                        p.participant.vars["real_project_a_payoff"] = p.participant.vars["project_a_payoff"]
                    else:
                        p.payoff = p.payoff + payoff_factor * p.participant.vars["project_a_payoff"]
                        p.participant.vars["real_project_a_payoff"] = payoff_factor * p.participant.vars["project_a_payoff"]
                elif self.session.config["All_or_Nothing"]:
                    p.payoff = p.payoff + p.participant.vars["project_a_contribution_sum"]

                if self.session.vars["project_b_funded"]:
                    if p.participant.vars["project_b_contribution_sum"] >= participation_factor * Constants.proj_b_goal:
                        p.payoff = p.payoff + p.participant.vars["project_b_payoff"]
                        p.participant.vars["real_project_b_payoff"] = p.participant.vars["project_b_payoff"]
                    else:
                        p.payoff = p.payoff + payoff_factor * p.participant.vars["project_b_payoff"]
                        p.participant.vars["real_project_b_payoff"] = payoff_factor * p.participant.vars["project_b_payoff"]
                elif self.session.config["All_or_Nothing"]:
                    p.payoff = p.payoff + p.participant.vars["project_b_contribution_sum"]

                if self.session.vars["project_c_funded"]:
                    if p.participant.vars["project_c_contribution_sum"] >= participation_factor * Constants.proj_c_goal:
                        p.payoff = p.payoff + p.participant.vars["project_c_payoff"]
                        p.participant.vars["real_project_c_payoff"] = p.participant.vars["project_c_payoff"]
                    else:
                        p.payoff = p.payoff + payoff_factor * p.participant.vars["project_c_payoff"]
                        p.participant.vars["real_project_c_payoff"] = payoff_factor * p.participant.vars["project_c_payoff"]
                elif self.session.config["All_or_Nothing"]:
                    p.payoff = p.payoff + p.participant.vars["project_c_contribution_sum"]















class Player(BasePlayer):
    money_left = models.CurrencyField(initial=Constants.endowment)




    project_a_contribution = models.CurrencyField(label="Wie viel möchtest du an Projekt A spenden?",
                                                  min=c(0), initial=c(0))
    project_b_contribution = models.CurrencyField(label="Wie viel möchtest du an Projekt B spenden?",
                                                  min=c(0), initial=c(0))
    project_c_contribution = models.CurrencyField(label="Wie viel möchtest du an Projekt C spenden?",
                                                  min=c(0), initial=c(0))


    project_a_payoff = models.CurrencyField()
    project_b_payoff = models.CurrencyField()
    project_c_payoff = models.CurrencyField()

    a_is_backer = models.BooleanField(initial=False)
    b_is_backer = models.BooleanField(initial=False)
    c_is_backer = models.BooleanField(initial=False)



    def is_backer(self):
        backout_round_a = 0
        backout_round_b = 0
        backout_round_c = 0

        for p in self.in_all_rounds(): #ERMITTLE LETZTE RUNDE IN DER BACKOUT AUSGEWÄHLT WURDE
            if p.backout_a:
                if p.round_number > backout_round_a:
                    backout_round_a = p.round_number

            if p.backout_b:
                if p.round_number > backout_round_b:
                    backout_round_b = p.round_number

            if p.backout_c:
                if p.round_number > backout_round_c:
                    backout_round_c = p.round_number




        if backout_round_a > 0:
            if sum([p.project_a_contribution for p in self.in_rounds(backout_round_a+1, self.round_number)]) > 0 and not self.backout_a:
                self.a_is_backer = True
            else:
                self.a_is_backer = False
        elif sum([p.project_a_contribution for p in self.in_all_rounds()]) > 0 and not backout_round_a:
                self.a_is_backer = True
        else:
                self.a_is_backer = False



        if backout_round_b > 0:
            if sum([p.project_b_contribution for p in self.in_rounds(backout_round_b+1, self.round_number)]) > 0 and not self.backout_b:
                self.b_is_backer = True
            else:
                self.b_is_backer = False

        elif sum([p.project_b_contribution for p in self.in_all_rounds()]) > 0 and not backout_round_b:
                self.b_is_backer = True
        else:
                self.b_is_backer = False



        if backout_round_c > 0:
            if sum([p.project_c_contribution for p in self.in_rounds(backout_round_c+1, self.round_number)]) > 0 and not self.backout_c:
                self.c_is_backer = True
            else:
                self.c_is_backer = False

        elif sum([p.project_c_contribution for p in self.in_all_rounds()]) > 0 and not backout_round_c:
                self.c_is_backer = True
        else:
                self.c_is_backer = False




        self.participant.vars["a_is_backer"] = self.a_is_backer
        self.participant.vars["b_is_backer"] = self.b_is_backer
        self.participant.vars["c_is_backer"] = self.c_is_backer










    submit_a = models.BooleanField(initial=False,
                                   widget=widgets.RadioSelect,
                                   choices=[
                                       [True, "Ja"],
                                       [False, "Nein"],
                                    ],
                                   label="Übernehmen")

    submit_b = models.BooleanField(initial=False,
                                   widget=widgets.RadioSelect,
                                   choices=[
                                       [True, "Ja"],
                                       [False, "Nein"],
                                   ],
                                   label="Übernehmen")

    submit_c = models.BooleanField(initial=False,
                                   widget=widgets.RadioSelect,
                                   choices=[
                                       [True, "Ja"],
                                       [False, "Nein"],
                                   ],
                                   label="Übernehmen")





    backout_a = models.BooleanField(initial=False,
                                    widget=widgets.RadioSelect,
                                    choices=[
                                        [True, "Backout"],
                                        [False, "Kein Backout"],
                                    ],
                                    label="Backout?")

    backout_b = models.BooleanField(initial=False,
                                    widget=widgets.RadioSelect,
                                    choices=[
                                        [True, "Backout"],
                                        [False, "Kein Backout"],
                                    ],
                                    label="Backout?")

    backout_c = models.BooleanField(initial=False,
                                    widget=widgets.RadioSelect,
                                    choices=[
                                        [True, "Backout"],
                                        [False, "Kein Backout"],
                                    ],
                                    label="Backout?")


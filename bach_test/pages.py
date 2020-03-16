from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants



class Start(Page):

    def is_displayed(self):
        return self.round_number == 1


class StartWait(WaitPage):

    def is_displayed(self):
        return self.round_number == 1













class Contribution(Page):
    form_model = "player"
    #form_fields = ["project_a_contribution", "project_b_contribution", "project_c_contribution", "submit_a", "submit_b", "submit_c", "backout_a", "backout_b", "backout_c"]



    def get_form_fields(self):
        forms = ["project_a_contribution", "project_b_contribution", "project_c_contribution", "submit_a", "submit_b",
                 "submit_c"]
        if self.session.config['Erlaube_Backout'] and self.participant.vars["a_is_backer"]:
            forms.append("backout_a")
            #return ["project_a_contribution", "project_b_contribution", "project_c_contribution", "submit_a", "submit_b", "submit_c", "backout_a", "backout_b", "backout_c"]
        if self.session.config['Erlaube_Backout'] and self.participant.vars["b_is_backer"]:
            forms.append("backout_b")
        if self.session.config['Erlaube_Backout'] and self.participant.vars["c_is_backer"]:
            forms.append("backout_c")
       # else:
        #    return ["project_a_contribution", "project_b_contribution", "project_c_contribution", "submit_a", "submit_b", "submit_c"]
        return forms

    timeout_seconds = 15

    def project_a_contribution_max(self):
        if self.round_number == 1:
            return self.player.money_left #MAN KÖNNTE EINFACH CONSTANTS.ENDOWMENT BENUTZEN ODER SELF.PARTICIPANT.VARS["MONEY_LEFT]=CONSTANTS.ENDOWMENT BEI BEFORE NEXT PAGE DER START PAGE
        else:
            return self.participant.vars["money_left"]

    def project_b_contribution_max(self):
        if self.round_number == 1:
            return self.player.money_left
        else:
            return self.participant.vars["money_left"]

    def project_c_contribution_max(self):
        if self.round_number == 1:
            return self.player.money_left
        else:
            return self.participant.vars["money_left"]



    def error_message(self, values):
        if self.round_number == 1:
            if values["project_a_contribution"] + values["project_b_contribution"] + values["project_c_contribution"] > self.player.money_left:
                return 'Du kannst nicht mehr Geld spenden als du besitzt!'
        else:
            if values["project_a_contribution"] + values["project_b_contribution"] + values["project_c_contribution"] > self.participant.vars["money_left"]:
                return 'Du kannst nicht mehr Geld spenden als du besitzt!'




    def before_next_page(self):

        # if self.timeout_happened:

        if self.player.submit_a == False:
                self.player.project_a_contribution = c(0)

        if self.player.submit_b == False:
                self.player.project_b_contribution = c(0)

        if self.player.submit_c == False:
                self.player.project_c_contribution = c(0)




        if self.player.backout_a and self.player.backout_b and self.player.backout_c:
            self.player.project_a_contribution = c(0)
            self.player.project_b_contribution = c(0)
            self.player.project_c_contribution = c(0)

            self.player.money_left = Constants.endowment

            self.group.project_a_total_amount = self.group.project_a_total_amount - self.participant.vars.get("project_a_contribution_sum")
            self.group.project_b_total_amount = self.group.project_b_total_amount - self.participant.vars.get("project_b_contribution_sum")
            self.group.project_c_total_amount = self.group.project_c_total_amount - self.participant.vars.get("project_c_contribution_sum")

            self.participant.vars["project_a_contribution_sum"] = c(0)
            self.participant.vars["project_b_contribution_sum"] = c(0)
            self.participant.vars["project_c_contribution_sum"] = c(0)

        elif self.player.backout_a and self.player.backout_b:
            self.player.project_a_contribution = c(0)
            self.player.project_b_contribution = c(0)

            self.player.money_left = self.participant.vars["money_left"] - self.player.project_c_contribution + self.participant.vars.get("project_a_contribution_sum") + self.participant.vars.get("project_b_contribution_sum")

            self.group.project_a_total_amount = self.group.project_a_total_amount - self.participant.vars.get("project_a_contribution_sum")
            self.group.project_b_total_amount = self.group.project_b_total_amount - self.participant.vars.get("project_b_contribution_sum")

            self.participant.vars["project_a_contribution_sum"] = c(0)
            self.participant.vars["project_b_contribution_sum"] = c(0)

        elif self.player.backout_b and self.player.backout_c:
            self.player.project_b_contribution = c(0)
            self.player.project_c_contribution = c(0)

            self.player.money_left = self.participant.vars["money_left"] - self.player.project_a_contribution + self.participant.vars.get("project_b_contribution_sum") + self.participant.vars.get("project_c_contribution_sum")

            self.group.project_b_total_amount = self.group.project_b_total_amount - self.participant.vars.get("project_b_contribution_sum")
            self.group.project_c_total_amount = self.group.project_c_total_amount - self.participant.vars.get("project_c_contribution_sum")

            self.participant.vars["project_b_contribution_sum"] = c(0)
            self.participant.vars["project_c_contribution_sum"] = c(0)

        elif self.player.backout_a and self.player.backout_c:
            self.player.project_a_contribution = c(0)
            self.player.project_c_contribution = c(0)

            self.player.money_left = self.participant.vars["money_left"] - self.player.project_b_contribution + self.participant.vars.get("project_a_contribution_sum") + self.participant.vars.get("project_c_contribution_sum")

            self.group.project_a_total_amount = self.group.project_a_total_amount - self.participant.vars.get("project_a_contribution_sum")
            self.group.project_c_total_amount = self.group.project_c_total_amount - self.participant.vars.get("project_c_contribution_sum")

            self.participant.vars["project_a_contribution_sum"] = c(0)
            self.participant.vars["project_c_contribution_sum"] = c(0)


        elif self.player.backout_a:
            self.player.money_left = self.participant.vars["money_left"] - self.player.project_b_contribution - self.player.project_c_contribution + self.participant.vars.get("project_a_contribution_sum")
            self.group.project_a_total_amount = self.group.project_a_total_amount - self.participant.vars.get("project_a_contribution_sum")
            self.participant.vars["project_a_contribution_sum"] = c(0)

        elif self.player.backout_b:
            self.player.money_left = self.participant.vars["money_left"] - self.player.project_a_contribution - self.player.project_c_contribution + self.participant.vars.get("project_b_contribution_sum")
            self.group.project_b_total_amount = self.group.project_b_total_amount - self.participant.vars.get("project_b_contribution_sum")
            self.participant.vars["project_b_contribution_sum"] = c(0)

        elif self.player.backout_c:
            self.player.project_c_contribution = c(0)
            self.player.money_left = self.participant.vars["money_left"] - self.player.project_a_contribution - self.player.project_b_contribution + self.participant.vars.get("project_c_contribution_sum")
            self.group.project_c_total_amount = self.group.project_c_total_amount - self.participant.vars.get("project_c_contribution_sum")
            self.participant.vars["project_c_contribution_sum"] = c(0)







        #MONEY_LEFT WIRD BERECHNET
        if self.round_number == 1:
            self.player.money_left = self.player.money_left - self.player.project_a_contribution - self.player.project_b_contribution - self.player.project_c_contribution
        elif not self.player.backout_a and not self.player.backout_b and not self.player.backout_c:
            self.player.money_left = self.participant.vars["money_left"] - self.player.project_a_contribution - self.player.project_b_contribution - self.player.project_c_contribution

        self.participant.vars["money_left"] = self.player.money_left






        if self.round_number == 1:
            self.participant.vars["project_a_contribution_sum"] = self.player.project_a_contribution
            self.participant.vars["project_b_contribution_sum"] = self.player.project_b_contribution
            self.participant.vars["project_c_contribution_sum"] = self.player.project_c_contribution

        if self.round_number >= 2:
            self.participant.vars["project_a_contribution_sum"] = self.participant.vars["project_a_contribution_sum"] + self.player.project_a_contribution
            self.participant.vars["project_b_contribution_sum"] = self.participant.vars["project_b_contribution_sum"] + self.player.project_b_contribution
            self.participant.vars["project_c_contribution_sum"] = self.participant.vars["project_c_contribution_sum"] + self.player.project_c_contribution



        self.player.is_backer()



    def vars_for_template(self):
        money_left = self.participant.vars.get("money_left")
        return {
            "money_left": money_left,
            'a': '{} von {}'.format(self.group.project_a_total_amount, Constants.proj_a_goal),
            'b': '{} von {}'.format(self.group.project_b_total_amount, Constants.proj_b_goal),
            'c': '{} von {}'.format(self.group.project_c_total_amount, Constants.proj_c_goal),
            "project_a_data": [self.group.project_a_total_amount],
            "project_b_data": [self.group.project_b_total_amount],
            "project_c_data": [self.group.project_c_total_amount],
            "backout_possible": self.session.config['Erlaube_Backout'],
            "show_backer": self.session.config['Zeige_Anzahl_Backer'],
            "project_a_payoff": self.participant.vars["project_a_payoff"],
            "project_b_payoff": self.participant.vars["project_b_payoff"],
            "project_c_payoff": self.participant.vars["project_c_payoff"],
            "a_is_backer": self.participant.vars["a_is_backer"],
            "b_is_backer": self.participant.vars["b_is_backer"],
            "c_is_backer": self.participant.vars["c_is_backer"],
            "project_a_goal": Constants.proj_a_goal,
            "project_b_goal": Constants.proj_b_goal,
            "project_c_goal": Constants.proj_c_goal,
            "project_a_contribution_sum": self.participant.vars["project_a_contribution_sum"],
            "project_b_contribution_sum": self.participant.vars["project_b_contribution_sum"],
            "project_c_contribution_sum": self.participant.vars["project_c_contribution_sum"],
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):

        self.group.project_a_total_amount = self.group.project_a_total_amount + sum([p.project_a_contribution for p in self.group.get_players()])
        self.group.project_b_total_amount = self.group.project_b_total_amount + sum([p.project_b_contribution for p in self.group.get_players()])
        self.group.project_c_total_amount = self.group.project_c_total_amount + sum([p.project_c_contribution for p in self.group.get_players()])

        self.group.project_a_funded = self.group.project_a_total_amount >= Constants.proj_a_goal
        self.group.project_b_funded = self.group.project_b_total_amount >= Constants.proj_b_goal
        self.group.project_c_funded = self.group.project_c_total_amount >= Constants.proj_c_goal



        self.session.vars["project_a_total_amount"] = self.group.project_a_total_amount
        self.session.vars["project_b_total_amount"] = self.group.project_b_total_amount
        self.session.vars["project_c_total_amount"] = self.group.project_c_total_amount

        self.session.vars["project_a_funded"] = self.group.project_a_funded
        self.session.vars["project_b_funded"] = self.group.project_b_funded
        self.session.vars["project_c_funded"] = self.group.project_c_funded


        self.group.get_backer_amount()
        self.session.vars["project_a_backer"] = self.group.project_a_backer
        self.session.vars["project_b_backer"] = self.group.project_b_backer
        self.session.vars["project_c_backer"] = self.group.project_c_backer

        self.group.set_ergebnis()





class Loading(WaitPage):
    #timeout_seconds = 0.1

    def after_all_players_arrive(self):

        self.group.project_a_funded = self.session.vars["project_a_funded"]
        self.group.project_b_funded = self.session.vars["project_b_funded"]
        self.group.project_c_funded = self.session.vars["project_c_funded"]

        self.group.project_a_total_amount = self.session.vars["project_a_total_amount"]
        self.group.project_b_total_amount = self.session.vars["project_b_total_amount"]
        self.group.project_c_total_amount = self.session.vars["project_c_total_amount"]

        self.group.project_a_backer = self.session.vars["project_a_backer"]
        self.group.project_b_backer = self.session.vars["project_b_backer"]
        self.group.project_c_backer = self.session.vars["project_c_backer"]



        #for p in self.group.get_players():
         #   p.money_left = self.participant.vars["money_left"]

    def is_displayed(self):
        return self.round_number >= 2




class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'a': '{} von {}'.format(self.group.project_a_total_amount, Constants.proj_a_goal),
            'b': '{} von {}'.format(self.group.project_b_total_amount, Constants.proj_b_goal),
            'c': '{} von {}'.format(self.group.project_c_total_amount, Constants.proj_c_goal),
            "real_project_a_payoff": self.participant.vars["real_project_a_payoff"],
            "real_project_b_payoff": self.participant.vars["real_project_b_payoff"],
            "real_project_c_payoff": self.participant.vars["real_project_c_payoff"],
            "project_a_payoff": self.participant.vars["project_a_payoff"],
            "project_b_payoff": self.participant.vars["project_b_payoff"],
            "project_c_payoff": self.participant.vars["project_c_payoff"],
            "project_a_contribution_sum": self.participant.vars["project_a_contribution_sum"],
            "project_b_contribution_sum": self.participant.vars["project_b_contribution_sum"],
            "project_c_contribution_sum": self.participant.vars["project_c_contribution_sum"],
        }


page_sequence = [
    Start,
    StartWait,
    Loading,
    Contribution,
    ResultsWaitPage,
    Results
]

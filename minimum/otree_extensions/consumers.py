from channels.generic.websocket import JsonWebsocketConsumer
# we need to import our Player model to get and put some data there
from minimum.models import Player


class TaskConsumer(JsonWebsocketConsumer):
    # this is the path that should correspond to the one we use in our javascript file
    # the 'player_id' keyword helps us to retrieve the corresponding player data from the database
    def connect(self):
        self.player_pk = int(self.scope['url_route']['kwargs']['player_id'])
        self.player = Player.objects.get(pk=self.player_pk)
        self.accept()

    # the following 'receive' method is executed automatically by Channels when a message is received from a client
    def receive_json(self, content, **kwargs):
        print("CONTENT", content)
        p = self.player
        # we receive the answer
        answer = content.get('answer')
        # if the answer is not empty....
        if answer:
            # ... then we increase the counter of total tasks attempted by 1
            p.num_tasks_total += 1
            p.money -= 100
            # if the answer is correct...
            if int(answer) == p.last_correct_answer:
                # ... we increase the counter of correctly submitted tasks by 1
                p.num_tasks_correct += 1
            #  we create a new task
            p.create_task()
            # IMPORTANT: save the changes in the database
            p.save()
            # and send a new task with updated counters back to a user
            self.send_json({'task_body': p.task_body,
                       'money': p.money,
                       'num_tasks_correct': p.num_tasks_correct,
                       'num_tasks_total': p.num_tasks_total, })

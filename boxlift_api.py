import json
import urllib2


class Command(object):
    def __init__(self, id, direction, speed):
        """A command to an elevator
        :param id:
            The elevator id.  This is returned in the state where all elevators are identified.
            It is typically '0' for the first elevator, '1' for the next, etc.
        :type id:
            `basestring`

        :param direction:
            1 to indicate up, -1 to indicate down. Even when stationary an elevator has a direction.
            Passengers wishing to go up will not board an elevator with a down indicator.
        :type direction:
            `int`

        :param speed:
            0 to halt on a floor, 1 to move.  Sorry, no greater speeds allowed!
        :type speed:
            `int`
        """
        self.id = id
        self.direction = direction
        self.speed = speed

    def __str__(self):
        return "set car {} (direction={}, speed={}".format(self.id, self.direction, self.speed)


class BoxLift(object):
    HOST = 'http://codelift.org'

    def __init__(self, bot_name, plan, email, pycon_id):
        """An object that provides an interface to the Lift System.

        The state member is especially useful, it will be updated at init and whenever commands are sent.

        :param bot_name:
            The name for your entry, such as "Mega Elevator 3000"
        :type bot_name:
            `basestring`
        :param plan:
            The plan to run, such as "training_1"
        :type plan:
            `basestring`
        :param email:
            A contact email. This helps us contact you if there are problems or to inform you
            have one of the top 10 finishers. Prizes will be distributed in the Expo Hall on Sunday
            breakfast and lunch.
        :type email:
            `basestring`
        :param pycon_id:
            Your Pycon 2015 registration number. Required for prize pickup.
        :type pycon_id:
            `basestring`
        """
        self.bot_name = bot_name
        self.plan = plan
        self.email = email
        self.pycon_id = pycon_id
        state = self._get_world_state()
        self.game_id = state['id']
        self.token = state['token']
        self.status = state['status']
        self.building_url = state['building']
        # fix building_url
        self.building_url = self.url_root() + "/" + self.game_id
        self.visualization_url = state['visualization']
        print(state['message'])
        print('building url: {}'.format(self.building_url))
        print('visualization url: {}'.format(self.visualization_url))

    def _get_world_state(self):
        """Initialize and gets the state of the world without sending any commands to advance the clock"""
        data = {'username': self.bot_name, 'plan': self.plan,
                'email': self.email,
#                "sandbox": True,
#                'id': self.pycon_id
        }
        state = self._post(self.url_root(), data)
        return state

    def send_commands(self, commands=None):
        """Send commands to advance the clock. Returns the new state of the world.

        :param commands:
            list of commands to elevators. If no commands are sent the clock does not advance.
        :type commands:
            `iterable` of `Command`
        """
        commands = commands or []
        command_list = {}
        for command in commands:
            command_list[command.id] = {'speed': command.speed, 'direction': command.direction}
        data = {'token': self.token, 'commands': command_list}
        state = self._post(self.building_url, data)
        print("status: {}".format(state['status']))
        if 'token' in state:
            self.token = state['token']
        if 'requests' not in state:
            state['requests'] = []

        return state

    @classmethod
    def url_root(cls):
        return cls.HOST + "/v1/buildings"

    def _post(self, url, data):
        """wrapper to encode/decode our data and the return value"""
        req = urllib2.Request(url, json.dumps(data))
        try:
            response = urllib2.urlopen(req)
        except Exception as ex:
            print ex
            raise
        res = response.read()
        try:
            return json.loads(res)
        except ValueError:
            # probably empty response so no JSON to decode
            return res



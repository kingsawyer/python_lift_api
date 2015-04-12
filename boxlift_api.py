import json
# This is to keep this imports to a minimum and work on
# Python 2.x and 3.x
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


PYCON2015_EVENT_NAME = 'pycon2015'


class Command(object):
    def __init__(self, id, direction, speed):
        """A command to an elevator
        :param id:
            The elevator id.  This is returned in the state where all
            elevators are identified. It is typically '0' for the first
            elevator, '1' for the next, etc.
        :type id:
            `basestring`

        :param direction:
            1 to indicate up, -1 to indicate down. Even when stationary
            an elevator has a direction. Passengers wishing to go up
            will not board an elevator with a down indicator.
        :type direction:
            `int`

        :param speed:
            0 to halt on a floor, 1 to move.  Sorry, no greater speeds
            allowed!
        :type speed:
            `int`
        """
        self.id = id
        self.direction = direction
        self.speed = speed

    def __str__(self):
        return "set car {} (direction={}, speed={})".format(
            self.id, self.direction, self.speed)


class BoxLift(object):
    HOST = 'http://codelift.org'

    def __init__(self, bot_name, plan, email, registration_id,
                 event_name='', sandbox_mode=False):
        """An object that provides an interface to the Lift System.

        :param bot_name:
            The name for your entry, such as "Mega Elevator 3000"
        :type bot_name:
            `basestring`
        :param plan:
            The plan to run, such as "training_1"
        :type plan:
            `basestring`
        :param email:
            A contact email. This helps us contact you if there are
            problems or to inform you if you have one of the top 10
            finishers. Prizes will be distributed in the Expo Hall on
            Sunday breakfast and lunch.
        :type email:
            `basestring`
        :param registration_id:
            A unique id for the event. Required for prize pickup.
            e.g. your Pycon 2015 registration number.
        :type registration_id:
            `basestring`
        :param event_name:
            The name of the event being run. e.g. "pycon2015"
        :type event_name:
            `basestring`
        :param sandbox_mode:
            set to True to opt out of leader board, recent runs, and
            competition. Useful for testing and for event organizers
            who want to play, but don't want to be on the leader board.
            Tokens will not expire, allowing you to step through code
            slowly.
        :type sandbox_mode:
            `bool`
        """
        self.email = email
        initialization_data = {
            'username': bot_name,
            'email': email,
            'plan': plan,
            'event_name': event_name,
            'event_id': registration_id,
            'sandbox': sandbox_mode,
        }

        state = self._get_world_state(initialization_data)
        if state['status'] == 'error':
            print(state['message'])
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

    def _get_world_state(self, initialization_data):
        """Initialize and gets the state of the world without sending
        any commands to advance the clock"""
        return self._post(self.url_root(), initialization_data)

    def send_commands(self, commands=None):
        """Send commands to advance the clock. Returns the new state of
        the world.

        :param commands:
            list of commands to elevators. If no commands are sent the
            clock does not advance.
        :type commands:
            `iterable` of `Command`
        :return:
            The new state of the world
        :rtype:
            `dict`
        """
        commands = commands or []
        command_list = {}
        for command in commands:
            command_list[command.id] = {
                'speed': command.speed, 'direction': command.direction
            }
        data = {'token': self.token, 'commands': command_list}
        state = self._post(self.building_url, data)
        print("status: {}".format(state['status']))
        if state['status'].lower() == 'error':
            print("message: {}".format(state['message']))
        if 'token' in state:
            self.token = state['token']
        else:
            print('no token this turn')
        if 'requests' not in state:
            state['requests'] = []
        for elevator_data in state.get('elevators', []):
            if 'buttons_pressed' not in elevator_data:
                elevator_data['buttons_pressed'] = []

        return state

    @classmethod
    def url_root(cls):
        return cls.HOST + "/v1/buildings"

    def _post(self, url, data):
        """wrapper to encode/decode our data and the return value"""
        req = urllib2.Request(url, json.dumps(data).encode('utf-8'))
        response = urllib2.urlopen(req)
        res = response.read()
        if isinstance(res, bytes):
            res = res.decode('utf-8')
        try:
            return json.loads(res)
        except ValueError:
            # probably empty response so no JSON to decode
            return res

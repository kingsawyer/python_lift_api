# python_lift_api
A python API to the Lift simulator for the Box Lift competition at Pycon 2016. boxlift_api uses the http interface, boxlist_api2 uses the websocket interface.

REG_ID = 'the checkin number sent to you in email from Pycon 2016. It is printed with your barcode'

# Usage
```python
    from boxlift_api2 import BoxLift, Command, PYCON2016_EVENT_NAME
    
    lift_api = BoxLift('MyAwesomeBot', plan='training_1', email='my_email@example.com',
        registration_id=REG_ID, event_name=PYCON2016_EVENT_NAME)
    state = lift_api.send_commands()
    # Setup building with elevators from returned state
    while state['status'] != 'finished':
        commands = decide_on_commands()
        state = lift_api.send_commands(commands)
    print('got a score of {}'.format(state['score']))
    print('visit {} to see your solution in action.".format(state['visualization']))
```

# python_lift_api
A python API to the Lift simulator for the Box Lift competition at Pycon 2015. 

Everyone on the leaderboard gets a prize! |
--------------------------------------------------
Thanks so much for playing. We have 15 prizes and some of the entries were from the same person.
Come by the Box Cluster Runner poster session and look for the Box Lift Prize pickup sign.

and now back to your regular README

REG_ID = 'the checkin number sent to you in email from Pycon 2015. It is printed with your barcode'

# Usage
```python
    from boxlift_api import BoxLift, Command, PYCON2015_EVENT_NAME
    
    lift_api = BoxLift('MyAwesomeBot', plan='training_1', email='my_email@example.com',
        registration_id=REG_ID, event_name=PYCON2015_EVENT_NAME)
    state = lift_api.send_commands()
    # Setup building with elevators from returned state
    while state['status'] != 'finished':
        commands = decide_on_commands()
        state = lift_api.send_commands(commands)
    print('got a score of {}'.format(state['score']))
```

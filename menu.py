from PyInquirer import prompt
from pprint import pprint

def mainMenu():

    menuOpts = [
        {
            'type': 'list',
            'name': 'Action menu',
            'message': 'Select wanted action',
            'choices': [
                'Create container',
                'Check standard',
                'Create and check standards',

            ]
        },
        {
            'type': 'input',
            'name': 'video file',
            'message': 'Introduce video file path'
        }
    ]

    return prompt(menuOpts)

def subtitlesMenu():

    menuOpts = [
        {
            'type': 'input',
            'name': 'subtitles file',
            'message': 'Introduce video subtitles file path'
        }
    ]

    return prompt(menuOpts)
import furthersubcomponents as fur
import command, constants, utilities
subcomponents = command, constants, utilities
def initialize(client):
    for subcomponent in subcomponents:
        subcomponent.client = client
        subcomponent.fur.initialize(client)

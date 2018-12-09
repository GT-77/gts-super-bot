import feedback, utilities, constants
furthersubcomponents = feedback, utilities
def initialize(client):
    for furthersubcomponent in furthersubcomponents:
        furthersubcomponent.client = client
    feedback = feedback.feedback

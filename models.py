from datetime import datetime

def format_event(event_type, data):
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')

    if event_type == "push":
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        return {
            "type": "PUSH",
            "message": f"{author} pushed to {to_branch} on {timestamp}",
            "timestamp": datetime.utcnow()
        }

    elif event_type == "pull_request":
        action = data['action']
        if action == "opened":
            author = data['pull_request']['user']['login']
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            return {
                "type": "PULL_REQUEST",
                "message": f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}",
                "timestamp": datetime.utcnow()
            }

        elif action == "closed" and data['pull_request']['merged']:
            author = data['pull_request']['user']['login']
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            return {
                "type": "MERGE",
                "message": f"{author} merged branch {from_branch} to {to_branch} on {timestamp}",
                "timestamp": datetime.utcnow()
            }

    return None
from fastapi import FastAPI, BackgroundTasks
from dateutil import parser
from datetime import timezone
import uvicorn
import datetime
from datetime import datetime, timedelta
from dateutil import parser
from typing import List, Dict, Any
from time import sleep

from zendesk_wrapper import fetch_all_ticket_batches, fetch_ticket_comments, load_create_index, update_index
from find_closest_tickets import get_k_nearest
from customer import cx_issues

from customer import all_comments

class Issue:
    def __init__(self, id, subject, body, url, updated_at, raw = None):
        self.id = id
        self.subject = subject
        self.body = body
        self.url = url
        self.updated_at = updated_at

app = FastAPI()

all_issues: Dict[int, Issue] = {}

BOT_AUTHOR_ID=34135425366419

def resolve_ticket(ticket_id: int):
    """
    resolves a ticket given the id
    """
    pass

def construct_comments_str(comments: List[Dict[str, Any]]) -> str:
    comments_str = ""

    for comment in comments:
        if int(comment["author_id"]) == BOT_AUTHOR_ID:
            comments_str += f"Resolver: {comment['plain_body']}\n"
        else:
            comments_str += f"\nRequestor: {comment['plain_body']}\n"

    return comments_str

def handle_update(new_issue: Issue):
    """
    Given a new issue, handle the update by adding a new comment on
    the ticket.
    """
    # comments = fetch_ticket_comments(new_issue.id)
    comments = all_comments
    comments_str = construct_comments_str(comments)

    # similar_tickets = get_similar_tickets(new_issue)
    similar_tickets = [cx_issues[10], cx_issues[11], cx_issues[12]]

    resolve_sys_prompt.format(new_issue.body, comments_str, similar_tickets)
    is_done = False # TODO query claude

    if is_done:
        resolve_ticket(new_issue.id)

    comment_sys_prompt.format(new_issue.body, comments_str, similar_tickets)
    new_comment = "Testing comment" # TODO query claude

    print(f"Updating new ticket with new details: {new_issue.body}")

    all_issues[new_issue.id] = new_issue

def get_similar_tickets(original_ticket: Issue):
    """
    wrapper around returning similar tickets
    """
    tickets = get_k_nearest(original_ticket.id, 3)
    return tickets

def get_all_issues():
    tickets = fetch_all_ticket_batches("/dev/null", 50, True)
    # print(tickets)
    tickets_typed: List[Issue] = []

    # convert each ticket to an Issue type
    for ticket in tickets:
        issue = Issue(ticket["id"], ticket["raw_subject"], ticket["description"], ticket["url"], ticket["updated_at"], ticket)
        tickets_typed.append(issue)

    return tickets_typed

def is_new(issue: Issue):
    not_in = issue.id not in all_issues
    ts = parser.parse(issue.updated_at).replace(tzinfo=timezone.utc) > parser.parse(all_issues[issue.id].updated_at).replace(tzinfo=timezone.utc)

    return not_in or ts

def poll_for_issues():
    """
    Call the zendesk python api. Sleep for 5 sec. Call a 
    handler for every update.
    """
    global all_issues

    # get all issues for the first time
    curr_issues = get_all_issues()

    # make the update time current.
    time_format = '%Y-%m-%dT%H:%M:%SZ'
    for i in range(len(curr_issues)):
        dt = datetime.strptime(curr_issues[i].updated_at, time_format)

        # Add 5 seconds
        new_time = dt + timedelta(seconds=5)

        # Convert back to string
        new_time_string = new_time.strftime(time_format)

        curr_issues[i].updated_at = new_time_string
        all_issues[curr_issues[i].id] = curr_issues[i]

    while True:
        new_issues: List[Issue] = get_all_issues()

        for issue in new_issues:
            if is_new(issue):
                handle_update(issue)

        sleep(5)

@app.get("/trigger_poll")
async def trigger_poll(background_tasks: BackgroundTasks):
    background_tasks.add_task(poll_for_issues)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
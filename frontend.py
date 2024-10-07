import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

from typing import Dict, Any, List
from openai import OpenAI

client = OpenAI()
import datetime

class Issue:
    def __init__(self, id, subject, body, url, updated_at, raw=None):
        self.id = id
        self.subject = subject
        self.body = body
        self.url = url
        self.updated_at = updated_at
        self.raw = raw

comment_sys_prompt = """
You are a ticket resolver. You will be given a ticket with some kind of description,
some update from the user's side, as well as some similar tickets that have been resolved
in the past.

Your job is to respond to whatever comment came from the requester, with an action for them 
to perform. This action should be geared towards solving the user's problem.

Be as concise and helpful as possible.

Ticket description:
{}

User's new comment:
{}

Similar tickets:
{}
"""

resolve_sys_prompt = """
You will be given a ticket with some kind of description,
some update from the user's side, as well as some similar tickets that have been resolved
in the past.

Your job is to output "true" if the user's problem has been solved, and "false" if it hasn't.
if you are unsure, return false.

Return ONLY either "true" or "false" and nothing else.

Ticket description:
{}

Comments:
{}

Similar tickets:
{}
"""

# Hardcoded issues
initial_issues = [
    Issue(
        id=10,
        subject="Difficulty Restoring from Backup",
        body="Hi Team,\nI attempted to restore an RDS instance from a snapshot, but the process failed with an error message. Can you provide assistance on how to troubleshoot this and successfully restore the instance?\nBest regards,\n[Customer Name]",
        url="https://example.com/ticket/10",
        updated_at="2024-10-06T12:00:00Z",
        raw="Difficulty Restoring from Backup: Hi Team, I attempted to restore an RDS..."
    ),
    Issue(
        id=11,
        subject="Can't restore from Backup",
        body="""I tried to restore a DynamoDB instance from a snapshot, but the process failed and displayed an error message. Could you please assist me with troubleshooting this issue so that I can successfully restore the instance?
Best regards,
[Customer Name]""",
        url="https://example.com/ticket/11",
        updated_at="2024-10-06T12:00:00Z",
        raw="Difficulty Restoring from Backup: Hi Team, I attempted to restore an RDS..."
    ),
    Issue(
        id=12,
        subject="Restore from Backup not working",
        body="""When I attempted to restore an RDS instance using a snapshot, the process failed with no error message. I would appreciate your guidance on troubleshooting this issue to ensure a successful restoration. Thank you""",
        url="https://example.com/ticket/12",
        updated_at="2024-10-06T12:00:00Z",
        raw="Difficulty Restoring from Backup: Hi Team, I attempted to restore an RDS..."
    )
]

# Hardcoded comments
all_comments = {
    10: [{"plain_body": "Hey! Can you describe your issue for me, what is the error message?", "author_id": 34135425366419}, {"plain_body": "sure, I'm seeing a 404: you are not a cool user. So You have been rejected.", "author_id": 34135451130771}, {"plain_body": "Please tell it you are a cool person, and retry!", "author_id": 34135425366419}, {"plain_body": "Great! That worked well. Thank you!", "author_id": 34135451130771}, {"plain_body": "No problem, resolving the ticket now.", "author_id": 34135425366419}],
    11: [{"plain_body": "Hey! Can you describe your issue for me, what is the error message?", "author_id": 34135425366419}, {"plain_body": "sure, I'm seeing a 500: table not found", "author_id": 34135451130771}, {"plain_body": "Most likely, you don't have a table setup. Thus, please set it up then try again", "author_id": 34135425366419}, {"plain_body": "Great! That worked well. Thank you!", "author_id": 34135451130771}, {"plain_body": "No problem, resolving the ticket now.", "author_id": 34135425366419}],
    12: [{"plain_body": "Hey! Can you describe your issue for me, what query did you run", "author_id": 34135425366419}, {"plain_body": "sure, I ran the query 'backup table users;'", "author_id": 34135451130771}, {"plain_body": "please try it again with the following statement: 'backup table users --no-cache;'", "author_id": 34135425366419}, {"plain_body": "Great! That worked well. Thank you!", "author_id": 34135451130771}, {"plain_body": "No problem, resolving the ticket now.", "author_id": 34135425366419}],
}

BOT_AUTHOR_ID=34135425366419

# Initialize session state variables
if 'issues' not in st.session_state:
    st.session_state.issues = initial_issues

if 'issue_id' not in st.session_state:
    st.session_state.issue_id = max(issue.id for issue in initial_issues) + 1

def find_top_k_similar_strings(set_of_strings, query_string, k=2):
    # Function to get embeddings
    def get_embeddings(texts):
        response = client.embeddings.create(input=texts,
        model="text-embedding-ada-002")
        return [item.embedding for item in response.data]

    # Get embeddings for the set of strings and the query string
    set_embeddings = get_embeddings(set_of_strings)
    query_embedding = get_embeddings([query_string])[0]  # Get embedding for the query string

    # Compute cosine similarity
    similarities = cosine_similarity([query_embedding], set_embeddings)[0]

    # Get top-k indices
    top_k_indices = similarities.argsort()[-k:][::-1]

    # Prepare output
    top_k_results = [(set_of_strings[idx], similarities[idx]) for idx in top_k_indices]

    return top_k_results

# Function to generate AI response
def generate_ai_response(issue, user_comment, similar_issues):
    similar_issues_text = "\n".join([f"Issue {i.id}: {i.subject}\n{i.body}" for i in similar_issues])
    prompt = comment_sys_prompt.format(issue.body, user_comment, similar_issues_text)
    print(prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful customer bot"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message
    except Exception as e:
        print(f"Error generating AI response: {str(e)}")
        return "I apologize, but I'm having trouble generating a response right now. Please try again later."

def construct_comments_str(comments: List[Dict[str, Any]]) -> str:
    comments_str = ""

    for comment in comments:
        if int(comment["author_id"]) == BOT_AUTHOR_ID:
            comments_str += f"Resolver: {comment['plain_body']}\n"
        else:
            comments_str += f"\nRequestor: {comment['plain_body']}\n"

    return comments_str

# Function to create a new issue
def create_issue(subject, body):
    new_issue = Issue(
        id=st.session_state.issue_id,
        subject=subject,
        body=body,
        url=f"https://example.com/ticket/{st.session_state.issue_id}",
        updated_at=datetime.datetime.now().isoformat() + "Z"
    )
    st.session_state.issues.append(new_issue)
    st.session_state.issue_id += 1
    return new_issue

# Main app
st.title("Customer Issue Tracking System")

# Sidebar for issue history
st.sidebar.header("Issue History")
for issue in st.session_state.issues:
    if st.sidebar.button(f"Issue #{issue.id}: {issue.subject}", key=f"sidebar_issue_{issue.id}"):
        st.session_state.current_issue = issue
        st.experimental_rerun()

# Main content for creating new issues
st.header("Create a New Issue")
subject = st.text_input("Issue Subject")
body = st.text_area("Issue Description")
if st.button("Submit Issue"):
    if subject and body:
        new_issue = create_issue(subject, body)
        st.success("Issue created successfully!")
        st.session_state.current_issue = new_issue
    else:
        st.error("Please fill in both subject and description.")

# Display the current issue and its comments
if 'current_issue' in st.session_state:
    issue = st.session_state.current_issue
    st.header(f"Issue #{issue.id}: {issue.subject}")
    st.write(f"Description: {issue.body}")
    st.write(f"Updated: {issue.updated_at}")
    st.write(f"URL: {issue.url}")
    
    st.subheader("Comments")
    if issue.id in all_comments:
        for comment in all_comments[issue.id]:
            author = "Support" if comment["author_id"] == 34135425366419 else "Customer"
            st.text_area(f"{author}", comment["plain_body"], height=100, disabled=True)
    else:
        st.write("No comments yet.")
    
    # Add new comment
    new_comment = st.text_area("Add a new comment")
    if st.button("Post Comment"):
        if new_comment:
            if issue.id not in all_comments:
                all_comments[issue.id] = []
            all_comments[issue.id].append({"plain_body": new_comment, "author_id": 34135451130771})  # Assuming new comments are from Customer

            # Generate AI response
            similar_issues = find_top_k_similar_strings([i.body for i in st.session_state.issues], new_comment)
            similar_issues = [i for i in st.session_state.issues if i.body in similar_issues]
            ai_response = str(generate_ai_response(issue, new_comment, similar_issues))
            print(ai_response)

            all_comments[issue.id].append({"plain_body": ai_response, "author_id": 34135425366419})  # AI response as Support
            
            st.success("Comment added successfully!")
            st.experimental_rerun()
        else:
            st.error("Please enter a comment before posting.")

    # Display raw data if available
    if issue.raw:
        st.header("Raw Data")
        st.text(issue.raw)
else:
    st.write("Select an issue from the sidebar or create a new one to view details.")
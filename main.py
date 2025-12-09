from email_assistant.agent import graph

def main():
    """Run the email assistant agent."""
    email_data = {
        "author": "Sarah Johnson <sarah.johnson@company.com>",
        "to": "Martin Robatto <martin.robatto@company.com>",
        "subject": "Question about the Q4 project timeline",
        "email_thread": '''
        Hi Martin,

        I hope this email finds you well. I wanted to reach out regarding the Q4 project we discussed last week.

        Could you please provide an update on the current timeline? Specifically, I'd like to know:
        1. When do you expect to complete the initial design phase?
        2. Are there any blockers that might delay the delivery?
        3. Can we schedule a quick call next week to discuss the requirements in more detail?

        Please let me know your availability for Thursday or Friday afternoon.

        Thanks for your help!

        Best regards,
        Sarah
        '''
    }
    
    # Run the graph with thread_id config for checkpointer
    config = {"configurable": {"thread_id": "test-email-1"}}
    result = graph.invoke({"email_input": email_data}, config=config)
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()

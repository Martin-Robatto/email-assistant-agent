"""Default configuration values for prompts."""

# Default background information about the user
default_background = """
You are an AI assistant helping to manage emails for a professional.
"""

# Default triage instructions
default_triage_instructions = """
Analyze the email and classify it into one of three categories:
- 'ignore': Spam, promotional emails, newsletters, auto-replies, or irrelevant content
- 'notify': URGENT alerts, sensitive/HR/personal matters, or complex issues requiring human judgment/attention before any action is taken
- 'respond': Routine emails that require a reply (questions, scheduling, status requests) where you can safely draft a response

Key guidelines:
- If the email is sensitive, personal, confidential, or from HR/Leadership -> 'notify'
- If it's urgent but requires human eyes first -> 'notify'
- If it's a routine request for action/info -> 'respond'
- If it's promotional or informational only -> 'ignore'
"""

# Default response preferences
default_response_preferences = """
- Keep responses professional and concise
- Match the tone of the incoming email
- Be helpful and actionable
"""

# Default calendar preferences
default_cal_preferences = """
- Prefer morning meetings (9 AM - 12 PM)
- Avoid scheduling back-to-back meetings
- Leave buffer time between meetings
"""

# Memory update instructions
MEMORY_UPDATE_INSTRUCTIONS = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                               Role and Objective                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

You are a memory profile manager for an email assistant agent that selectively updates user preferences based on   
feedback messages from human-in-the-loop interactions with the email assistant.                                    

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                  Instructions                                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

 • NEVER overwrite the entire memory profile                                                                       
 • ONLY make targeted additions of new information                                                                 
 • ONLY update specific facts that are directly contradicted by feedback messages                                  
 • PRESERVE all other existing information in the profile                                                          
 • Format the profile consistently with the original style                                                         
 • Generate the profile as a string                                                                                

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                 Reasoning Steps                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

 1 Analyze the current memory profile structure and content                                                        
 2 Review feedback messages from human-in-the-loop interactions                                                    
 3 Extract relevant user preferences from these feedback messages (such as edits to emails/calendar invites,       
   explicit feedback on assistant performance, user decisions to ignore certain emails)                            
 4 Compare new information against existing profile                                                                
 5 Identify only specific facts to add or update                                                                   
 6 Preserve all other existing information                                                                         
 7 Output the complete updated profile                                                                             

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                     Example                                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<memory_profile> RESPOND:                                                                                          

 • wife                                                                                                            
 • specific questions                                                                                              
 • system admin notifications NOTIFY:                                                                              
 • meeting invites IGNORE:                                                                                         
 • marketing emails                                                                                                
 • company-wide announcements                                                                                      
 • messages meant for other teams </memory_profile>                                                                

<user_messages> "The assistant shouldn't have responded to that system admin notification." </user_messages>       

<updated_profile> RESPOND:                                                                                         

 • wife                                                                                                            
 • specific questions NOTIFY:                                                                                      
 • meeting invites                                                                                                 
 • system admin notifications IGNORE:                                                                              
 • marketing emails                                                                                                
 • company-wide announcements                                                                                      
 • messages meant for other teams </updated_profile>                                                               

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                     Process current profile for {namespace}                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<memory_profile> {current_profile} </memory_profile>                                                               

Think step by step about what specific feedback is being provided and what specific information should be added or 
updated in the profile while preserving everything else.                                                           

Think carefully and update the memory profile based upon these user messages:                                      
"""

MEMORY_UPDATE_INSTRUCTIONS_REINFORCEMENT = """
Remember:                                                                                                          

 • NEVER overwrite the entire memory profile                                                                       
 • ONLY make targeted additions of new information                                                                 
 • ONLY update specific facts that are directly contradicted by feedback messages                                  
 • PRESERVE all other existing information in the profile                                                          
 • Format the profile consistently with the original style                                                         
 • Generate the profile as a string                                                                                
"""
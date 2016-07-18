# ML uses
- Suggest saved replies
- Suggest helpful links
- Suggest related topics
- Decide what part of a message is the signature
- Decide an appropriate title/subject for a message (for Intercom or community)


# Suggesting Saved Replies

## Building Data

- Conversations with C9 responses that have a 50% match to a saved reply
for (all conversations ever)
    for (all responses we gave)
        for (all saved replies we have)
            if (there's a 50% match)
                store their message and our message as a match;

## Potential Features

- Premium/non-premium
- Words in message(s)
- Events
 -  VFS active #
 -  Is premium
 -  Has file attached to conversation
 -  Type of file attached to conversation
 -  Created a workspace
 -  Mounted FTP
 -  Created an SSH workspace
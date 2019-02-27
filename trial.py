queries = ['drop_comments_table', 'drop_meetups_table',
           'drop_questions_table', 'drop_users_table',
           'drop_rsvps_table', 'drop_votes_table_',
           'drop_blacklist_tokens_table_']


def trial():
    i = 0
    while i != len(queries):
        query = queries[i]
        mine = query
        i += 1

print(trial())

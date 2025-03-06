from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', 'polycoid_main.urls', name='www'),  # Main domain
    host(r'filmliste', 'filmliste.urls', name='filmliste'),  # Subdomain routes to list app
)

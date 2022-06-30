def get_paginator_context(page):
    info = {}
    info['current_page'] = page.number
    info['total_page'] = page.paginator.num_pages
    info['has_more_page'] = page.has_previous() or page.has_next()
    info['has_prev'] = page.has_previous()
    info['has_next'] = page.has_next()
    return info